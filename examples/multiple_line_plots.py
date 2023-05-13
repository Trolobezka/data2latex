import os

os.chdir(os.path.abspath("./examples"))

import data2latex as dtol
import numpy as np
dtol.use_one_page_standalone()
X = np.linspace(0, 100, 30)
Y = np.cumsum(np.random.normal(10, 10, (3, 30)), axis=1)
dtol.plot([X] * 3, Y, r"Line plots from \texttt{np.random.normal}",
          "Time $t$ [s]", "Variable $b$ [-]", escape_caption=False,
          line=["-", "--", "-."], line_color="black", mark=None,
          legend=["A", "B", "C"], legend_pos="top left",
          xlimits="exact", ylimits=(0, None))
dtol.finish("multiple_line_plots")