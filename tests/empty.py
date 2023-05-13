import traceback

import numpy as np
import pandas as pd

import data2latex as dtol


def try_excute(command: str) -> None:
    print("\nRUNNING:", command, "\n")
    try:
        exec(command)
        dtol.text(command)
        print("FINISHED")
    except:
        print(
            "\n".join(["\t" * 1 + exc for exc in traceback.format_exc().splitlines()])
        )


#
# Empty
#

# table: lists
try_excute("dtol.table([])")
try_excute("dtol.table([[]])")
try_excute("dtol.table([[], []])")

# table: arrays
try_excute("dtol.table(np.array([]))")
try_excute("dtol.table(np.array([[]]))")
try_excute("dtol.table(np.array([[], []]))")

# table: dataframes
try_excute("dtol.table(pd.DataFrame([]))")
try_excute("dtol.table(pd.DataFrame([[]]))")
try_excute("dtol.table(pd.DataFrame([[], []]))")

# table: dataframes with headers
try_excute("dtol.table(pd.DataFrame([], ['A'], ['B']))")

# plot: lists
try_excute("dtol.plot([], [])")
try_excute("dtol.plot([[]], [[]])")
try_excute("dtol.plot([[], []], [[], []])")

# plot: arrays
try_excute("dtol.plot(np.array([]), np.array([]))")
try_excute("dtol.plot(np.array([[]]), np.array([[]]))")
try_excute("dtol.plot(np.array([[], []]), np.array([[], []]))")

# plot: dataframes
try_excute("dtol.plot(pd.DataFrame([]), pd.DataFrame([]))")
try_excute("dtol.plot(pd.DataFrame([[]]), pd.DataFrame([[]]))")
try_excute("dtol.plot(pd.DataFrame([[], []]), pd.DataFrame([[], []]))")

# plot: dataframes as arrays
try_excute("dtol.plot(pd.DataFrame([]).__array__(), pd.DataFrame([]).__array__())")
try_excute("dtol.plot(pd.DataFrame([[]]).__array__(), pd.DataFrame([[]]).__array__())")
try_excute(
    "dtol.plot(pd.DataFrame([[], []]).__array__(), pd.DataFrame([[], []]).__array__())"
)

# plot: dataframes with headers
try_excute("dtol.plot(pd.DataFrame([], ['A'], ['B']), pd.DataFrame([], ['A'], ['B']))")
try_excute(
    "dtol.plot(pd.DataFrame([], ['A'], ['B']).__array__(), pd.DataFrame([], ['A'], ['B']).__array__())"
)

#
# One entry
#

# table: lists
try_excute("dtol.table([0])")
try_excute("dtol.table([[0]])")
try_excute("dtol.table([[0], [0]])")

# table: arrays
try_excute("dtol.table(np.array([0]))")
try_excute("dtol.table(np.array([[0]]))")
try_excute("dtol.table(np.array([[0], [0]]))")

# table: dataframes
try_excute("dtol.table(pd.DataFrame([0]))")
try_excute("dtol.table(pd.DataFrame([[0]]))")
try_excute("dtol.table(pd.DataFrame([[0], [0]]))")

# table: dataframes with headers
try_excute("dtol.table(pd.DataFrame([0], ['A'], ['B']))")

# plot: lists
try_excute("dtol.plot([0], [0])")
try_excute("dtol.plot([[0]], [[0]])")
try_excute("dtol.plot([[0], [0]], [[0], [0]])")

# plot: arrays
try_excute("dtol.plot(np.array([0]), np.array([0]))")
try_excute("dtol.plot(np.array([[0]]), np.array([[0]]))")
try_excute("dtol.plot(np.array([[0], [0]]), np.array([[0], [0]]))")

# plot: dataframes
try_excute("dtol.plot(pd.DataFrame([0]), pd.DataFrame([0]))")
try_excute("dtol.plot(pd.DataFrame([[0]]), pd.DataFrame([[0]]))")
try_excute("dtol.plot(pd.DataFrame([[0], [0]]), pd.DataFrame([[0], [0]]))")

# plot: dataframes as arrays
try_excute("dtol.plot(pd.DataFrame([0]).__array__(), pd.DataFrame([0]).__array__())")
try_excute(
    "dtol.plot(pd.DataFrame([[0]]).__array__(), pd.DataFrame([[0]]).__array__())"
)
try_excute(
    "dtol.plot(pd.DataFrame([[0], [0]]).__array__(), pd.DataFrame([[0], [0]]).__array__())"
)

# plot: dataframes with headers
try_excute(
    "dtol.plot(pd.DataFrame([0], ['A'], ['B']), pd.DataFrame([0], ['A'], ['B']))"
)
try_excute(
    "dtol.plot(pd.DataFrame([0], ['A'], ['B']).__array__(), pd.DataFrame([0], ['A'], ['B']).__array__())"
)

# Comment this out, run, read the exceptions, uncomment, try to compile
try:
    dtol.finish("empty")
except:
    print("COMPILATION ERROR")
