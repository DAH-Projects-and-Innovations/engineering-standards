# Repository structure

## TL;DR

- DAH Labs has three kinds of repositories: **service** (back end + front end), **Python library**, and **research / ML**.
- Each kind has a reference layout. Use it for new repositories; move existing ones towards it step by step.
- The root holds the standard files (see [Required files](required-files.md)) and one folder per deployable part.
- Documentation lives in `docs/`, never inside the source package.
- Data, models and build output are never committed.

## Rules

### REPO-001: The root holds standard files and one folder per part

**MUST** · Level 1 · Verified by: code review (manual); audit checklist (manual)

The root contains the [required files](required-files.md), `docs/`, and one folder per deployable part (`backend/`, `frontend/`) or the package layout. Scripts go in `scripts/`, examples in `examples/`. No loose files or folders such as `test.py`, `main_old.py`, `notes.txt` or `My Scripts/`.

### REPO-002: A service repository follows the service layout

**SHOULD** · Level 1 · Verified by: code review (manual)

This is the layout of baraza and RAG-DataAfriqueHub. The back-end layers are explained in [Architecture](architecture.md).

```text
my-service/
├── README.md  LICENSE  CONTRIBUTING.md  CODE_OF_CONDUCT.md  SECURITY.md  CHANGELOG.md
├── .editorconfig  .gitattributes  .gitignore  .env.example  .pre-commit-config.yaml
├── sonar-project.properties  release-please-config.json  .release-please-manifest.json
├── docker-compose.yml
├── .github/
│   ├── CODEOWNERS  dependabot.yml  pull_request_template.md
│   ├── ISSUE_TEMPLATE/
│   └── workflows/ci.yml
├── docs/
│   ├── architecture.md
│   └── adr/                       # Architecture Decision Records
├── backend/
│   ├── pyproject.toml  uv.lock  .python-version  Dockerfile  .dockerignore  README.md
│   ├── src/my_service/
│   │   ├── domain/                # entities and business rules, no framework
│   │   ├── application/           # use cases and ports (interfaces)
│   │   ├── infrastructure/        # adapters: LLM, vector store, database
│   │   └── interfaces/            # FastAPI routes, CLI, workers
│   ├── configs/                   # versioned YAML configuration, if any
│   ├── scripts/
│   └── tests/{unit,integration,e2e}/
├── frontend/
│   ├── package.json  pnpm-lock.yaml  .nvmrc  Dockerfile  README.md
│   └── src/
└── eval/                          # evaluation sets and harness, if any
```

### REPO-003: A Python library uses the `src/` layout

**MUST** · Level 1 · Verified by: code review (manual)

```text
my-library/
├── README.md  LICENSE  CONTRIBUTING.md  CODE_OF_CONDUCT.md  SECURITY.md  CHANGELOG.md
├── pyproject.toml  uv.lock  .python-version
├── src/my_library/
│   ├── __init__.py               # public API: what users import
│   ├── py.typed                  # the library ships type information
│   └── …
├── tests/{unit,integration}/
├── docs/
└── examples/
```

**Why:** with `src/`, tests import the installed package, so a packaging error is found before users find it.

### REPO-004: A research or ML repository follows the research layout

**SHOULD** · Level 1 · Verified by: code review (manual)

For a benchmark, a dataset or a model. Details are in [ML and research](ml-research.md).

```text
my-research/
├── README.md  LICENSE  CITATION.cff  CONTRIBUTING.md  CODE_OF_CONDUCT.md  SECURITY.md
├── pyproject.toml  uv.lock  .python-version
├── MODEL_CARD.md or DATASET_CARD.md
├── configs/                      # one YAML file per experiment, versioned
│   └── baseline.yaml
├── data/                         # ignored by Git, except data/README.md
│   └── README.md                 # how to download or build the data
├── notebooks/                    # exploration only, outputs stripped
│   └── 01-ak-explore-labels.ipynb
├── src/my_research/              # reusable code: loaders, models, metrics
├── eval/                         # evaluation harness, versioned
├── experiments/                  # results of runs: config + metrics, small text files
├── reports/                      # written results, figures
└── tests/
```

### REPO-005: Documentation lives in `docs/`, not in the source package

**MUST** · Level 1 · Verified by: code review (manual)

- ✅ `docs/retrieval.md`, `docs/api.md`
- ❌ `backend/src/docs/retrieval/TASK_DELIVERABLES.md`

Each top-level part MAY have a short `README.md` (`backend/README.md`) that explains how to run it.

### REPO-006: Generated files, data and models are not committed

**MUST** · Level 1 · Verified by: `check-added-large-files` pre-commit hook (automatic); `.gitignore` review (manual)

Never commit `dist/`, `build/`, `.venv/`, `node_modules/`, `coverage/`, model weights (`*.pt`, `*.safetensors`, `*.h5`), datasets, vector store files (`chroma_db/`) or PDF corpora. See [ML and research](ml-research.md) for free storage options.

The `check-added-large-files` hook blocks files larger than 500 KB. A real need for a larger file (for example a small test fixture) is discussed in the PR.

### REPO-007: Examples and notebooks are outside the package

**SHOULD** · Level 1 · Verified by: code review (manual)

- ✅ `examples/01_quickstart.ipynb`, `examples/retrieval_examples.py`
- ❌ `backend/src/examples/` (examples are installed with the package and checked by the package linters)

### REPO-008: New repository names are lower-case kebab-case English words

**MUST** · Level 1 · Verified by: organization review (manual)

- ✅ `engineering-standards`, `baraza`, `swahili-asr-benchmark`
- ❌ `RAG_DataAfriqueHub_v2`, `MonProjet`

Renaming an existing repository is optional: GitHub redirects old URLs, but every clone has to update its remote.

## Checklist

- [ ] The root contains only standard files and the expected folders.
- [ ] The layout matches the repository kind (service, library or research).
- [ ] Documentation is in `docs/`; no `docs/` folder inside `src/`.
- [ ] No data, model, build output or virtual environment is committed (`git ls-files | grep -E '\.(pt|h5|safetensors|pdf|zip)$'` is empty).
- [ ] Examples and notebooks are outside the package.

---

*Last verified: 2026-11-13.*
