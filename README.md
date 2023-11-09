## Integrating RDF Cubes with SPARQL and LLMs

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ktk/cube-sparql-llm.git/HEAD?labpath=cube-sparql-langchain%2Ffull_pipeline.ipynb)

Welcome to the intersection of structured data and cutting-edge AI! This Jupyter notebook aims to explore the synergy between RDF cubes, SPARQL queries, and Language Model (LM) capabilities. Using [OpenAI's API](https://platform.openai.com/docs/introduction) through [LangChain](https://www.langchain.com/), we will dive into the process of constructing intuitive SPARQL queries to interact with [RDF cubes](https://cube.link), enhancing our data retrieval and analysis processes

This Proof of Concept (PoC) taps into the powerful combination of structured semantic web data (RDF cubes) and natural language processing.

## Setting the Stage

The fastest way to try this is to click on the "launch binder" icon above. This will start a web-based container where you can directly try the notebook. The only thing you need to adjust is the [OpenAI API key](https://platform.openai.com/api-keys), which you can generate using the trial offer from OpenAI (requires credit card now apparently...).

If you wish to run the project locally, please follow the installation guide below.

### Prerequisites

Ensure you have Python 3.10 installed to align with our dependencies.

### Project Setup
1. Install [python](https://www.python.org/).
2. Install [poetry](https://python-poetry.org/) globally.

```
pip install poetry
```

3. Clone the repository and navigate to the project directory.

```
git clone https://github.com/ktk/cube-sparql-llm.git
cd cube-sparql-llm
```

4. Create a virtual environment within the project directory.

```
python -m venv .venv
```

5. Activate your virtual environment

```
source .venv/bin/activate
```

6. Install dependencies using poetry in virtual environment

```
poetry install --no-root
```

7. Run it within Visual Studio Code

The optimal experience is through Visual Studio Code equipped with the [Jupyter extension](https://code.visualstudio.com/docs/datascience/jupyter-notebooks) . This setup allows seamless interaction with the `playground/full_pipeline.ipynb` notebook, our playground for our hands-on adventure.

## Contributing

We welcome contributions from the community! If you have suggestions for improvements or want to contribute to the code, please feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright 2023 Zazuko GmbH

