# Quality checks

Lint (Ruff) and tests (pytest) run locally and in GitHub Actions with the same commands. These are development tools only; they do not choose the application's runtime dependencies.

## Run locally (Windows PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt

ruff check .
python -m pytest
```

To apply safe automatic lint fixes: `ruff check . --fix`.

## What CI runs

`.github/workflows/ci.yml` runs on pushes to `main` and on pull requests, on `windows-latest` with Python 3.11 and 3.13. Each job installs `requirements-dev.txt`, then runs `ruff check .` and `python -m pytest`.

## Configuration

- `pyproject.toml` holds only pytest and Ruff settings. It deliberately has no `[project]` table, so the package name, packaging and Python requirement stay undecided.
- `requirements-dev.txt` lists the two tools.
- `tests/test_smoke.py` exists only so pytest collects at least one test; delete it when real tests are added.

## Adjusting

The Python versions in the CI matrix and Ruff's `target-version` are a practical starting point, not a support decision. Change them together when the supported versions are decided.
