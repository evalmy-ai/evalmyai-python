import pandas as pd
from utils import init_evaluator

evaluator = init_evaluator()

index = ["optimist", "realist", "pessimist"]

expected = ["We live in a best of worlds!"] * 3

actual = ["Life is great!", "Life has its ups and downs!", "Life is miserable!"]

dataset = pd.DataFrame({"expected": expected, "actual": actual}, index=index)

print(dataset)

result = evaluator.evaluate_dataset(dataset)

print(result[['score_con', 'reason_con']])
print(result['reason_con'])
print(result[['error']])
