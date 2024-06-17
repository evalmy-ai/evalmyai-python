import json

import pandas as pd
import requests
from .validators import validate_single_input_data, validate_dict, validate_single_output_score, validate_test_case_data

SYMBOLS = ["contradictions"]
SYMBOLS_VERSION = {
    "contradictions": "1"
}

# the web address of the evalmy.ai web services
URL_HOST = "https://dsk4hmhgxqrrr.cloudfront.net"
URL_API = f"{URL_HOST}/api"
URL_EVAL = f"{URL_API}/symbol/evaluate"

DEFAULT_SCORING = {
    "contradictions": {
        "name": "linear",
        "params": {
            "weights": {
                "critical": 1,
                "large": 0.5,
                "small": 0.1,
                "negligible": 0
            }
        }
    }
}


class Evaluator:

    def __init__(self, auth: dict, token: str):
        """
        :param auth: either OpenAI or Azure OpenAI authentication

            example OpenAI:
            {
                "api_key": e.g.: "cd0...101",
                "model":   e.g.: "gpt-4o",
            }

            example Azure OpenAI:
            {
                "api_key":          e.g.: "cd0...101",
                "azure_endpoint":   e.g.: "https://...azure.com/"
                "api_version":      e.g.: ""
                "azure_deployment": e.g.: "2023-07-01-preview"
            }

        :param token: evalmyai API token
        """
        self.auth = auth
        self.token = token

        self.scoring = DEFAULT_SCORING

    def set_scoring(self, symbol: str, scoring: dict) -> None:
        """
            Sets the scoring criteria for a specified symbol.
        :param symbol: the symbol which scoring is to be replaced
        :param scoring: the scoring criteria. see self.scoring for default values.
        """

        if symbol not in SYMBOLS:
            raise ValueError(f"Wrong symbol: {symbol}, one of {SYMBOLS} expected.")

        if not (v := validate_dict(DEFAULT_SCORING[symbol], scoring))[0]:
            raise ValueError(f"Wrong scoring format with msg: {v[1]}.")

        self.scoring[symbol] = scoring

    def evaluate(self, data: dict, symbols: list = SYMBOLS, scoring = None) -> dict:
        """
            Evaluates a single entry.

        :param data: a dictionary with textual keys "expected", "actual" and "context"
        :param symbols: a list of symbols to be evaluated
        :param scoring: the scoring criteria, if not set, defalt from self.scoring is used
        :return: a dictionary with keys given by symbols and values by evaluated score
        """

        if "context" not in data:
            data["context"] = ""

        if not scoring:
            scoring = self.scoring

        if not (v := validate_single_input_data(data))[0]:
            raise ValueError(f"Wrong input data format with msg: {v[1]}.")

        if not set(symbols) <= set(SYMBOLS):
            raise ValueError(f"Wrong symbols value. Should be subset of {SYMBOLS}")

        result = dict()

        for symbol in symbols:
            task = {
                "input_data": data,
                "scoring": scoring[symbol],
                "aggregation": {
                    "n_calls": 1,
                    "agg_method": "mean"
                },
                "auth": self.auth,
                "api_token": self.token
            }

            response = requests.post(f"{URL_EVAL}/{symbol}/v{SYMBOLS_VERSION[symbol]}".lower(), json=task)

            if response.status_code == 200:
                res = response.json()
                if "score" not in res or res["score"] is None:
                    raise BaseException(res["reasoning"])
                res["reasoning"] = json.loads(res["reasoning"])
                del res["call_outputs"]

                result[symbol] = res
            else:
                response.raise_for_status()

        if not (v := validate_single_output_score(result))[0]:
            raise ValueError(f"Wrong output data format with msg: {v[1]}.")

        return result

    def evaluate_batch(self, data: list, symbols: list = SYMBOLS) -> list:
        """
            Evaluates a list of entries.

        :param data: a list with entries for evaluate function
        :param symbols: a list of symbols to be evaluated
        :return: a tuple (results, errors) where *results* is a list of dictionaries with the scoring similar to single
        call of evaluate function or Nones if error happens and *errors* is a list of errors that happened during the
        evaluation or Nones if no error happens
        """

        result = list()
        errors = list()

        for entry in data:
            try:
                res = self.evaluate(entry, symbols)
                result.append(res)
                errors.append(None)
            except Exception as e:
                result.append(None)
                errors.append(e)

        return result, errors

    def evaluate_test_case(self, data: dict) -> str:

        if not (v := validate_test_case_data(data))[0]:
            raise ValueError(f"Wrong input data format with msg: {v[1]}.")

        if "scoring" in data:
            scoring = data["scoring"]
            symbols = scoring.keys()
            for symbol in symbols:
                if not (v := validate_dict(DEFAULT_SCORING[symbol], scoring[symbol]))[0]:
                    raise ValueError(f"Wrong scoring format with msg: {v[1]}.")
        else:
            symbols = SYMBOLS

        context = data["context"] if "context" in data else ""

        result = dict()

        result["items"] = list()

        for item in data["items"]:
            if context:
                item["context"] = context + ("\n" + item["context"]) if "context" in item else ""

            res_item = {
                "expected": item["expected"],
                "actual": item["actual"]
            }

            if "context" in item:
                res_item["context"] = item["context"]

            try:
                res = self.evaluate(item, symbols=symbols)
                for symbol in res:
                    res_item[symbol] = res[symbol]
            except Exception as e:
                res_item["error"] = res

            result["items"].append(res_item)

        return result

    def evaluate_dataset(self, data: pd.DataFrame, symbols: list = SYMBOLS, context: str = '') -> pd.DataFrame:
        """

            Evaluates a whole pandas dataset.

        :param data: a dataframe with string columns 'expected' and 'actual' and optionally 'context'
        :param symbols: the list of symbols to evaluate
        :param context: the general context to be preceded to the context of each row
        :return: the result dataset with same index as the input dataset and columns:
        - 'expected': str, same as in input dataset
        - 'actual': str, same as in input dataset
        - 'context': str, same as in input dataset if exists otherwise the context variable is used
        - 'score_[sym]': float, the evaluated score value for every given symbol
        - 'reason_[sym]': json, the reasoning for every given symbol. a json encoded dictionary
        - 'errors': str, the list of errors during evaluation or None if no error happened
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
                res = self.evaluate({
                    "expected": row.expected,
                    "actual": row.actual,
                    "context": context + ("\n" + row.context if "context" in row else "")
                }, symbols)
                for symbol in res:
                    scores[symbol].append(res[symbol]['score'])
                    reasons[symbol].append(res[symbol]['reasoning'])
                errors.append(None)
            except Exception as e:
                for symbol in symbols:
                    scores[symbol].append(float('nan'))
                    reasons[symbol].append('')
                errors.append(e)

        result = {
            'expected': data['expected'],
            'actual': data['actual'],
            'context': data['context'] if 'context' in data.columns else context
        }

        for symbol in symbols:
            result[f'score_{symbol[:3]}'] = scores[symbol]

        for symbol in symbols:
            result[f'reason_{symbol[:3]}'] = reasons[symbol]

        result['error'] = errors

        return pd.DataFrame(data=result, index=data.index)

