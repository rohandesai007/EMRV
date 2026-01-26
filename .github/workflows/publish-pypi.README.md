# Publish to PyPI workflow (README)

What this workflow does
- On every push of a Git tag that matches `v*` (for example `v1.0.2`), the workflow builds source and wheel distributions and publishes them to PyPI.

Required repository secret
- `PYPI_API_TOKEN` — a PyPI API token (value only, not username). Create it on https://pypi.org/manage/account/#api-tokens:
  1. Click "Add API token".
  2. Choose scope (project-specific recommended) and create token.
  3. Copy the token value immediately (you won't be able to view it again).
  4. In GitHub: Repository -&gt; Settings -&gt; Secrets and variables -&gt; Actions -&gt; New repository secret. Name it `PYPI_API_TOKEN` and paste the token.

How to trigger the workflow
- Bump the package version (e.g., in `pyproject.toml` and/or package `__init__`) and commit that change.
- Create an annotated Git tag with the same version name (e.g., `git tag -a v1.0.2 -m "release v1.0.2"`).
- Push the tag: `git push origin v1.0.2`.
- The workflow will run automatically and publish the built distributions to PyPI.

Tips and notes
- Ensure `pyproject.toml` contains the correct version before tagging.
- Test builds locally with `python -m build`.
- Scope the PyPI token to the specific project for better security.
- If you want GitHub Releases created automatically, I can add a step to make a release on tag.
