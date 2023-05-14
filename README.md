# Data2LaTeX

![Data2LaTeX logo](docs/_static/img/logo.png)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This project is part of my bachelor thesis which deals with data representation using **Python** and **LaTeX**. You can find the source code on my [GitHub](https://github.com/Trolobezka/data2latex).

The idea behind this package prototype is that generating LaTeX documents containing scientific data from Python should not be difficult and require many steps. Currently the package supports the creation of simple tables and two types of plots: scatter plots and line plots. The package uses the [PyLaTeX](https://github.com/JelteF/PyLaTeX) package to handle the document creation and compilation process. The main data sources are arrays and data tables from the popular `numpy` and `pandas` packages. A major inspiration for the module syntax is the `matplotlib.pyplot` module, which allows plots to be created in a few lines of code. The tables are created using `tblr` environment from `tabularray` package. The plots are created using `tikzpicture` / `axis` environment from `tikz` / `pgfplots` package.

## Examples

Examples with results can be found in the [documentation](https://trolobezka.github.io/data2latex-docs).

### Simple features

```python
import data2latex as dtol
dtol.section("Data2LaTeX")
dtol.text("This project is part of my bachelor thesis which deals with data representation using Python and LaTeX.")
dtol.finish("simple_features")
```

### Simple table

```python
import data2latex as dtol
data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
dtol.table(data)
dtol.finish("simple_table")
```

### Simple plot

```python
import data2latex as dtol
X = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Y = [84, 13, 94, 37, 80, 89, 90, 45, 55, 26, 92]
dtol.plot(X, Y, line="-", mark="*")
dtol.finish("simple_plot")
```

## Installation

```bash
python -m pip install --upgrade pip
python -m pip install --upgrade data2latex
```

## Development

```bash
python -m venv .venv
./.venv/Scripts/activate
python -m pip install --upgrade pip
python -m pip install .[dev]
```

## Generating documentation

```bash
sphinx-apidoc -o docs src/data2latex
./docs/make html
```

## Packaging

```bash
python clear.py
python -m pip install --upgrade build
python -m build
```

## Publishing

```bash
python -m pip install --upgrade twine
python -m twine upload dist/*
```