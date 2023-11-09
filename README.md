# RDF Cube meets SPARQL meets LLM

```
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ktk/cube-sparql-llm.git/HEAD?labpath=cube-sparql-langchain%2Ffull_pipeline.ipynb)
```

PoC using [OpenAI API](https://platform.openai.com/docs/introduction) via [LangChain](https://www.langchain.com/) to create SPARQL queries that query [RDF cubes](https://www.langchain.com/).

## Installation guide

1. Install python. At the time writing, dependencies require Python 3.10.
2. Install [poetry](https://python-poetry.org/) globally

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

6. Recommended way to run: Visual Studio Code with [Jupyter extension](https://code.visualstudio.com/docs/datascience/jupyter-notebooks) installed. Allows to run `playground/full_pipelne.ipynb` notebook.

