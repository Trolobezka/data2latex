import os

os.chdir(os.path.abspath("./examples"))

import data2latex as dtol
dtol.use_one_page_standalone()
data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
dtol.table(data)
dtol.finish("simple_table")
