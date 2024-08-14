from utils import init_evaluator
import json

evaluator = init_evaluator()

data = {
    "expected": "Jane is twelve.",
    "actual":   "Jane is 12 yrs, 7 mths and 3 days old."
}

result = evaluator.evaluate(data=data)

res_con = result["contradictions"]

print(f"Score: {res_con['score']}")

print(f"Reasoning: {res_con['reasoning']}")

print(json.dumps(result["contradictions"], indent=4))
