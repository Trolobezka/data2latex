import os

os.chdir(os.path.abspath("./examples"))

import data2latex as dtol
import numpy as np
dtol.use_one_page_standalone()
X = np.linspace(0, 2, 50)
Y = [np.exp(X) + np.random.uniform(0, 0.2, 50),
     (2 * X + 1) + np.random.uniform(0, 0.3, 50)]
dtol.plot([X] * 2, Y, r"Line plots with semi-log scale",
          "Variable $x$ [-]", "Variable $y$ [-]",
          line="-", mark=None, mode=("lin", "log"),
          legend=[r"$e^x+\varepsilon_1(x)$", r"$5x+1+\varepsilon_2(x)$"],
          legend_pos="top left", legend_entry_align="l",
          xlimits="exact", ylimits=(1, None),
          precision=1, zerofill=(False, True))
dtol.finish("line_plots_semilog_scale")