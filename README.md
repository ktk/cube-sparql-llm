# Installation guide (tested on Python 3.10)

1. Install python
2. Install poetry globally

```
pip install poetry
```

3. Setup virtual environment in local directory:

```
python -m venv .venv
```

4. Activate virtual environment

```
source .venv/bin/activate
```

5. Install dependencies using poetry in virtual environment

```
poetry install --no-root
```

6. Recommended way to run: Visual Studio Code with Python etensions installed. Allows to run playground/full_pipelne.ipynb notebook.


