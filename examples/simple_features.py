import os

os.chdir(os.path.abspath("./examples"))

import data2latex as dtol
dtol.use_one_page_standalone()
dtol.section("Data2LaTeX")
dtol.text("This project is part of my bachelor thesis which deals with data representation using Python and LaTeX")
dtol.finish("simple_features")
