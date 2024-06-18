# evalmy.ai

Python client library for [evalmy.ai](https://evalmy.ai).

## Instalation

The evalmyai requires python 3.11 or higher.

```shell
python -m pip install evalmyai-python 
```

## Simple usage

```python
from evalmyai import Evaluator

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

## Contributing

First create the Python environment.

```sh
python -m venv ".venv"
source ./venv/bin/activate
python -m pip install -r "requirements.txt" -e .
```
