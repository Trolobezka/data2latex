import os

os.chdir(os.path.abspath("./examples"))

import data2latex as dtol
import pandas as pd
dtol.use_one_page_standalone()
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
