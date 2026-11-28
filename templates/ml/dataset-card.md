---
# DAH Labs dataset card template (rule ML-005). Copy to DATASET_CARD.md, and use it as the
# README.md of the dataset repository on Hugging Face Hub. The metadata below is read by the Hub.
# Replace every TODO marker; delete the lines that do not apply.
license: cc-by-4.0 # TODO: license of the data (FILE-003); it must respect the licenses of the sources
language:
  - fr # TODO: ISO 639-1 codes
pretty_name: TODO dataset name
task_categories:
  - text-classification # TODO
size_categories:
  - 1K<n<10K # TODO
tags:
  - dah-labs
---

# TODO dataset name

One sentence: what the data is, and what it is for.

- **Curated by:** DAH Labs, Data Afrique Hub
- **Version:** TODO (Git tag of the building code, and Hub revision)
- **Code that builds it:** <https://github.com/DAH-Projects-and-Innovations/TODO>
- **License:** TODO
- **Contact:** TODO (public contact address of the team)

## Content

- What one example contains (fields and types): TODO
- Splits and sizes:

| Split | Examples | Notes |
|---|---|---|
| train | TODO | |
| validation | TODO | |
| test | TODO | never used for training or tuning |

- Languages, countries and periods covered: TODO

## Sources and collection

- Sources, with their license and the permission to reuse them: TODO
- How the data was collected (scraping, partners, crowdsourcing) and when: TODO
- Annotation: who annotated, guidelines (link), agreement between annotators: TODO

## Personal data and consent

- Does the data contain personal data? TODO (yes / no). If yes: legal basis, consent, the laws of the countries concerned (see the security standard of DAH Labs), and the anonymization method.
- Sensitive content (health, religion, ethnicity, minors): TODO
- How a person can ask for the removal of their data: TODO

## Known limitations and biases

- Over- or under-represented groups, languages or regions: TODO
- Known label errors: TODO

## How to load

```python
from datasets import load_dataset

dataset = load_dataset("DAH-Projects-and-Innovations/TODO", revision="vX.Y.Z")
```

## Citation

```bibtex
TODO (or link to CITATION.cff)
```
