---
# DAH Labs model card template (rule ML-004). Copy to MODEL_CARD.md, and use it as the README.md
# of the model repository on Hugging Face Hub. The metadata below is read by the Hub.
# Replace every TODO marker; delete the lines that do not apply.
license: apache-2.0 # TODO: license of the weights (FILE-003)
language:
  - fr # TODO: ISO 639-1 codes, for example fr, en, wo, yo, sw
library_name: transformers # TODO
pipeline_tag: text-classification # TODO
base_model: TODO/base-model
datasets:
  - DAH-Projects-and-Innovations/TODO-dataset
metrics:
  - f1 # TODO
tags:
  - dah-labs
---

# TODO model name

One sentence: what the model does, for whom.

- **Developed by:** DAH Labs, Data Afrique Hub
- **Version:** TODO (Git tag `vX.Y.Z` of the training repository, and Hub revision)
- **Code:** <https://github.com/DAH-Projects-and-Innovations/TODO>
- **License:** TODO
- **Contact:** TODO (public contact address of the team, never a personal address)

## Intended use

- **Primary use:** TODO
- **Users:** TODO
- **Out of scope:** TODO (uses that the model must not be used for, for example medical or legal decisions without human review)

## Training data

- Dataset(s), version and link to their dataset card: TODO
- Languages and countries covered, and their share of the data: TODO
- Pre-processing: TODO

## Training procedure

- Base model and fine-tuning method: TODO
- Hyperparameters: link to the versioned configuration file (`configs/TODO.yaml`)
- Hardware and duration: TODO (for example "1 × T4, 3 h on a free notebook service")
- Seed(s): TODO

## Evaluation

- Test set: TODO (never used for training or tuning)
- Baseline: TODO

| Metric | Overall | TODO subgroup (language, country) | TODO subgroup |
|---|---|---|---|
| TODO | | | |

## Limitations and risks

- Known failure cases: TODO
- Languages, dialects or groups where the model is weaker: TODO
- Biases found during evaluation: TODO

## How to use

```python
# TODO: minimal working example
```

## Citation

```bibtex
TODO (or link to CITATION.cff)
```
