from typing import Any

import matplotlib.pyplot as plt
import numpy as np

import data2latex as dtol


# https://stackoverflow.com/a/11352216/9318084
def moving_average(interval: Any, window_size: Any) -> Any:
    window = np.ones(int(window_size)) / float(window_size)
    return np.convolve(
        interval, window, "same"
    )  # pyright: ignore [reportUnknownVariableType]


N = 100
n = 3
X = np.linspace(0, 100, N)
Y = [
    (k * moving_average(y, 10) / 2)
    for y, k in zip(np.random.uniform(0, 100, (n, N)), range(2, 2 + n))
]

# dtol.use_multi_page_standalone()
# dtol.use_one_page_standalone()

dtol.plot(
    [X] * n,
    Y,
    "Different line colors",
    "Time $t$ [s]",
    "Position $x$ [mm]",
    line="-",
    mark=None,
    grid="_",
    legend=[r"$\alpha$", r"$\beta$", r"$\gamma$"],
    width="12cm",
    height="8cm",
    xlimits="exact",
    ylimits=(0, None),
)
dtol.plot(
    [X] * n,
    Y,
    "Different line styles",
    "Time $t$ [s]",
    "Position $x$ [mm]",
    line=["-", "--", "-."],
    line_color="black",
    mark=None,
    grid="_",
    legend=[r"$\alpha$", r"$\beta$", r"$\gamma$"],
    width="12cm",
    height="8cm",
    xlimits="exact",
    ylimits=(0, None),
)
try:
    dtol.finish("plotting")
except:
    print("COMPILATION ERROR")

# plt.plot(  # pyright: ignore [reportUnknownMemberType]
#     np.array([X] * n).T, np.array(Y).T, "-"
# )
# plt.show()  # pyright: ignore [reportUnknownMemberType]
