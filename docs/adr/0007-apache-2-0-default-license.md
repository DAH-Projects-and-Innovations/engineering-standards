---
status: proposed
date: 2026-11-13
decision-makers: DAH Labs team (to validate)
---

# Use Apache-2.0 as the default license for code, and CC BY 4.0 for documentation and data

## Context and problem statement

DAH Labs repositories use MIT, Apache-2.0 or no license at all. A repository without a license is not open source: nobody may legally reuse it. Which license do we use by default?

## Decision drivers

- Real open source, compatible with the open source policy of DAH Labs.
- Protection against patent claims for users and contributors.
- Compatibility with the licenses of the dependencies and of the main AI libraries.
- Clear rules for exceptions (personal data, partner data, commercial incubation, misuse risks).

## Considered options

1. Apache-2.0 for code, CC BY 4.0 for documentation and datasets.
2. MIT for code.
3. A copyleft license (GPL-3.0, AGPL-3.0).

## Decision outcome

Chosen option: **1. Apache-2.0 for code, CC BY 4.0 for documentation and datasets when possible**, with documented exceptions.

### Consequences

- Good: Apache-2.0 is permissive like MIT and adds an explicit patent license and a patent retaliation clause.
- Good: it is the license of many AI projects, which simplifies reuse.
- Bad: Apache-2.0 asks to state significant changes and to keep the NOTICE file, a little more work than MIT.
- Bad: existing MIT repositories need a decision. Changing to Apache-2.0 is possible because MIT code can be included in an Apache-2.0 project, but the MIT copyright notices of existing code must be kept.

### Confirmation

FILE-002 and FILE-003 are checked by the audit (`gh repo view --json licenseInfo`).

## More information

- ⚠️ **Team decision to validate:** the default license, and the harmonization of existing MIT repositories.
- Exceptions follow the open source policy of DAH Labs and are each documented in the README and an ADR of the repository.
- [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), [choosealicense.com](https://choosealicense.com/licenses/)
- Standard: [Required files](../standards/required-files.md#file-003-code-is-apache-20-by-default-documentation-and-data-are-cc-by-40-exceptions-are-documented)
