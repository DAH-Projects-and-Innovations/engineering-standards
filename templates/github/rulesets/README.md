# Ruleset templates

`main.json` is the DAH Labs ruleset for the default branch (rules GH-002 and GH-003).

Before you import it:

1. **Fix the required status checks.** The names above match the caller template
   [`../workflows/ci.yml`](../workflows/ci.yml). Remove the checks of parts that your repository
   does not have (for example `frontend / Node checks`), and copy the exact names from the
   "Checks" tab of a pull request.
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
