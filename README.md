# EVALMY.AI

Python client library for [EVALMY.AI](https://evalmy.ai), a public 
service for evaluating GPT answers based on semantics.

This service enables cost-effective, reliable, and 
consistent automated testing of GenAI solutions like 
RAGs and others. 

Using EVALMY.AI, you can accelerate your development 
process, reduce testing costs and enhance the reliability 
of your AI applications.

## Example

You are developing a RAG (Retrieval-Augmented Generation) 
to answer simple geographical questions. It's essential to 
test its performance both during development and after 
release to ensure the model maintains its accuracy. For 
this purpose, you create a set of test questions along 
with their respective correct answers.

```
1. What is the capital of France?               --> Paris
2. What are three longest rivers in the world?  --> Nile, Amazon, Yanktze
3. Which continent is the second smallest?      --> Europe
```

Your RAG provides following answers:

```
1. The capital of France is Paris.
2. Nile, Mississippi and Amazon.
3. The second smallest continent in the world is Australia.
```

Pretty well but not yet perfect. 

Reading through long sets of AI-generated answers can become 
tedious and monotonous, especially if the test set remains 
unchanged. This costs time and can lead to people making errors.

Fortunately, AI can handle the task for us. With the help of 
EVALMY.AI, simply send us the questions along with the expected 
and actual answers, and you'll receive the results effortlessly.

```
CONTRADICTIONS IN TEXTS:
1. Score: 1.0, 
Reasoning: "Both texts identify the capital of France correctly."

2. Score 0.5,
Severity: Large
Reasoning: "Different rivers listed as the three longest." 

3. Score 0.0, 
Severity: Critical
Reasoning: Different continents identified as the second smallest.

```


## Instalation

The evalmyai requires python 3.8 or higher.

```shell
python -m pip install evalmyai 
```

## Simple usage

```python
from evalmyai import Evaluator

data = {
    "expected": "Jane is twelve.",
    "actual": "Jane is 12 yrs, 7 mths and 3 days old."
}

ev = Evaluator(...) # see authentication later

result = ev.evaluate(data)

print(result['contradictions'])
```

The result of the evaluation is as follows:

```json
{
    "score": 1.0,
    "reasoning": {
        "statements": [
            {
                "reasoning": "The statement from <TEXT 1> 'Jane is twelve' provides a general age for Jane, while <TEXT 2> 'Jane is 12 yrs, 7 mths and 3 days old' provides a more precise age. There is no contradiction between the two statements, as the second text simply provides more detail on Jane's age, but does not conflict with the first text's assertion that she is twelve years old. The criterion for severity in this context could be based on the impact of the age description on understanding Jane's age. Since both statements agree on Jane being twelve, the severity of the difference in description is negligible.",
                "summary": "Slight difference in the description of Jane's age.",
                "severity": "negligible"
            }
        ]
    }
}
```

## Authentication

First, you need your EVALMY.AI service token, which you can get [here](https://evalmy.ai).

The service runs on your own instance of GPT, either in Azure or directly on an OpenAI endpoint you provide.

Due to capacity limits per organization, we cannot provide an GPT endpoint directly.

### Azure 

If you use an Azure endpoint, the configuration should look like this:

```python
token = "YOUR_EVALMYAI_TOKEN"

auth_azure = {
    "api_key": "cd0...101",
    "azure_endpoint": "https://...azure.com/",
    "api_version": "2023-07-01-preview",
    "azure_deployment": "...",
}

ev = Evaluator(auth_azure, token)
```

### OpenAI 

In case you use OpenAI endpoint, the configuration should look like this:

```python
token = "YOUR_EVALMYAI_TOKEN"

auth_open_ai = {
    "api_key": "...",
    "model": "gpt-4o" # select your model, we strongly recommend GPT-4.
}

ev = Evaluator(auth_open_ai, token)
```

The EVLAMY.AI tutorial with practical exmaples can be found [here](https://datascience.profinitservices.cz/evalmyai/evalmyai-client/).


