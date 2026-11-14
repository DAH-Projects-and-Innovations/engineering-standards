# Clean code

## TL;DR

- Code is read many more times than it is written, often by a volunteer who does not know it yet. Write for that reader.
- **Names** say what a thing is or does, in English, without abbreviations.
- **Small functions** that do one thing. Ruff and SonarQube Cloud check complexity, number of arguments and branches.
- **No magic values, no dead code, no commented-out code.**
- **Errors are explicit**: specific exceptions, never `except: pass`, never a silent failure.
- Comments explain **why**, not what. A `TODO` has an issue number.

Most of these rules are checked automatically by the [Ruff configuration](python.md#py-006-level-2-enables-the-full-dah-labs-rule-set) and by [SonarQube Cloud](sonar.md). The others are checked in [code review](code-review.md).

## Rules

### CC-001: Names say what things are, in English, without abbreviations

**MUST** · Level 1 · Verified by: code review (manual); Ruff `N` rules for the naming style (automatic)

- Variables and functions: `snake_case`. Classes: `PascalCase`. Constants: `UPPER_SNAKE_CASE`. TypeScript: `camelCase` and `PascalCase`.
- A function name is a verb (`load_documents`, `build_prompt`); a boolean starts with `is_`, `has_`, `can_` or `should_`.
- Use the words of the domain, the same everywhere: if the domain says "document", do not also say "file", "doc" and "item".
- Common abbreviations are fine (`id`, `url`, `http`, `llm`, `api`); others are not (`usr`, `cnt`, `tmp_lst`).
- One-letter names only for very short scopes (`for i in range(3)`, `lambda x: x.score`).

**Examples:**

- ✅ `def split_into_chunks(text: str, max_tokens: int) -> list[Chunk]:`
- ❌ `def proc(t, n):` (what does it do, what are `t` and `n`?)

### CC-002: Functions are short, do one thing, and stay within the complexity limits

**SHOULD** · Level 1 · Verified by: Ruff `C90`, `PLR0911`, `PLR0912`, `PLR0913`, `PLR0915` (automatic)

The [pyproject template](../../templates/python/pyproject.toml) sets the limits: cyclomatic complexity 10, 6 arguments, 12 branches, 6 return statements, 50 statements. When a function reaches a limit, split it; do not add a `noqa`.

**Why:** a function that does one thing has a clear name, is easy to test, and fits on one screen.

### CC-003: Cognitive complexity of a function is at most 15

**SHOULD** · Level 2 · Verified by: SonarQube Cloud rule "Cognitive Complexity of functions should not be too high" (automatic)

Cognitive complexity counts how hard the code is to **read**: nested conditions and loops cost more than flat ones. Reduce it with early returns ([CC-007](#cc-007-early-returns-instead-of-deep-nesting)), small helper functions and lookup tables.

### CC-004: No magic numbers or strings

**MUST** · Level 1 · Verified by: Ruff `PLR2004` (automatic); code review (manual)

A value with a meaning gets a name: a module constant, an `Enum`, or a setting when it can change between environments.

```python
# ✅
MAX_CHUNK_TOKENS = 512
if len(tokens) > MAX_CHUNK_TOKENS:
    ...

# ❌ What is 512? Is it the same 512 as in the other module?
if len(tokens) > 512:
    ...
```

`0`, `1`, `-1`, `""` and values in tests are fine.

### CC-005: No dead code and no commented-out code

**MUST** · Level 1 · Verified by: Ruff `F401`, `F841`, `ERA001` (automatic); SonarQube Cloud (automatic)

Delete unused imports, variables, functions and files. Do not keep old code in comments "just in case": Git keeps the history.

**Why:** dead code is read, maintained and feared by everybody, and used by nobody.

### CC-006: Errors are explicit and never silenced

**MUST** · Level 1 · Verified by: Ruff `E722`, `S110`, `S112`, `B904` (automatic); code review (manual)

- Catch **specific** exceptions, never a bare `except:`. Catch `Exception` only at the edge (a route, a worker loop), to log it and return an error.
- Never `except ...: pass`. If ignoring an error is correct, write why and log it.
- Raise exceptions of the domain or of the port (`DocumentNotFoundError`), with `raise ... from error` to keep the cause.
- Do not return `None` or `False` to mean "it failed": raise, or return a result type that the caller must check.
- Error messages say what happened and what to do, without secrets or personal data ([PY-020](python.md#py-020-logs-contain-no-secrets-and-no-personal-data)).

```python
# ✅
try:
    response = client.post("/chat/completions", json=payload)
    response.raise_for_status()
except httpx.HTTPError as error:
    raise LanguageModelError("The language model did not answer.") from error

# ❌ The caller receives None and fails later, far from the cause.
try:
    response = client.post("/chat/completions", json=payload)
except Exception:
    return None
```

### CC-007: Early returns instead of deep nesting

**SHOULD** · Level 1 · Verified by: code review (manual); SonarQube Cloud cognitive complexity (automatic)

Handle the special cases first and return. The main path stays at the first indentation level.

```python
# ✅
def answer(question: Question) -> Answer:
    documents = retriever.search(question, limit=3)
    if not documents:
        return Answer(text=NO_DOCUMENT_ANSWER, sources=())
    return Answer(text=model.complete(question, documents), sources=ids(documents))


# ❌
def answer(question):
    documents = retriever.search(question, limit=3)
    if documents:
        text = model.complete(question, documents)
        if text:
            return Answer(text=text, sources=ids(documents))
        else:
            ...
    else:
        ...
```

### CC-008: Each module and class has one responsibility, and depends on abstractions

**SHOULD** · Level 2 · Verified by: code review (manual); import-linter (automatic)

The SOLID principles, in practice:

| Principle | In DAH Labs code |
|---|---|
| **S**ingle responsibility | One use case per module; one adapter per technology. A class named `Manager`, `Helper` or `Utils` usually does too much. |
| **O**pen/closed | Add a new adapter (a new vector store) without changing the use case. |
| **L**iskov substitution | Every adapter of a port behaves as the port describes: a fake, a test double and the real adapter are interchangeable. |
| **I**nterface segregation | Small ports: `Retriever` with `search()`, not a `VectorDatabase` port with twenty methods. |
| **D**ependency inversion | Use cases depend on `Protocol` ports; the composition root gives the adapters ([ARCH-004](architecture.md#arch-004-one-composition-root-creates-the-adapters-nothing-is-created-at-import-time)). |

### CC-009: Comments explain why; a TODO has an issue number

**SHOULD** · Level 1 · Verified by: code review (manual)

- Good names make "what" comments useless. Write a comment for **why**: a business reason, a workaround, a link to a paper or an issue.
- Public functions have docstrings ([PY-011](python.md#py-011-public-api-has-google-style-docstrings)).
- `# TODO(#123): ...` with the number of the issue that tracks it. A `TODO` without issue is forgotten.

**Examples:**

- ✅ `# The provider rejects requests above 32k tokens (see #87), so we truncate here.`
- ❌ `# increment i` above `i += 1`

### CC-010: Data is immutable by default, and default arguments are never mutable

**SHOULD** · Level 1 · Verified by: Ruff `B006`, `B008`, `RUF009` (automatic); code review (manual)

- Prefer `@dataclass(frozen=True)`, `tuple` and `frozenset` for values that should not change.
- Never `def f(items: list[str] = [])`: use `None` and create the list inside, or `field(default_factory=list)`.
- Do not change the arguments you receive; return a new value.

### CC-011: Business logic is in pure functions; side effects are at the edges

**SHOULD** · Level 1 · Verified by: code review (manual)

A function that computes something (a score, a prompt, a chunk split) takes values and returns a value. Reading files, calling APIs, writing to databases and logging happen in adapters and entry points.

**Why:** pure functions are tested with simple asserts, without mocks, and give the same result every time.

### CC-012: Duplicated logic is extracted the third time

**SHOULD** · Level 2 · Verified by: SonarQube Cloud duplication condition, at most 3 % on new code (automatic)

Two similar blocks are acceptable; at the third one, extract a function. Do not extract code that only looks similar but changes for different reasons.

## Checklist

- [ ] Names are English words of the domain, without unusual abbreviations.
- [ ] Ruff passes without new `noqa` for complexity, arguments or magic values.
- [ ] No unused code and no commented-out code.
- [ ] No bare `except`, no `except: pass`; exceptions are specific and chained with `from`.
- [ ] Comments explain why; every `TODO` has an issue number.
- [ ] No mutable default argument.

---

*Last verified: 2026-11-14.*
