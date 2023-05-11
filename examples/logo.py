import os
from subprocess import run

os.chdir(os.path.abspath("./examples"))

document = r"""
\documentclass[12pt,border=1pt]{standalone}
\begin{document}
$\Delta$\texttt{ata2}\LaTeX{}
\end{document}
"""
with open("logo.tex", "w") as f:
    f.write(document)
run("latexmk --pdf --interaction=nonstopmode logo.tex")
run("latexmk -c logo.tex")
