import json
from unittest import TestCase
import os

import pandas as pd

from src.evalmyai.evalmyai import Evaluator

from dotenv import load_dotenv
load_dotenv(dotenv_path='../../.env')

auth = {
    "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
    "azure_endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
    "api_version": os.getenv("AZURE_OPENAI_API_VERSION"),
    "azure_deployment": os.getenv("AZURE_DEPLOYMENT_NAME")
}

token = os.getenv("EVALMYAI_TOKEN")


class TestEvaluator(TestCase):

    evaluator = Evaluator(auth, token)

    def test_set_scoring(self):

        wrong_scoring = {
            "name": "linear",
            "params": {
                "weights": {
                    "critical": 1,
                    "small": 0.1,
                    "negligible": 0
                }
            }
        }

        correct_scoring = {
            "name": "linear",
            "params": {
                "weights": {
                    "critical": 1,
                    "large" : 0.5,
                    "small": 0.1,
                    "negligible": 0
                }
            }
        }

        self.evaluator.set_scoring('contradictions', correct_scoring)

        self.assertRaises(ValueError, self.evaluator.set_scoring, 'contrad ictions', correct_scoring)
        self.assertRaises(ValueError, self.evaluator.set_scoring, 'contradictions', wrong_scoring)

    def test_evaluate(self):
        data = {
            "expected": "Nehoří!",
            "actual": "Hoří!",
            "context": ""
        }

        result = self.evaluator.evaluate(data)

        self.assertLess(result['contradictions']['score'], 0.1)

    def test_evaluate_batch(self):

        data = [
            {
                "expected": "Nehoří!",
                "actual": "Hoří!",
            },
            {
                "expected": "Nehoří!",
                "actual": "Hoří trochu!",
            },
            {
                "expected": "Nehoří!",
                "actual": "Nehoří vůbec!",
            },
            {
                "expected": "Nehoří!",
            }
        ]

        results, errors = self.evaluator.evaluate_batch(data)

        print(results)
        print(errors)

        self.assertLess(results[0]['contradictions']['score'], 0.1)
        self.assertLess(results[1]['contradictions']['score'], 0.5)
        self.assertGreater(results[2]['contradictions']['score'], 0.5)
        self.assertEqual(len([e for e in errors if e]), 1)

    def test_evaluate_dataset(self):

        data = pd.DataFrame(data={
            "expected": ["Nehoří!"]*4,
            "actual": ["Hoří!", "Hoří trochu!", "Nehoří vůbec!", None]
        }, index=['wrong', 'wrongish', 'correct', 'error'])

        result = self.evaluator.evaluate_dataset(data)

        self.assertEqual((4, 6), result.shape)
        self.assertEqual(True, result.index.equals(data.index))
        self.assertEqual(1, sum(result["error"].notnull()))
        self.assertLess(result.loc['wrong', 'score_con'], 0.1)
        self.assertLess(result.loc['wrongish', 'score_con'], 0.1)
        self.assertGreater(result.loc['correct', 'score_con'], 0.5)

        print(result)

    def test_evaluate_test_case(self):
        data = {
            "items": [
                {
                    "context": "Question: What are three longest rivers in the world?",
                    "expected": "Nile, Amazon, Yanktze",
                    "actual": "Nile, Mississippi and Jordan."
                },
                {
                    "context": "Question: Which continent is the second smallest?",
                    "expected": "Europe",
                    "actual": "The second smallest continent in the world is Australia."
                }
            ]
        }

        result = self.evaluator.evaluate_test_case(data)

        print(json.dumps(result, ensure_ascii=False, indent=4))


