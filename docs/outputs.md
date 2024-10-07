# evalmy.ai backend  output format definition

## SYMBOLS = "contradiction"

```json
{
  "contradiction": {
    "scores": {
      "score": "1.00 # float, 0.0 - 1.0, two decimal digits"
    }, 
    "reasoning": {
      "statements": [
        {
          "severity": "str, one of critical, large, small, negligible",
          "reasoning": "str",
          "summary": "str"
        }
      ]
    }
  }
}
```

## SYMBOLS = "f1"

```json
{
  "f1": {
    "scores": {
      "f1": "1.00 # float, 0.0 - 1.0, two decimal digits",
      "correctness": "1.00 # float, 0.0 - 1.0, two decimal digits",
      "completeness": "1.00 # float, 0.0 - 1.0, two decimal digits",
    },
    "reasoning": {
      "statements": [
        {
          "occurrence": "str, one of both, 1, 2",
          "severity": "str, one of critical, large, small, negligible",
          "reasoning": "str",
          "summary": "str"
        }
      ]
    }
  }
}
```

## SYMBOL = "c3-score"

```json
{
  "c3-score": {
    "scores": {
      "c3": "1.00 # float, 0.0 - 1.0, two decimal digits",
      "f1": "1.00 # float, 0.0 - 1.0, two decimal digits",
      "correctness": "1.00 # float, 0.0 - 1.0, two decimal digits",
      "completeness": "1.00 # float, 0.0 - 1.0, two decimal digits",
    },
  }
}
```

