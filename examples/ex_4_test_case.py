import json

from utils import init_evaluator

evaluator = init_evaluator()

with open('test_case_input.json') as fi:
    test_case = json.load(fi)

values = ["Paris.", "It is 13 thousand miles.", "A hundred years."]

result = evaluator.evaluate_test_case(test_case=test_case, actual_values=values)

with open('test_case_output.json', 'w') as fo:
    json.dump(result, fo, ensure_ascii=False, indent=4)

