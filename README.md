# EVALMY.AI

Python client library for [EVALMY.AI](https://evalmy.ai), a public 
service for evaluating GPT answers based on semantics.

This service enables cost-effective, reliable, and 
consistent automated testing of GenAI solutions like 
RAGs and others. 

Using EVALMY.AI, you can accelerate your development 
process, reduce testing costs and enhance the reliability 
of your AI applications.

### Example

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

ev = Evaluator(auth_azure, token)
```

## More Complex Usage

### Context

You can specify the context of the comparison, such as what 
matters to you and what should be ignored.

To do this, simply add the context into the input data 
structure.

```python
data = {
    "expected": "There are three apples, seven oranges, and one banana in the basket.",
    "actual":   "In the basket there are thee apples, and four pears.",
    "context":  "I am interested in the apples only, ignore all the other fruits."
}
```

The result without any context:

```json 
{
  "score": 0.5,
  "reasoning": {
    "statements": [
      {
        "reasoning": "The statement from <TEXT 1> lists 'three apples, seven oranges, and one banana' as the contents of the basket. In contrast, <TEXT 2> mentions 'three apples, and four pears' in the basket. There is a direct contradiction regarding the types of fruits and their quantities. <TEXT 1> does not mention pears at all, while <TEXT 2> does not mention the seven oranges and one banana from <TEXT 1>. This is a large contradiction because it involves a significant difference in the facts presented about the basket's contents, which changes the overall context or story of what is in the basket.", 
        "summary": "Different fruits and quantities in the basket.", 
        "severity": "large"
      }
    ]
  }
}
```

The result with context applied:

```json 
{
  "score": 1.0,
  "reasoning": {
    "statements": [
      {
        "reasoning": "Both <TEXT 1> and <TEXT 2> state that there are three apples in the basket. Since the context specifies that only information about apples should be considered, the mention of other fruits in both texts is irrelevant. Therefore, there is no contradiction between the texts concerning the number of apples.", 
        "summary": "No contradiction regarding apples.", 
        "severity": "negligible"
      }
    ]
  }
}
```

### Batch Evaluation

In real-world testing, it is practical to define a complete 
test set containing multiple questions and answers. The 
Evaluator class includes several convenient methods to 
handle this for you.

#### Simple python lists

```python
data = [
   {
      "expected": "Sunny.",
      "actual": "Raining.",
   },
   {
      "expected": "Cloudy.",
      "actual": "Storm.",
   }
]

results, errors = ev.evaluate_batch(data, context='Compare precipitation only. Ignore other weather traits.')
```

The *evaluate_batch* method returns a tuple of lists:

- **results**: A list of evaluation results, with None values if an error occurs.
- **errors**: A list of evaluation errors, with None values if no error occurs.

#### Pandas dataset

```python
import pandas as pd

df = pd.DataFrame({
    "expected": ["We live in a best of worlds!"] * 3,
    "actual": ["Life is great!", "Life has its ups and downs!", "Life is miserable!"]
}, index=["optimist", "realist", "pessimist"])

ev.evaluate_dataset(data)
```

he *evaluate_dataset* method returns a Pandas DataFrame 
indexed by the same values as the input, with the following 
columns:

- **expected**: original expected values
- **actual**: original actual values
- **context**: context used for evaluation
- **score_con**: contradiction score
- **reason_con**: contradiction reasoning
- **error**: evaluation error or None

#### Whole test case defined in json

It might be convenient to define the entire test scenario using a JSON file.

```json
{
  "name": "A sample rag testcase",

  "context": "Evaluate the answers to the school test. Be careful to factual clarity and particular numbers. Formulation and style is not relevant.",

  "scoring": {
    "contradictions": {
      "name": "linear",
      "params": {
        "weights": {
          "critical": 1,
          "large": 0.5,
          "small": 0.1,
          "negligible": 0
        }
      }
    }
  },

  "items": [
    {
      "context": "Question: What is the capital of France?",
      "expected": "The capital of France is Paris",
      "actual": "Paris."
    },
    {
      "context": "Question: How long is Great Wall of China?",
      "expected": "GWCh is more than 21 thousand kilometers long.",
      "actual": "It is 13 thousand miles."
    },
    {
      "context": "Question: How long was hundred years war?",
      "expected": "116 years, 4 months, 3 weeks and 4 days.",
      "actual": "A hundred years."
    }
  ]
}
```

The scenario is evaluated by calling the *evaluate_test_case* method.

```python
with open('test_case_input.json') as fi:
    test_case = json.load(fi)

result = ev.evaluate_test_case(test_case=test_case)

with open('test_case_output.json', 'w') as fo:
    json.dump(result, fo, ensure_ascii=False, indent=4)
```

It is also possible to input the actual values directly into 
the *evaluate_test_case* method, rather than including them 
in the test scenario definition.

```python
values = ["Paris.", "It is 13 thousand miles.", "A hundred years."]
result = ev.evaluate_test_case(test_case=test_case, actual_values=values)
```

### Scoring Parameters Definition

Currently, *contradiction scoring* is implemented. Precision, recall, and F1 scores are in development.

#### Contradiction Scoring

The goal is to find, identify, and classify all contradictions in the compared texts.

**Score: 1.0** means no contradiction in the texts.

Every contradiction found in the texts is classified into one of four categories:

**1. Critical** — Significantly changes the meaning of the text.
  
  - *John is older than Jane.* vs. *Jane is older than John.*

**2. Large** — Major shift in the meaning of the text.

  - *VW Golf is faster and cheaper than Toyota Corolla.* vs. *VW Golf is faster but more expensive than Toyota Corolla.*
  
**3. Small** — Minor shift in the meaning of the text.

  - *I bought three books, seven envelopes, and a blue pen.* vs. *I bought three books, seven envelopes, and a blue pencil.*

**4. Negligible** — Changes in text with minimal effect on the overall meaning.

  - *Da Vinci's is a popular Italian restaurant serving pizza, pasta, and wine.* vs. *Da Vinci's is a famous Italian restaurant with great Italian foods and drinks.*

The classification of contradictions can be altered by the context (see the Context section).

For every contradiction found in the text, a penalty is applied. The penalty is defined in the scoring criteria with following default values:
```python
DEFAULT_SCORING = {
    "contradictions": {
        "name": "linear",
        "params": {
            "weights": {
                "critical": 1,
                "large": 0.5,
                "small": 0.1,
                "negligible": 0
            }
        }
    }
}
```

Thus, score = 0 is achieved by just a single critical 
contradiction, two large contradictions, or ten small 
ones. Negligible contradictions do not affect the score 
at all.