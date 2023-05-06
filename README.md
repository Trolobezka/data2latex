# data2latex

This project is part of my bachelor thesis which deals with data representation using Python and LaTeX.

The idea behind this package prototype is that generating LaTeX documents containing scientific data from Python should not be difficult and require many steps. Currently the package supports the creation of simple tables and two types of plots: scatter plot and line plot. The package uses the PyLaTeX package to handle the document creation and compilation process. The main data sources are arrays and data tables from the popular Numpy, SciPy and Pandas packages. A major inspiration for the package syntax is the Matplotlib.Pyplot package, which allows plots to be created in a few lines of code. This package allows the user to choose a backend for plotting: Matplotlib in Python or pgfplots in LaTeX.

## Examples

```python
print("Hello World!")
```

## Installation

```bash
python -m pip install --upgrade pip
python -m pip install --upgrade data2latex
```

## Developing

```bash
python -m venv .venv
./.venv/Scripts/activate
python -m pip install --upgrade pip
python -m pip install .
python -m pip install .[dev]
```

## Generating documentation

```bash
sphinx-apidoc -o docs src
./docs/make html
```

## Packaging

```bash
python clear.py
python -m pip install --upgrade build
python -m build
python -m pip install ./dist/data2latex-?.whl
```