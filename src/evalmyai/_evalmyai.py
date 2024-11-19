import json
import copy
from collections import OrderedDict
from collections.abc import Iterable
import pandas as pd
import requests
from evalmyai._validators import (
    validate_single_input_data,
    validate_dict,
    validate_single_output_score,
    validate_test_case_data,
)
from evalmyai._utils import order_output_dict, order_contradictions, order_f1

SYMBOLS = ["contradictions", "missing_facts", "f1"]
DEFAULT_SYMBOLS = [SYMBOLS[0]]
SYMBOLS_VERSION = {"contradictions": "1", "missing_facts": "1", "f1": "1"}

# The web address of the evalmy.ai web services.
URL_HOST = "https://evalmy.ai"
URL_API = f"{URL_HOST}/api"
URL_EVAL = f"{URL_API}/symbol/evaluate"

DEFAULT_SCORING = {
    "contradictions": {
        "name": "linear",
        "params": {
            "weights": {"critical": 1, "large": 0.5, "small": 0.1, "negligible": 0}
        },
    },
    "missing_facts": {
        "name": "linear",
        "params": {
            "weights": {"critical": 1, "large": 0.5, "small": 0.1, "negligible": 0}
        },
    },
    "f1": {
        "name": "linear",
        "params": {
            "weights": {"critical": 1, "large": 0.5, "small": 0.1, "negligible": 0}
        },
    }
}


