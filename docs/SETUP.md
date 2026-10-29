# Maintaining the contribution metropolis

This profile uses local SVGs, Python's standard library, and GitHub Actions. There is no JavaScript inside the README, paid image service, or aesthetic API key.

## Review and activate

1. Review the `profile/neon-metropolis` branch and pull request. The branch README uses relative assets so you can inspect the complete design before merging.
2. Merge the pull request into `main` to display it on the public profile. A branch preview does not replace the live profile.
3. `Update Contribution City` runs at **03:17 UTC / 08:47 IST daily**, on manual dispatch, and on relevant generator changes to `main`. Scheduled runs start only after the workflow exists on the default branch.
4. `Update Contribution Snake` runs weekly, Mondays at **03:47 UTC / 09:17 IST**, on manual dispatch, and on relevant workflow changes. Its first successful run inserts the local SVG into the dedicated README marker. Until then the README displays a setup link, never a broken image.
5. Both refresh workflows also allow the dedicated review branch for pre-merge validation. They share a concurrency group to prevent simultaneous pushes. The read-only validation workflow runs on pull requests.

GitHub schedules can be delayed and may be disabled after prolonged repository inactivity. Manual **Actions → workflow → Run workflow** remains available.

## Authentication and permissions

The supplied `GITHUB_TOKEN` is used for the supported GitHub GraphQL `contributionCalendar` query and public repository metadata. No personal token is needed for the default configuration. The source code is pinned to full action commit SHAs, including the optional Platane snake generator.

Workflow-level permissions are `contents: read`. Only the two publication jobs request `contents: write`; PR validation remains read-only, with checkout credentials disabled. There is no `pull_request_target` event and no write job runs pull-request code. Refreshes stage explicit output paths and never use `git add .` or force-push.

If a repository or organization policy blocks bot writes, the workflow will fail without changing unrelated files. Review that policy; do not grant broad account access just to refresh a profile. Protected branches that require PRs also prevent direct bot pushes; in that case maintain generated assets through review branches or change the workflow to create PRs according to repository policy.

Do not paste tokens in source code, command arguments, screenshots, or commits. This package does not read private repository metadata. The public repository endpoint is explicitly used for the dashboard.

## Data fidelity

- Each city block is a real calendar date. Zero counts are dark empty platforms.
- Height is `7 + 126 * log2(count+1) / log2(max_count+1)` for active days. Normalization is per snapshot; compare counts rather than absolute heights across snapshots.
- Roof bands are 0, 1–2, 3–9, and 10+. A beacon marks every tied maximum.
- The date position is calculated from the actual weekday, preserving partial weeks. Polygons are ordered back to front.
- The default query returns GitHub's rolling contribution calendar. A local bootstrap and failure fallback parse exact counts from GitHub's public contribution tooltips. This HTML is not a stable API: unknown or incomplete markup fails closed; colors are never converted into invented counts.
- Both sources validate nonnegative integer counts and a continuous 300–371-day calendar. `data/contributions.json` records which source produced the data.
- Visibility follows GitHub settings and token access. Publicly visible anonymous private counts may be included. Counts are not equivalent to public commits, productivity, or code quality.
- The dashboard counts **owned public non-fork repositories**, their stars, and their primary language. It does not scan private repositories, count vendored bytes, or claim language expertise.
- The longest streak is computed only inside this calendar, not across all years. No ambiguous current-streak widget or unverifiable trophy badge is displayed.

On a fetch, authentication, rate-limit, or data-validation failure, the job reports an error and retains the last committed snapshot. It never publishes a fabricated zero calendar. Requests have timeouts; the workflow has an overall timeout. There are no unbounded retry loops. Identical source data produces identical files, and the workflows commit only staged differences.

## Local commands

Use Python 3.10+ (Actions uses 3.12). No `pip install` is required.

```sh
python scripts/generate_assets.py
python scripts/generate_city.py --input data/contributions.json
python scripts/generate_stats.py --input data/repositories.json
python -m unittest discover -s tests -v
python scripts/validate_profile.py
```

To refresh from GitHub, omit `--input`. Set `GH_TOKEN` securely in your shell environment if available. Without it, the city uses the public calendar bootstrap and repository statistics use unauthenticated REST limits. The public HTML endpoint may change independently of the supported GraphQL API.

## Customization

| File | Responsibility |
| --- | --- |
| `README.md` | Recruiter-readable copy, project links, local asset embeds |
| `scripts/generate_assets.py` | Hero, typing strip, developer OS, five concept cards, experience journey |
| `scripts/generate_city.py` | Data collection, strict validation, isometric rendering, atomic writes |
| `scripts/generate_stats.py` | Public repository snapshot and activity dashboard |
| `scripts/attach_snake.py` | Insert successful snake output into its README marker; add reduced-motion CSS |
| `data/*.json` | Inspectable real input snapshots |
| `.github/workflows/` | Refresh city/statistics, optional snake, and read-only CI |
| `tests/test_city.py` | Real-data rendering, data rejection, failure preservation, and deterministic writes |
| `docs/AUDIT.md` | Evidence, project-status decisions, link review, validation limits |

Change source generators and regenerate assets rather than hand-editing generated SVGs. All SVGs have a `viewBox`, meaningful accessible descriptions or README alt text, and opaque dark canvases that retain contrast in light and dark GitHub themes. Important identity and project text also exists as normal Markdown for mobile reading and assistive technology.

Animation uses CSS inside SVG, with `prefers-reduced-motion` overrides. Some GitHub clients or image proxies can display static frames. The hero and city remain meaningful without motion. The optional snake is collapsed by default. GitHub Markdown does not support a true interactive 3D/WebGL city; this is a data-generated isometric SVG.

## Sources

- [GitHub GraphQL reference](https://docs.github.com/en/graphql/reference)
- [Public contribution calendar](https://github.com/users/AishwaryaChandel27/contributions)
- [GitHub REST: list repositories for a user](https://docs.github.com/en/rest/repos/repos#list-repositories-for-a-user)
- [GitHub workflow syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Platane/snk](https://github.com/Platane/snk) — optional snake, pinned in the workflow
