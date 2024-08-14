from utils import init_evaluator

evaluator = init_evaluator()

print("--- simple example ---")

data = {
    "expected": "There are three apples, seven oranges, and one banana in the basket.",
    "actual":   "In the basket there are thee apples, and four pears."
}

print(data)

result = evaluator.evaluate(data=data)["contradictions"]

print(f"Score: {result['score']}")

print(f"Reasoning: {result['reasoning']}")

print("--- contextual example ---")

data = {
    "context":  "I am interested in the apples only, ignore all the other fruits.",
    "expected": "There are three apples, seven oranges, and one banana in the basket.",
    "actual":   "In the basket there are thee apples, and four pears."
}

print(data)

result = evaluator.evaluate(data=data)["contradictions"]

print(f"Score: {result['score']}")

print(f"Reasoning: {result['reasoning']}")