class Evaluator:
    """
    Initializes the Evaluator class to evaluate AI model outputs with evalmyai. See [evalmyai-python](https://github.com/evalmy-ai/evalmyai-python).

    Args:
        auth (dict): Authentication details, either for OpenAI or Azure OpenAI. See [examples](#examples).
        token (str): evalmyai API token.
    Examples
    --------
    
    ### OpenAI Example:
    ```{python}
    from evalmyai import Evaluator

    token = "YOUR_EVALMYAI_TOKEN"
    auth_open_ai = {  
        "api_key": "cd0...101",
        "model": "gpt-4o", 
    }
    ev = Evaluator(auth_open_ai, token)
    ```

    ### Azure OpenAI Example:
    ```{python}
    from evalmyai import Evaluator

    token = "YOUR_EVALMYAI_TOKEN"
    auth_azure = {
                "api_key": "cd0...101",
                "azure_endpoint": "https://...azure.com/",
                "api_version": "2023-07-01-preview",
                "azure_deployment": "...",
    }
    ev = Evaluator(auth_azure, token)
    ```

    """
    def __init__(self, auth: dict, token: str):
        self.auth = auth
        self.token = token
        self.scoring = copy.deepcopy(DEFAULT_SCORING)

    def set_scoring(self, symbol: str, scoring: dict) -> None:
        """
        Sets the scoring criteria for a specified symbol.

        Args:
            symbol (str): The symbol for which scoring is to be replaced.
            scoring (dict): The scoring criteria. See `self.scoring` for default values.

        Raises:
            ValueError: If the symbol is not in SYMBOLS or the scoring format is invalid.
        """
        if symbol not in SYMBOLS:
            raise ValueError(f"Wrong symbol: {symbol}, one of {SYMBOLS} expected.")

        if not (v := validate_dict(DEFAULT_SCORING[symbol], scoring))[0]:
            raise ValueError(f"Wrong scoring format with msg: {v[1]}.")

        self.scoring[symbol] = scoring

    def evaluate(
        self,
        data: dict,
        symbols: list = DEFAULT_SYMBOLS,
        scoring: dict = None,
        retry_cnt: int = 1,
    ) -> OrderedDict:
        """
        Evaluates a single entry.

        Args:
            data (dict): A dictionary with textual keys "expected", "actual", and "context".
            symbols (list, optional): A list of symbols to be evaluated. Defaults to ["contradictions"].
            scoring (dict, optional): The scoring criteria. If not set, default from `self.scoring` is used.
            retry_cnt (int, optional): Number of times to retry evaluation in case of server errors. Defaults to 1.

        Returns:
            OrderedDict: A dictionary with keys given by symbols and values by evaluated score.

        Raises:
            ValueError: If input data or symbols are invalid, or if the output format is incorrect.
        """
        if "context" not in data:
            data["context"] = ""

        if not set(symbols) <= set(SYMBOLS):
            raise ValueError(f"Wrong symbols value. Should be subset of {SYMBOLS}")

        if not scoring:
            scoring = self.scoring
        else:
            for symbol in symbols:
                if symbol in scoring and scoring[symbol] is None:
                    scoring[symbol] = self.scoring[symbol]

        if not (v := validate_single_input_data(data))[0]:
            raise ValueError(f"Wrong input data format with msg: {v[1]}.")

        result = OrderedDict()

        for symbol in symbols:
            task = {
                "input_data": data,
                "scoring": scoring[symbol],
                "aggregation": {
                    "n_calls": 1,
                    "agg_method": "mean",
                },
                "auth": self.auth,
                "api_token": self.token,
            }

            for i in range(retry_cnt):
                response = requests.post(
                    f"{URL_EVAL}/{symbol}/v{SYMBOLS_VERSION[symbol]}".lower(), json=task
                )

                if response.status_code == 200:
                    res = response.json()

                    if (
                        "scores" not in res or res["scores"] is None
                    ) and i == retry_cnt - 1:
                        raise BaseException(res["reasoning"])

                    res["reasoning"] = json.loads(res["reasoning"])
                    result[symbol] = order_output_dict(res, order_f1 if symbol == "f1" else order_contradictions) # TBD!
                    break

                elif i == retry_cnt - 1:
                    response.raise_for_status()

        if not (v := validate_single_output_score(result))[0]:
            raise ValueError(f"Wrong output data format with msg: {v[1]}.")

        return result

    def evaluate_batch(
        self,
        data: list,
        symbols: list = DEFAULT_SYMBOLS,
        scoring: dict = None,
        retry_cnt: int = 1,
    ) -> list:
        """
        Evaluates a list of entries.

        Args:
            data (list): A list with entries for the `evaluate` function.
            symbols (list, optional): A list of symbols to be evaluated. Defaults to ["contradictions"].
            scoring (dict, optional): Scoring criteria. If not set, default from `self.scoring` is used.
            retry_cnt (int, optional): Number of times to retry evaluation in case of server errors. Defaults to 1.

        Returns:
            list: A tuple (results, errors) where `results` is a list of dictionaries with the scoring similar to
                  a single call of `evaluate` function or `None` if an error occurs, and `errors` is a list of
                  errors that occurred during evaluation or `None` if no error occurs.
        """
        result = list()
        errors = list()

        for entry in data:
            try:
                res = self.evaluate(
                    data=entry, symbols=symbols, scoring=scoring, retry_cnt=retry_cnt
                )
                result.append(res)
                errors.append(None)
            except Exception as e:
                result.append(None)
                errors.append(e)

        return result, errors

    def evaluate_test_case(
        self, test_case: dict, actual_values: Iterable[str] = None, retry_cnt: int = 1
    ) -> OrderedDict:
        """
        Evaluates a test case based on the provided test case data and actual values.

        Validates the test case data and scoring format, applies the context to each item,
        and evaluates each item using the provided actual values.

        Args:
            test_case: A dictionary containing the test case data. The expected structure is:
                {
                    "context": str,  # Optional context for all items.
                    "scoring": dict,  # Optional scoring criteria for symbols.
                    "items": [
                        {
                            "expected": str,  # Expected result.
                            "actual": str,    # Actual result (optional if `actual_values` is provided).
                            "context": str    # Optional context for this item.
                        },
                        ...
                    ]
                }
            actual_values: An iterable of actual values to be used for the items in the test case. If an item
                does not have an "actual" key, values from this iterable will be used.
            retry_cnt: The number of times to retry the evaluation of a single entry in case of a server error
                (e.g., GPT capacity issue). Default is 1.

        Returns:
            An OrderedDict representing the evaluation results. The structure of the result is:
                {
                    ... all non-items fields found in test_case are copied first,
                    "items": [
                        {
                            "expected": str,
                            "actual": str,
                            "context": str,  # If context was provided.
                            "symbol1": result,  # Result for symbol1.
                            "symbol2": result,  # Result for symbol2.
                            ...
                            "error": str  # If an error occurred.
                        },
                    ]
                }

        Raises:
            ValueError: If the input data format or scoring format is incorrect.
        """

        if not (v := validate_test_case_data(test_case))[0]:
            raise ValueError(f"Wrong input data format with msg: {v[1]}.")

        if "scoring" in test_case:
            scoring = test_case["scoring"]
            symbols = scoring.keys()
            for symbol in symbols:
                if scoring[symbol] is not None:
                    if not (v := validate_dict(DEFAULT_SCORING[symbol], scoring[symbol]))[
                        0
                    ]:
                        raise ValueError(f"Wrong scoring format with msg: {v[1]}.")
        else:
            scoring = None
            symbols = DEFAULT_SYMBOLS

        context = test_case["context"] if "context" in test_case else ""

        act_iter = iter(actual_values) if actual_values else None

        result = OrderedDict()

        for key in test_case:
            if key != "items":
                result[key] = copy.deepcopy(test_case[key])

        result["items"] = []

        for item in test_case["items"]:
            if context:
                item["context"] = (
                    context + ("\n" + item["context"]) if "context" in item else ""
                )

            if "actual" not in item:
                actual = next(act_iter, None)
                if actual:
                    item["actual"] = actual
            else:
                actual = item["actual"]

            res_item = OrderedDict()

            if "context" in item:
                res_item["context"] = item["context"]

            res_item["expected"] = item["expected"]
            res_item["actual"] = item["actual"]

            if actual:
                try:
                    res = self.evaluate(item, symbols=symbols, scoring=scoring, retry_cnt=retry_cnt)
                    for symbol in res:
                        res_item[symbol] = order_output_dict(
                            res[symbol], order_contradictions
                        )
                except requests.exceptions.HTTPError as e:
                    res_item["error"] = OrderedDict(
                        code=e.response.status_code,
                        text=str(e)
                    )
                except Exception as e:
                    res_item["error"] = str(e)

            else:
                res_item["error"] = "No actual value."

            result["items"].append(res_item)

        return result

    def evaluate_dataset(
        self,
        data: pd.DataFrame,
        symbols: list = DEFAULT_SYMBOLS,
        context: str = "",
        retry_cnt: int = 1,
    ) -> pd.DataFrame:
        """
        Evaluates an entire pandas DataFrame dataset.

        Args:
            data: A DataFrame with string columns 'expected' and 'actual', and optionally 'context'.
            symbols: A list of symbols to evaluate, defaults to ["contradictions"].
            context: A general context to precede the context of each row, defaults to an empty string.
            retry_cnt: The number of times to retry the evaluation of a single entry in case of a server error
                (e.g., GPT capacity issue). Default is 1.

        Returns:
            pd.DataFrame: A DataFrame containing the evaluation results. The output DataFrame has the same index as
            the input DataFrame and includes the following columns:
                - 'expected': str, same as in the input dataset.
                - 'actual': str, same as in the input dataset.
                - 'context': str, same as in the input dataset if exists, otherwise the context variable is used.
                - 'score_[sym]': float, the evaluated score value for each given symbol.
                - 'reason_[sym]': json, the reasoning for each given symbol, a JSON-encoded dictionary.
                - 'error': str, the list of errors during evaluation, or None if no error occurred.

        Raises:
            ValueError: If 'expected' or 'actual' columns are not found in the dataset.
        """

        if "expected" not in data.columns:
            raise ValueError("Column name 'expected' not found in the dataset.")

        if "actual" not in data.columns:
            raise ValueError("Column name 'actual' not found in the dataset.")

        scores = {k: [] for k in symbols}
        reasons = {k: [] for k in symbols}
        errors = []

        for row in data.itertuples():
            try:
                res = self.evaluate(
                    {
                        "expected": row.expected,
                        "actual": row.actual,
                        "context": context
                        + ("\n" + row.context if "context" in row else ""),
                    },
                    symbols=symbols,
                    retry_cnt=retry_cnt,
                )
                for symbol in res:
                    scores[symbol].append(res[symbol]["scores"]["score"])
                    reasons[symbol].append(res[symbol]["reasoning"])
                errors.append(None)
            except requests.exceptions.HTTPError as e:
                for symbol in symbols:
                    scores[symbol].append(float("nan"))
                    reasons[symbol].append("")
                errors.append(str(e) + "\n" + e.response.text)
            except Exception as e:
                for symbol in symbols:
                    scores[symbol].append(float("nan"))
                    reasons[symbol].append("")
                errors.append(e)

        result = {
            "expected": data["expected"],
            "actual": data["actual"],
            "context": data["context"] if "context" in data.columns else context,
        }

        for symbol in symbols:
            result[f"score_{symbol[:3]}"] = scores[symbol]

        for symbol in symbols:
            result[f"reason_{symbol[:3]}"] = reasons[symbol]

        result["error"] = errors

        return pd.DataFrame(data=result, index=data.index)
