

def check_structure(struct, obj, path=""):
    location = f" at '{path}'" if path else ""
    if isinstance(struct, dict) and isinstance(obj, dict):
        for k in struct:
            if k not in obj:
                return False, f"field '{k}' expected, but not found{location}."
            res = check_structure(struct[k], obj[k], f'{path}.{k}')
            if not res[0]:
                return False, res[1]
    elif isinstance(struct, list) and isinstance(obj, list):
        for i, v in enumerate(obj):
            res = check_structure(struct[0], v, f'{path}[{i}]')
            if not res[0]:
                return False, res[1]
    elif not isinstance(obj, type(struct)) and not isinstance(struct, type(obj)):
        return False, f"'{type(struct).__name__}' expected, but '{type(obj).__name__}' found{location}."
    return True, path


STRUCT_SINGLE_INPUT_DATA = {
    "expected": "string",
    "actual": "string",
    "context": "string"
}


STRUCT_SINGLE_OUTPUT_DATA = {
    "contradictions": {
        "score": 1.0,
        "reasoning": {
            "statements": [
                {
                    "reasoning": "string",
                    "summary": "string",
                    "severity": "string"
                }
            ]
        }
    }
}

STRUCT_TEST_CASE_DATA = {
    "items": [
        {
            "expected": "string",
        }
    ]
}

def validate_dict(correct: dict, actual) -> bool:
    """
        Test proper format of a dictionary.
        :param correct: correct dictionary
        :param actual: actual dictionary
        :return: true if valid, false otherwise
    """
    return check_structure(correct, actual)


def validate_single_input_data(data: dict) -> bool:
    """
        Test proper format of input data.
        :param data: the input data
        :return: true if valid, false otherwise
    """
    return check_structure(STRUCT_SINGLE_INPUT_DATA, data)


def validate_single_output_score(score: dict) -> bool:
    """
        Test proper format of output data.
        :param data: the output score data
        :return: true if valid, false otherwise
    """
    return check_structure(STRUCT_SINGLE_OUTPUT_DATA, score)


def validate_test_case_data(test_case: dict) -> bool:
    return check_structure(STRUCT_TEST_CASE_DATA, test_case)
