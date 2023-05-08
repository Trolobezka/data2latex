from typing import (
    Any,
    Dict,
    List,
    Literal,
    Optional,
    TypeAlias,
    Union,
    Tuple,
    Protocol,
    runtime_checkable,
    Generator,
    Iterator,
    Generic,
    TypeVar,
)

import numpy as np
import pylatex as tex
import pandas as pd

import data2latex as d2l
from data2latex.iter_protocols import *

d2l.section("Testing Area")
d2l.text(
    "Fusce ex sem, lacinia eget eros ac, semper blandit leo. Fusce vel aliquam magna. Nulla facilisi. Donec vel sapien rhoncus eros accumsan congue consectetur ut arcu. Nullam tincidunt lectus a leo rutrum, sed posuere turpis aliquet. Aenean vel aliquet arcu. Etiam vulputate, eros et euismod ultrices, ante sapien semper tellus, ac aliquet turpis leo et tortor. Sed et ex id velit bibendum ultrices. Aliquam erat volutpat."
)

a = np.random.normal(1000, 200, (4, 2))
b = np.random.normal(1, 2, (4, 2))
data = np.concatenate([a, b], axis=1)
data = data.astype("object")
data = np.concatenate(
    [np.array([["First", "Second", "Third long", "Fourth"]]), data], axis=0
)

header = ["Cat", "Dog", "Rabbit"]
animals = pd.DataFrame([[True, 2, 3], [3, "a", 2], [0, 1, 11.256]], header, header)
animals = pd.DataFrame(
    [["1", "2", "3"], ["Ahoooooj", "a", "HEEEELLoooo"], [True, 1, 11.256]],
    header,
    header,
)

d2l.table(
    animals.__array__().tolist(),
    caption="Some animals",
    DF_row_names=False,
    line_style="header",
    header_col_align="l",
    col_align="r",
    header_dir="top",
    str_try_number=False,
)

d2l.table(
    data,
    caption="Table with no settings",
)
d2l.table(
    data,
    caption="Decent table",
    escape_caption=False,
    line_style="header",
    header_dir="top",
    header_col_align="l",
    col_align="r",
    use_siunitx=True,
)

try:
    d2l.pdf()
except:
    print("COMPILATION ERROR")
d2l.latex()
