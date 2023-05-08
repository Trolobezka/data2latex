from typing import (
    Any,
    Dict,
    Generator,
    Generic,
    Iterator,
    List,
    Literal,
    Optional,
    Protocol,
    Tuple,
    TypeAlias,
    TypeVar,
    Union,
    runtime_checkable,
)

import numpy as np
import pandas as pd
import pylatex as tex  # pyright: ignore [reportMissingTypeStubs]

import data2latex as dtol

dtol.section("Testing Area")
dtol.text(
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
dataframe = pd.DataFrame([[True, 0, 0], [0, "a", 0], [0, 0, 11.256]], header, header)

dtol.table(data, caption="Data from numpy.ndarray", rules="#", top_head_bold=True)

dtol.table(
    dataframe,
    caption="Data from pandas.DataFrame",
    rules="|2_2",
    top_head_bold=True,
    top_head_col_align="l",
    left_head_bold=True,
    left_head_col_align="r",
    col_align="r",
)

try:
    dtol.pdf("overall")
except:
    print("COMPILATION ERROR")
dtol.latex()
