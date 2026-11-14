---
status: accepted
date: 2026-11-13
decision-makers: DAH Labs maintainers
---

# Use pnpm for JavaScript and TypeScript projects

## Context and problem statement

Front-end projects use npm or pnpm. Two package managers mean two lock file formats, two sets of commands in documentation and CI, and possible differences in installed versions. Which package manager do we use?

## Decision drivers

- One lock file format and one set of commands.
- Fast and economical installation (disk and network).
- Strictness: a package cannot use a dependency that it does not declare.

## Considered options

1. pnpm.
2. npm.
3. Yarn.

## Decision outcome

Chosen option: **1. pnpm**, pinned with the `packageManager` field of `package.json`, with Node.js 24 LTS.

### Consequences

- Good: global content-addressed store, fast installs, strict dependency resolution.
- Good: CI and Docker read the pnpm version from `packageManager`.
- Bad: npm projects must migrate (`pnpm import`). Mitigation: the JavaScript standard gives the steps.
- Bad: Node.js 25 and newer do not ship corepack, which was the simplest way to install pnpm. Mitigation: Node.js 24 still includes it; on newer versions use `npm install --global corepack` or the pnpm standalone installer. This ADR is reviewed when DAH Labs moves to Node.js 26.

### Confirmation

`node-ci.yml` runs `pnpm install --frozen-lockfile`; the audit checks that no `package-lock.json` or `yarn.lock` exists.

## More information

- [pnpm documentation](https://pnpm.io/)
- [Node.js corepack documentation](https://nodejs.org/api/corepack.html)
- Standard: [JavaScript and TypeScript](../standards/javascript.md)
