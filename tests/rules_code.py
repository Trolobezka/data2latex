import pandas as pd
import pylatex as tex  # pyright: ignore [reportMissingTypeStubs]

import data2latex as dtol

header = ["Cat", "Dog", "Rabbit"]
animals = pd.DataFrame([[True, 0, 0], [0, "a", 0], [0, 0, 12.345]], header, header)

for rules in [
    "",
    "#",
    "O",
    "o",
    "|A_A",
    "|a_a",
    "|B_B",
    "|b_b",
    "|13_1",
    "_13|1",
    "|2_2",
]:
    cap = tex.utils.escape_latex(  # pyright: ignore [reportUnknownMemberType]
        f"rules={rules}"
    )
    dtol.table(
        animals,
        rules=rules,
        caption=rf"\texttt{{{cap}}}",
        escape_caption=False,
        str_try_number=False,
    )

try:
    dtol.finish("rules_code")
except:
    print("COMPILATION ERROR")
