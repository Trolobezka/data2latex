import os

os.chdir(os.path.abspath("./examples"))

import data2latex as dtol
import pylatex as tex
dtol.use_one_page_standalone()
dtol.gd().packages.add(tex.Package("xcolor"))
dtol.gd().packages.add(tex.utils.NoEscape(
    r"\newcommand{\RGB}[3]{\fcolorbox{black}%" + "\n"
    r"{rgb,255:red,#1;green,#2;blue,#3}%" + "\n"
    r"{\makebox[47pt][r]{\textcolor{white}%" + "\n"
    r"{{#1|#2|#3}}}}}%"
))
data = [[r"\RGB{%s}{%s}{%s}" % ((x, 0, y)) for y in range(0, 256, 51)]
        for x in range(0, 256, 51)]
dtol.table(
    data, "", "RGB boxes with varying R and B channels",
    use_siunitx=False, escape_cells=False
)
dtol.finish("table_cells_with_macros")
