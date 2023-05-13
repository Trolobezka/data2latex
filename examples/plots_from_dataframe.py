import os

os.chdir(os.path.abspath("./examples"))

from io import StringIO
import data2latex as dtol
import pandas as pd
dtol.use_one_page_standalone()
data = pd.read_csv(StringIO("""\
x,A,B
0,0.0367,0.3447
1,0.8942,0.9806
2,1.1932,1.9215
3,1.5006,2.0402
4,1.6435,2.3271
5,1.9531,2.7670
6,2.6498,3.6242
7,2.6637,3.9957
8,3.5884,4.0811
9,3.6901,5.0544
10,4.6011,5.1315
"""))
X = data[data.columns[0]]
legend = data.columns[1:].tolist()
Y = data[legend].__array__().T
dtol.plot(
    [X] * len(legend), Y, legend=legend, grid="_1",
    legend_pos="top left", line="-", mark=["o", "x"],
    mark_fill_color=None, mark_stroke_opacity=1.0,
    mark_stroke_color=["blue", "red"])
dtol.finish("plots_from_dataframe")
