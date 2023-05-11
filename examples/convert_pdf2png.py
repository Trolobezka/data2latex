import os
from glob import glob
from subprocess import run

os.chdir(os.path.abspath("./examples"))

for file in glob("*.pdf"):
    run(
        f"C:/Program Files/ImageMagick-7.1.0-Q16-HDRI/convert.exe -density 300 -background white -alpha remove {file} ../docs/_static/img/{file}.png"
    )
    print(file, "done")
