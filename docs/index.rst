.. data2latex documentation master file, created by
   sphinx-quickstart on Sat May  6 15:14:35 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Data2LaTeX's documentation!
======================================

.. image:: /_static/img/logo.png
   :alt: Data2LaTeX logo
   :align: center
   :scale: 80 %

.. _PyLaTeX: https://jeltef.github.io/PyLaTeX/current/index.html
.. _GitHub: https://github.com/Trolobezka/data2latex

.. toctree::
   :maxdepth: 2
   :caption: Contents:

This project is part of my bachelor thesis which deals with data representation using **Python** and **LaTeX**. You can find the source code on my GitHub_.

The idea behind this package prototype is that generating LaTeX documents containing scientific data from Python should not be difficult and require many steps. Currently the package supports the creation of simple tables and two types of plots: scatter plots and line plots. The package uses the PyLaTeX_ package to handle the document creation and compilation process. The main data sources are arrays and data tables from the popular ``numpy`` and ``pandas`` packages. A major inspiration for the module syntax is the ``matplotlib.pyplot`` module, which allows plots to be created in a few lines of code. The tables are created using ``tblr`` environment from ``tabularray`` package. The plots are created using ``tikzpicture`` / ``axis`` environment from ``tikz`` / ``pgfplots`` package.

Examples
========

Simple features
---------------

Data2LaTeX offers two basic features: sections and plain text. If you need other features and environment, you can use PyLaTeX to create the features and insert them into the document object manually.

.. highlight:: python
.. code-block:: python

   import data2latex as dtol
   dtol.section("Data2LaTeX")
   dtol.text("This project is part of my bachelor thesis which deals with data representation using Python and LaTeX")
   dtol.finish("simple_features")

.. image:: /_static/img/simple_features.pdf.png
   :scale: 30 %
   :class: img-border

Simple table
------------

.. highlight:: python
.. code-block:: python

   import data2latex as dtol
   data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
   dtol.table(data)
   dtol.finish("simple_table")

.. image:: /_static/img/simple_table.pdf.png
   :scale: 30 %
   :class: img-border

Simple plot
-----------

.. highlight:: python
.. code-block:: python

   import data2latex as dtol
   X = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
   Y = [84, 13, 94, 37, 80, 89, 90, 45, 55, 26, 92]
   dtol.plot(X, Y, line="-", mark="*")
   dtol.finish("simple_plot")

.. image:: /_static/img/simple_plot.pdf.png
   :scale: 30 %
   :class: img-border

Table from ``numpy.ndarray``
----------------------------

.. highlight:: python
.. code-block:: python

   import data2latex as dtol
   import numpy as np
   data = np.random.normal(0, 1000, (8, 4))
   dtol.table(data, "#", r"Data from \texttt{numpy.random.normal}", escape_caption=False)
   dtol.finish("table_from_numpy_ndarray")

.. image:: /_static/img/table_from_numpy_ndarray.pdf.png
   :scale: 30 %
   :class: img-border

Table from ``pandas.DataFrame``
-------------------------------

.. highlight:: python
.. code-block:: python

   import data2latex as dtol
   import pandas as pd
   data = pd.DataFrame(
      [[True, 0.1, "red"], [True, 0.9, "blue"], [False, 0.6, "black"]],
      ["First", "Second", "Third"],
      ["bool", "float", "str"],
   )
   dtol.table(
      data, "o", r"Data from \texttt{pandas.DataFrame}",
      escape_caption=False, float_format="{:0.1f}",
      left_head_bold=True, left_head_col_align="r",
      top_head_bold=True,
   )
   dtol.finish("table_from_pandas_dataframe")

.. image:: /_static/img/table_from_pandas_dataframe.pdf.png
   :scale: 30 %
   :class: img-border

Table cells with macros
-----------------------

.. _here: https://jeltef.github.io/PyLaTeX/current/api.html

Here we are using ``Package`` and ``NoEscape`` from PyLaTeX to add a new package and a custom macro into our document preamble. More about PyLaTeX features here_. We can get the document instance with function ``gd()`` from Data2LaTeX.

.. highlight:: python
.. code-block:: python

   import data2latex as dtol
   import pylatex as tex
   dtol.gd().packages.add(tex.Package("xcolor"))
   dtol.gd().packages.add(tex.utils.NoEscape(
      r"\newcommand{\RGB}[3]{\fcolorbox{black}%" + "\n"
      r"{rgb,255:red,#1;green,#2;blue,#3}%" + "\n"
      r"{\makebox[47pt][r]{\textcolor{white}%" + "\n"
      r"{{#1|#2|#3}}}}}%"
   ))
   data = [[r"\RGB{%s}{%s}{%s}" % ((x, 0, y)) for y in range(0, 256, 51)]
         for x in range(0, 256, 51)]
   dtol.table(
      data, "", "RGB boxes with varying R and B channels",
      use_siunitx=False, escape_cells=False
   )
   dtol.finish("table_cells_with_macros")

.. image:: /_static/img/table_cells_with_macros.pdf.png
   :scale: 30 %
   :class: img-border

Implemented features
====================

.. autofunction:: data2latex.gd
.. autofunction:: data2latex.gdm
.. autofunction:: data2latex.setup
.. autofunction:: data2latex.use_one_page_standalone
.. autofunction:: data2latex.use_multi_page_standalone
.. autofunction:: data2latex.section
.. autofunction:: data2latex.text
.. autofunction:: data2latex.plot
.. autofunction:: data2latex.table
.. autofunction:: data2latex.finish
.. autofunction:: data2latex.latex
.. autofunction:: data2latex.pdf
.. autofunction:: data2latex.reset

* :ref:`genindex`