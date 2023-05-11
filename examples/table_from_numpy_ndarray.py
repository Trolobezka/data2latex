import os

os.chdir(os.path.abspath("./examples"))

import data2latex as dtol
import numpy as np
dtol.use_one_page_standalone()
data = np.random.normal(0, 1000, (8, 4))
dtol.table(data, "#", r"Data from \texttt{numpy.random.normal}", escape_caption=False)
dtol.finish("table_from_numpy_ndarray")
