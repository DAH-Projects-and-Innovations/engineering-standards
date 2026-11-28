# ML and research

## TL;DR

- **Data and model weights never go into Git.** `data/README.md` says how to get them, with checksums. Publish them on **Hugging Face Hub** (organization account) or **Zenodo**.
- Every run is **reproducible**: one versioned config file, a fixed seed, `uv.lock`, and the Git commit recorded with the results.
- **Notebooks are for exploration.** Outputs are stripped; reusable code moves into `src/`.
- Every published model has a **model card**; every published dataset has a **dataset card**: sources, license, personal data, languages, limits.
- Evaluation uses a **held-out test set**, a versioned harness in `eval/`, a baseline, and results **per language or country** when the data covers several.
- Paid API calls (LLMs, embeddings) have a **budget**, a cache and a dry run on a small sample.

Layout: [REPO-004](repository-structure.md#repo-004-a-research-or-ml-repository-follows-the-research-layout). Templates: [model card](../../templates/ml/model-card.md), [dataset card](../../templates/ml/dataset-card.md), [CITATION.cff](../../templates/docs/CITATION.cff).

## Where to store data and models for free

| What | Where | Notes |
|---|---|---|
| Datasets and model weights to publish | **Hugging Face Hub**, `DAH-Projects-and-Innovations` organization | Versioned Git repositories with large-file support; tag each revision with the version of the code. ⚠️ To verify: current storage limits for organizations on the free plan. |
| Archive with a DOI, for a paper | **Zenodo** | Permanent DOI for each version; can archive GitHub releases automatically. ⚠️ To verify: current size limit per record. |
| Small files attached to a release | **GitHub Releases** | Assets up to 2 GiB per file; not for data that changes often. |
| Work in progress, private data | Storage of the partner that owns the data | Never a personal drive shared by link. |
| Experiment results | `experiments/` in the repository | Small text files only: config, metrics, commit (see [ML-007](#ml-007-every-run-records-its-config-commit-data-version-and-metrics)). |

## Rules

### ML-001: Data and models are outside Git, and `data/README.md` says how to get them

**MUST** · Level 1 · Verified by: `check-added-large-files` hook (automatic); `data/README.md` review (manual)

- `data/`, `models/` and `outputs/` are in `.gitignore`, except `data/README.md` ([REPO-006](repository-structure.md#repo-006-generated-files-data-and-models-are-not-committed)).
- `data/README.md` lists each file or dataset: source, version, license, size, SHA-256 checksum, and the command that downloads or builds it (`uv run python -m my_research.data.download`).
- The download script checks the checksums.

**Why:** a new contributor can rebuild the exact data of a result. Git stays small and fast on slow connections.

### ML-002: Every run is reproducible from a config file, a seed and the lock file

**MUST** · Level 1 · Verified by: code review (manual); re-run of a reported result (manual)

- One YAML file per experiment in `configs/`. All hyperparameters and paths come from it; nothing is changed in the code between runs.
- The seed is in the config and is applied to `random`, `numpy` and the framework (`torch.manual_seed`, `transformers.set_seed`).
- The environment is `uv.lock` (Python) and the base image or the notebook service used for GPU runs.
- A run refuses to start when the working tree has uncommitted changes, or records the diff with the results.

### ML-003: Notebooks are for exploration; outputs are stripped and reusable code moves to `src/`

**MUST** · Level 1 · Verified by: `nbstripout` hook (automatic); code review (manual)

- Notebooks live in `notebooks/` and are named `NN-initials-topic.ipynb` (`03-ak-error-analysis.ipynb`).
- A function used by two notebooks, or by a script, moves to `src/<package>/` with tests.
- Results that matter are produced by scripts from `configs/`, not by notebook cells run in an unknown order.
- Enable the `nbstripout` hook ([HOOK-009](git-hooks.md#hook-009-notebook-outputs-are-stripped-before-commit)) of the [pre-commit templates](../../templates/pre-commit/python.yaml).

### ML-004: Every published model has a model card

**MUST** · Level 2 · Verified by: Hub repository review (manual)

Use the [model card template](../../templates/ml/model-card.md) as `MODEL_CARD.md` and as the `README.md` of the Hub repository. It covers intended use and out-of-scope uses, training data, training procedure, evaluation with subgroups, limitations and risks, and how to use and cite the model.

**Why:** a model without a card is used for the wrong things. Reviewers and partners judge a lab by its cards.

### ML-005: Every published dataset has a dataset card, with sources, license and personal data

**MUST** · Level 2 · Verified by: Hub repository review (manual)

Use the [dataset card template](../../templates/ml/dataset-card.md). It states the license of each source and the permission to reuse it, the collection and annotation process, the **personal data** contained and the consent obtained, the languages and countries covered, and the known biases.

Personal data follows [SEC-010](security.md#sec-010-no-real-personal-data-in-the-repository-tests-or-fixtures), which lists the data protection laws of several African countries. When in doubt, do not publish: ask the maintainers.

### ML-006: Evaluation uses a held-out test set, a versioned harness and a baseline

**MUST** · Level 1 · Verified by: code review (manual)

- The test split is fixed, versioned, and **never** used for training, early stopping or hyperparameter tuning (use the validation split).
- The evaluation code is in `eval/`, tested, and gives the same numbers for the same predictions.
- Every result is compared with a baseline (a simple model, the previous version, or a published result) on the same test set.
- Report the metrics that matter for the task (for example macro F1 for unbalanced classes), with the number of examples.

### ML-007: Every run records its config, commit, data version and metrics

**SHOULD** · Level 2 · Verified by: `experiments/` review (manual)

For each run worth keeping, `experiments/<date>-<name>/` contains the config, the Git commit, the data version (checksums or Hub revision), the metrics as JSON, and a short `README.md` with the conclusion. A local tracking tool (for example MLflow with a file store) MAY be used; its files stay out of Git, and the summary goes to `experiments/`.

**Why:** "the model of last month was better" can be checked in five minutes.

### ML-008: Paid API calls have a budget, a cache and a dry run

**MUST** · Level 1 · Verified by: code review (manual)

- Before a full run, run on a small sample (`--limit 20`) and estimate the cost from the number of tokens.
- Write the expected cost and the budget in the PR or the experiment `README.md`. Above the budget agreed with the maintainers, ask first.
- Cache the responses (by a hash of model + prompt + parameters), so that a re-run does not pay twice.
- Use `temperature=0` and record the model name and version for evaluation runs.
- API keys come from `.env` or GitHub secrets, never from the code or a notebook ([SEC-004](security.md#sec-004-no-secret-is-ever-committed-and-a-leaked-secret-is-revoked-first)).

### ML-009: Results are reported per language and country when the data covers several

**SHOULD** · Level 2 · Verified by: model card review (manual)

An average can hide a model that works for French and fails for Wolof. When the data covers several languages, countries or other relevant groups, the evaluation table has a column for each, with its number of examples.

**Why:** DAH Labs builds AI for African contexts; showing where a model is weak is part of the result.

### ML-010: Published models and datasets are versioned with the code

**SHOULD** · Level 2 · Verified by: Hub repository tags (manual)

The Hub revision (a tag) has the same version as the Git tag of the code that produced it (`v1.2.0`). Users load a fixed revision (`revision="v1.2.0"`), never only `main`.

### ML-011: GPU code is marked, and CI runs a small CPU smoke test

**MUST** · Level 1 · Verified by: pytest markers (automatic)

- Tests that need a GPU are marked `@pytest.mark.requires_gpu`; GitHub-hosted runners do not run them.
- CI runs the training and evaluation code on a tiny config (a few examples, one step, a tiny model) on CPU, so that a broken pipeline is found before a long GPU run.

### ML-012: Research outputs are citable

**SHOULD** · Level 3 · Verified by: `CITATION.cff` and Zenodo DOI (manual)

- `CITATION.cff` is at the root ([FILE-017](required-files.md#file-017-research-repositories-have-a-citationcff-file)).
- A paper or a report cites the exact version of the code and data (DOI from Zenodo, or Git tag and Hub revision).

## Checklist

- [ ] `data/`, `models/` and `outputs/` are ignored; `data/README.md` gives sources, licenses, checksums and the download command.
- [ ] Each experiment has a config file with a seed; results record the commit and the data version.
- [ ] Notebook outputs are stripped by `nbstripout`; shared code is in `src/` with tests.
- [ ] Published models and datasets have cards, and a revision tag that matches the code version.
- [ ] The test set is never used for tuning; results have a baseline and per-language columns.
- [ ] Paid API runs have a cost estimate, a cache and a dry run.
- [ ] GPU tests are marked `requires_gpu`; CI runs a tiny CPU smoke test.

---

*Last verified: 2026-11-14.*
