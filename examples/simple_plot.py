import os

os.chdir(os.path.abspath("./examples"))

import data2latex as dtol
dtol.use_one_page_standalone()
X = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Y = [84, 13, 94, 37, 80, 89, 90, 45, 55, 26, 92]
dtol.plot(X, Y, line="-", mark="*")
dtol.finish("simple_plot")