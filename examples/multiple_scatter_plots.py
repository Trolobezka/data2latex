import os

os.chdir(os.path.abspath("./examples"))

import data2latex as dtol
import numpy as np
dtol.use_one_page_standalone()
X = [np.random.normal(loc, scale, 100) for loc, scale in [(50, 20), (50, 40), (100, 10)]]
Y = [np.random.normal(loc, scale, 100) for loc, scale in [(50, 20), (100, 40), (75, 10)]]
dtol.plot(X, Y, r"Scatter plots from \texttt{np.random.normal}",
          "Variable $a$ [-]", "Variable $b$ [-]", "#", escape_caption=False,
          line=None, mark="*", mark_fill_opacity=0.7)
dtol.finish("multiple_scatter_plots")