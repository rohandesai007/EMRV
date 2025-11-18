# Publishing EMRValidator to PyPI

This guide walks you through publishing EMRValidator to PyPI (Python Package Index).

## Prerequisites

1. **PyPI Account**
   - Create account at https://pypi.org/account/register/
   - Verify your email

2. **TestPyPI Account** (for testing)
   - Create account at https://test.pypi.org/account/register/
   - Verify your email

3. **API Tokens**
   - PyPI: https://pypi.org/manage/account/token/
   - TestPyPI: https://test.pypi.org/manage/account/token/
   - Save tokens securely

## One-Time Setup

### 1. Install Build Tools

```bash
pip install build twine
```

### 2. Configure GitHub Secrets

Add these secrets to your GitHub repository (Settings → Secrets and variables → Actions):

- `PYPI_API_TOKEN`: Your PyPI API token
- `TEST_PYPI_API_TOKEN`: Your TestPyPI API token

### 3. Update Package Information

Edit `pyproject.toml`:
```toml
[project]
name = "emrvalidator"
version = "1.0.0"  # Update version
authors = [
    {name = "Your Name", email = "your-email@example.com"}
]

[project.urls]
Homepage = "https://github.com/yourusername/emrvalidator"
Repository = "https://github.com/yourusername/emrvalidator"
```

## Manual Publishing (First Time)

### 1. Clean Previous Builds

```bash
rm -rf build/ dist/ *.egg-info
```

### 2. Build the Package

```bash
python -m build
```

This creates:
- `dist/emrvalidator-1.0.0.tar.gz` (source distribution)
- `dist/emrvalidator-1.0.0-py3-none-any.whl` (wheel distribution)

### 3. Check the Package

```bash
twine check dist/*
```

Verify:
- ✓ No errors in package metadata
- ✓ README renders correctly
- ✓ All required files included

### 4. Test on TestPyPI

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ emrvalidator

# Test the package
python -c "from emrvalidator import DataValidator; print('Success!')"
```

### 5. Publish to PyPI

```bash
# Upload to PyPI
twine upload dist/*

# Verify on PyPI
# Visit: https://pypi.org/project/emrvalidator/
```

### 6. Test Installation from PyPI

```bash
# In a fresh virtual environment
pip install emrvalidator

# Test import
python -c "from emrvalidator import DataValidator; print('Success!')"
```

## Automated Publishing (Recommended)

Once manual publishing works, use GitHub Actions for automated releases.

### 1. Create a Release on GitHub

```bash
# Tag the release
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Or create release via GitHub UI:
# - Go to repository → Releases → Create new release
# - Tag: v1.0.0
# - Title: v1.0.0
# - Description: Copy from CHANGELOG.md
# - Publish release
```

### 2. GitHub Actions Takes Over

The `.github/workflows/publish.yml` workflow will:
1. Build the package
2. Run checks
3. Upload to TestPyPI
4. Upload to PyPI

Monitor progress: Actions tab in GitHub repository

## Version Management

### Semantic Versioning

- **MAJOR** (1.0.0 → 2.0.0): Breaking changes
- **MINOR** (1.0.0 → 1.1.0): New features, backwards compatible
- **PATCH** (1.0.0 → 1.0.1): Bug fixes, backwards compatible

### Update Version

1. Edit `pyproject.toml`:
   ```toml
   version = "1.1.0"
   ```

2. Update `CHANGELOG.md`:
   ```markdown
   ## [1.1.0] - 2024-11-20
   ### Added
   - New feature X
   ### Fixed
   - Bug Y
   ```

3. Commit and tag:
   ```bash
   git add pyproject.toml CHANGELOG.md
   git commit -m "Bump version to 1.1.0"
   git tag v1.1.0
   git push origin main --tags
   ```

4. Create GitHub release

## Troubleshooting

### Error: Package already exists

```bash
# Solution: Increment version in pyproject.toml
# Cannot re-upload same version
```

### Error: Invalid package metadata

```bash
# Check with:
twine check dist/*

# Common issues:
# - Missing or invalid README.md
# - Invalid classifiers in pyproject.toml
# - Missing required fields
```

### Error: Authentication failed

```bash
# Verify:
# - API token is correct
# - Token has "upload" permission
# - Using __token__ as username
```

### README not rendering on PyPI

```bash
# Verify:
# - README.md is valid Markdown
# - readme = "README.md" in pyproject.toml
# - MANIFEST.in includes README.md
```

## Post-Publication Checklist

- [ ] Package appears on PyPI: https://pypi.org/project/emrvalidator/
- [ ] Installation works: `pip install emrvalidator`
- [ ] Import works: `from emrvalidator import DataValidator`
- [ ] Documentation link works
- [ ] GitHub link works
- [ ] Badge on README updates (may take a few minutes)
- [ ] Announce on social media / relevant forums

## Updating Documentation

After publishing, update:

1. **README badges** (if not automatic)
2. **Installation instructions** in docs
3. **Version references** in examples
4. **CHANGELOG.md** with actual release date

## Best Practices

1. **Test thoroughly** on TestPyPI first
2. **Use semantic versioning** consistently
3. **Keep CHANGELOG.md** updated
4. **Tag releases** in git
5. **Automate** with GitHub Actions
6. **Monitor** PyPI stats and issues
7. **Respond** to user feedback quickly

## Resources

- [Python Packaging Guide](https://packaging.python.org/)
- [PyPI Documentation](https://pypi.org/help/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [Semantic Versioning](https://semver.org/)

## Quick Reference

```bash
# Build
python -m build

# Check
twine check dist/*

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ emrvalidator

# Install from PyPI
pip install emrvalidator
```

---

Need help? Open an issue on GitHub!
