# WOW GitHub Profile Setup

1. Review the redesigned README and project descriptions.
2. Merge the review pull request to `main`.
3. In repository **Actions**, choose **Update Contribution City** and select **Run workflow**.
4. Ensure repository **Settings → Actions → General → Workflow permissions** allows read/write permissions for GitHub Actions if the first run cannot push.
5. Confirm `assets/contribution-city.svg` changed from its setup placeholder to a real skyline.
6. Scheduled runs refresh the graphic daily. The first successful action must run on the default branch.
7. The GraphQL data reflects GitHub's contribution-calendar visibility for the token. Private contributions depend on GitHub settings and authorization.
8. Revisit linked projects and portfolio URL when they change.

All assets are local SVGs, and the generator uses Python's standard library. No paid API key is required. The GitHub-provided GITHUB_TOKEN authenticates the workflow.

**Design note:** Github README viewers do not run arbitrary JavaScript. These SVGs provide decorative motion, while the contribution city is a generated static visual. It is not an interactive WebGL site.
