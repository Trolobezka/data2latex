from itertools import product

import pandas as pd
import pylatex as tex  # pyright: ignore [reportMissingTypeStubs]

import data2latex as dtol

header = ["Cat", "Dog", "Rabbit"]
animals = pd.DataFrame([["a" * 9, "b" * 9, "c" * 9]] * 3, header, header)

# dtol.use_multi_page_standalone()
# dtol.use_one_page_standalone()

# for dir, bold, align in product(["top", "left"], [True, False], ["l", "c", "r"]):
for top_bold, top_align, left_bold, left_align in product(
    [True, False], ["l", "c", "r"], [True, False], ["l", "c", "r"]
):
    cap = tex.utils.escape_latex(  # pyright: ignore [reportUnknownMemberType]
        f"{top_bold},{top_align},{left_bold},{left_align}"
    )
    dtol.table(
        animals,  # pyright: ignore [reportGeneralTypeIssues]
        caption=rf"\texttt{{{cap}}}",
        escape_caption=False,
        str_try_number=False,
        top_head_bold=top_bold,
        top_head_col_align=top_align,  # pyright: ignore [reportGeneralTypeIssues]
        left_head_bold=left_bold,
        left_head_col_align=left_align,  # pyright: ignore [reportGeneralTypeIssues]
    )
    # cap = tex.utils.escape_latex(  # pyright: ignore [reportUnknownMemberType]
    #     f"dir={dir},bold={bold},align={align}"
    # )
    # if dir == "top":
    #     dtol.table(
    #         animals,
    #         caption=rf"\texttt{{{cap}}}",
    #         escape_caption=False,
    #         str_try_number=False,
    #         top_head_bold=bold,
    #         top_head_col_align=align,
    #     )
    # else:
    #     dtol.table(
    #         animals,
    #         caption=rf"\texttt{{{cap}}}",
    #         escape_caption=False,
    #         str_try_number=False,
    #         left_head_bold=bold,
    #         left_head_col_align=align,
    #     )

try:
    dtol.finish("header_style")
except:
    print("COMPILATION ERROR")
