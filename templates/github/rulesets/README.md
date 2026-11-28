# Ruleset templates

`main.json` is the DAH Labs ruleset for the default branch (rules GH-002 and GH-003).

Before you import it:

1. **Fix the required status checks.** The names above match the caller template
   [`../workflows/ci.yml`](../workflows/ci.yml). Remove the checks of parts that your repository
   does not have (for example `frontend / Node checks`), and copy the exact names from the
   "Checks" tab of a pull request. At Level 2, add the checks of the jobs that you added:
   `sonar / SonarQube Cloud analysis` ([SONAR-004](../../../docs/standards/sonar.md#sonar-004-the-quality-gate-is-the-built-in-sonar-way-gate-and-blocks-the-merge)),
   `docker / Dockerfile lint (hadolint)` and `docker / Docker image build`.
2. **Choose the bypass list.** The template lets the *Repository admin* role (`actor_id: 5`)
   bypass in **pull request only** mode. Replace `bypass_actors` with `[]` to allow no bypass at all.
   Never use `"bypass_mode": "always"`.

Import it:

```bash
gh api --method POST repos/DAH-Projects-and-Innovations/<repo>/rulesets --input main.json
```

or in the web interface: **Settings → Rules → Rulesets → New ruleset → Import a ruleset**.

To update an existing ruleset, find its ID with `gh api repos/DAH-Projects-and-Innovations/<repo>/rulesets`
and use `--method PUT repos/DAH-Projects-and-Innovations/<repo>/rulesets/<id>`.

Rulesets are available for **public** repositories on GitHub Free. Private repositories need
GitHub Team or higher.
