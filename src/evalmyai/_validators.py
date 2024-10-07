def check_structure(struct, obj, path=""):
    """Recursively checks if the structure of `obj` matches the structure of `struct`.

    Args:
        struct: The structure to validate against.
        obj: The object to be checked.
        path: The current location in the structure (used for generating error messages).

    Returns:
        Tuple[bool, str]: A tuple where the first element is a boolean indicating whether
        the structure matches, and the second element is a string containing the error
        message if the structures don't match.
    """
    location = f" at '{path}'" if path else ""
    if isinstance(struct, dict) and isinstance(obj, dict):
        for k in struct:
            if k not in obj:
                return False, f"field '{k}' expected, but not found{location}."
            res = check_structure(struct[k], obj[k], f"{path}.{k}")
            if not res[0]:
                return False, res[1]
    elif isinstance(struct, list) and isinstance(obj, list):
        for i, v in enumerate(obj):
            res = check_structure(struct[0], v, f"{path}[{i}]")
            if not res[0]:
                return False, res[1]
    elif not isinstance(obj, type(struct)) and not isinstance(struct, type(obj)):
        return (
            False,
            f"'{type(struct).__name__}' expected, but '{type(obj).__name__}' found{location}.",
        )
    return True, path


STRUCT_SINGLE_INPUT_DATA = {
    "expected": "string",
    "actual": "string",
    "context": "string",
}


STRUCT_SINGLE_OUTPUT_DATA = {
    "contradictions": {
        "scores": {"score": 1.0},
        "reasoning": {
            "statements": [
                {"reasoning": "string", "summary": "string", "severity": "string"}
            ]
        },
    },
    "missing_facts": {
        "scores": {"score": 1.0},
        "reasoning": {
            "statements": [
                {"reasoning": "string", "summary": "string", "severity": "string"}
            ]
        },
    },
    "f1": {
        "scores": {"f1": 1.00, "correctness": 1.00, "completeness": 1.00},
        "reasoning": {
            "statements": [
                {"reasoning": "string", "summary": "string", "severity": "string"}
            ]
        },
    },
}

STRUCT_TEST_CASE_DATA = {
    "items": [
        {
            "expected": "string",
        }
    ]
}


def validate_dict(correct: dict, actual) -> bool:
    """Validates that a dictionary matches the expected structure.

    Args:
        correct (dict): The correct dictionary structure to validate against.
        actual: The actual dictionary to be checked.

    Returns:
        bool: True if the actual dictionary matches the correct structure, False otherwise.
    """
    return check_structure(correct, actual)


def validate_single_input_data(data: dict) -> bool:
    """Validates that the input data matches the expected structure.

    Args:
        data (dict): The input data to be checked.

    Returns:
        bool: True if the input data is valid, False otherwise.
    """
    return check_structure(STRUCT_SINGLE_INPUT_DATA, data)


def validate_single_output_score(score: dict) -> bool:
    """Validates that the output score data matches the expected structure.

    Args:
        score (dict): The output score data to be checked.

    Returns:
        bool: True if the output score data is valid, False otherwise.
    """

    for symbol in score.keys():
        if symbol not in STRUCT_SINGLE_OUTPUT_DATA.keys():
            return False, f"'{symbol}' is not valid symbol."
        else:
            return check_structure(STRUCT_SINGLE_OUTPUT_DATA[symbol], score[symbol])


def validate_test_case_data(test_case: dict) -> bool:
    """Validates that the test case data matches the expected structure.

    Args:
        test_case (dict): The test case data to be checked.

    Returns:
        bool: True if the test case data is valid, False otherwise.
    """
    return check_structure(STRUCT_TEST_CASE_DATA, test_case)
