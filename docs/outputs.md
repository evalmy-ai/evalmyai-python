# evalmy.ai backend  output format definition

## SYMBOLS = "contradiction"

```json
{
  "contradiction": {
    "score": "1.00 # float, 0.0 - 1.0, two decimal digits",
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
    "f1-score": "1.00 # float, 0.0 - 1.0, two decimal digits",
    "correctness": "1.00 # float, 0.0 - 1.0, two decimal digits",
    "completeness": "1.00 # float, 0.0 - 1.0, two decimal digits",
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
    "c3-score": "1.00 # float, 0.0 - 1.0, two decimal digits",
    "contradiction": {
      //..., see contradiction
    },
    "f1": {
      //..., see f1
    }
  }
}
```

