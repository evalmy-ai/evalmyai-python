# evalmy.ai

Python client library for [evalmy.ai](https://evalmy.ai).

## Instalation

The evalmyai requires python 3.11 or higher.

```shell
python -m pip install evalmyai 
```

## Simple usage

```python
from src.evalmyai import Evaluator

data = {
    "expected": "Jane is twelve.",
    "actual": "Jane is 12 yrs, 7 mths and 3 days old."
}

evaluator = Evaluator(...)

result = evaluator.evaluate(data)

print(result['contradictions'])
```

The result of the evaluation is as follows:

```json

```

