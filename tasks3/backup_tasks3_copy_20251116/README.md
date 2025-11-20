This package contains the `tasks3` and `tasks2` test/demo code used for the course
exercise. To run the test suite locally on Windows PowerShell when using the
project's `src` layout, set PYTHONPATH to point at the package `src` directory
before running pytest. Example (run from the `tasks3` folder):

```powershell
$env:PYTHONPATH='C:\Users\Ifra\csc299-project\tasks3\tasks3\src'
python -m pytest -q
```

If you prefer installing development dependencies into a virtual environment,
create and activate a venv and install the items in `requirements-dev.txt`:

```powershell
# create and activate a venv (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
pytest -q
```

Notes:
- The tests in this repo assume the packages are importable from the `src`
	directory. Either set `PYTHONPATH` as shown above or install the package in
	editable mode (`pip install -e .`) from the project root.
