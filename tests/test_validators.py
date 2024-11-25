from unittest import TestCase
from evalmyai._validators import (
    validate_single_input_data,
    validate_single_output_score,
)


class Test(TestCase):
    correct_data = {"expected": "one", "actual": "1", "context": "numerical equality"}

    wrong_data_1 = {"expected": "one", "actual": 1, "context": "numerical equality"}

    wrong_data_2 = {"expected": "one", "context": "numerical equality"}

    def test_validate_single_input_data(self):
        res = validate_single_input_data(Test.correct_data)
        self.assertEqual(True, res[0])
        print(res[1])
        res = validate_single_input_data(Test.wrong_data_1)
        self.assertEqual(False, res[0])
        print(res[1])
        res = validate_single_input_data(Test.wrong_data_2)
        self.assertEqual(False, res[0])
        print(res[1])

    correct_scoring = {
        "contradictions": {
            "scores": {"score": 1.0},
            "reasoning": {
                "statements": [
                    {"reasoning": "seems ok", "summary": "np", "severity": "negligible"}
                ]
            },
        }
    }

    wrong_scoring_1 = {
        "contradictions": {
            "scores": {"score": "0"},
            "reasoning": {
                "statements": [
                    {"reasoning": "seems wrong", "summary": "bad", "severity": "major"}
                ]
            },
        }
    }

    wrong_scoring_2 = {
        "contradictions": {
            "scores": {"score": 1.0},
            "reasoning": {
                "statements": [
                    {"reasoning": "seems wrong", "summary": "bad", "severity": "minor"},
                    {"reasoning": "seems wrong", "summary": "bad", "severity": 17},
                ]
            },
        }
    }

    def test_validate_single_output_score(self):
        res = validate_single_output_score(Test.correct_scoring)
        print(res[1])
        self.assertEqual(True, res[0])
        res = validate_single_output_score(Test.wrong_scoring_1)
        print(res[1])
        self.assertEqual(False, res[0])
        res = validate_single_output_score(Test.wrong_scoring_2)
        print(res[1])
        self.assertEqual(False, res[0])
