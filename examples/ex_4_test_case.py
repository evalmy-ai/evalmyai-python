import json

from utils import init_evaluator

evaluator = init_evaluator()

with open('test_case_input.json') as fi:
    data = json.load(fi)

result = evaluator.evaluate_test_case(data=data)

with open('test_case_output.json', 'w') as fo:
    json.dump(result, fo, ensure_ascii=False, indent=4)

