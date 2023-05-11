from itertools import cycle
from numbers import Integral, Number
from typing import Any, Dict, Iterable, List, Literal, Optional, Tuple, TypeAlias, Union

from pylatex import (  # pyright: ignore [reportMissingTypeStubs]
    Axis,
    Command,
    Package,
    Plot,
    TikZ,
)
from pylatex.base_classes import Float  # pyright: ignore [reportMissingTypeStubs]
from pylatex.utils import NoEscape  # pyright: ignore [reportMissingTypeStubs]

from .dm import gdm
from .environments import CenteringFlagCommand, Label2, SetLengthCommand
from .iter_protocols import dict2str

#
# TypeAliases for input parameters for plot function
#

Numeric: TypeAlias = Union[int, Integral, float, Number]

NamedColor: TypeAlias = Literal[
    "red",
    "green",
    "blue",
    "cyan",
    "magenta",
    "yellow",
    "black",
    "gray",
    "white",
    "darkgray",
    "lightgray",
    "brown",
    "lime",
    "olive",
    "orange",
    "pink",
    "purple",
    "teal",
    "violet",
]
Color: TypeAlias = Union[NamedColor, Tuple[int, int, int], Tuple[float, float, float]]

MarkStyle: TypeAlias = Literal[
    "*",
    "x",
    "+",
    "-",
    "|",
    "o",
    "asterisk",
    "star",
    "10-pointed star",
    "oplus",
    "oplus*",
    "otimes",
    "otimes*",
    "square",
    "square*",
    "triangle",
    "triangle*",
    "diamond",
    "diamond*",
    "halfdiamond*",
    "halfsquare*",
    "halfsquare right*",
    "halfsquare left*",
    "Mercedes star",
    "Mercedes star flipped",
    "halfcircle",
    "halfcircle*",
    "pentagon",
    "pentagon*",
    "ball",
]

LineStyle: TypeAlias = Literal[
    "-",
    "--l",
    "--",
    "--d",
    ".l",
    ".",
    ".d",
    "-.l",
    "-.",
    "-.d",
    "-..l",
    "-..",
    "-..d",
]

line_symbol_to_style: Dict[str, str] = {
    "-": "solid",
    "--l": "loosely dashed",
    "--": "dashed",
    "--d": "densely dashed",
    ".l": "loosely dotted",
    ".": "dotted",
    ".d": "densely dotted",
    "-.l": "loosely dashdotted",
    "-.": "dashdotted",
    "-.d": "densely dashdotted",
    "-..l": "loosely dashdotdotted",
    "-..": "dashdotdotted",
    "-..d": "densely dashdotdotted",
}

Anchor: TypeAlias = Literal[
    # Inside of plot
    "south west",
    "south",
    "south east",
    "north west",
    "north",
    "north east",
    "west",
    "east",
    "center",
    # Outside of plot
    "outer south west",
    "outer south",
    "outer south east",
    "outer north west",
    "outer north",
    "outer north east",
    "outer west",
    "outer east",
    "outer center",
    # Further outside of plot
    "below south west",
    "below south",
    "below south east",
    "above north west",
    "above north",
    "above north east",
    "right of north east",
    "right of east",
    "right of south east",
    "left of north west",
    "left of west",
    "left of south west",
]

LegendPosition: TypeAlias = Literal[
    "top left", "top left out", "top right", "down left", "down right"
]

legend_dir_to_pos: Dict[str, str] = {
    "top left": "north west",
    "top left out": "outer north west",
    "top right": "north east",
    "down left": "south west",
    "down right": "south east",
}

# Stephen Few - Show Me the Numbers
default_colors: List[Color] = [
    (93, 165, 218),
    (250, 164, 58),
    (96, 189, 104),
    (241, 124, 176),
]

AxisMode: TypeAlias = Literal["lin", "log"]

axis_mode_short_to_long: Dict[str, str] = {
    "lin": "linear",
    "log": "log",
}

#
# Helper functions
#


def roundN(x: Numeric, n: int) -> Numeric:
    y = 10**n
    return round(x * y) / y


def process_data(
    data: Any, name: str = "data"
) -> Tuple[Iterable[Iterable[Numeric]], List[int]]:
    if not isinstance(data, Iterable):
        raise ValueError("X must be at least iterable.")
    lengths: List[int] = []
    outer_length: int = 0
    for i, x in enumerate(  # pyright: ignore [reportUnknownVariableType]
        data  # pyright: ignore [reportUnknownArgumentType]
    ):
        if isinstance(x, Iterable):
            if len(lengths) != outer_length:
                raise ValueError(
                    f"Found a Sequence: '{name}[{i}]=[...]', expected a Number based on the data so far."
                )
            inner_length: int = 0
            for j, y in enumerate(  # pyright: ignore [reportUnknownVariableType]
                x  # pyright: ignore [reportUnknownArgumentType]
            ):
                if not isinstance(y, Number):
                    raise ValueError(
                        f"Found a non-numeric/sequence entry: '{name}[{i},{j}]={y}'."
                    )
                inner_length += 1
            lengths.append(inner_length)
        elif not isinstance(x, Number):
            raise ValueError(f"Found a non-numeric/sequence entry: '{name}[{i}]={x}'.")
        elif len(lengths) > 0:
            raise ValueError(
                f"Found a Number: '{name}[{i}]={x}', expected a Sequence based on the data so far."
            )
        outer_length += 1
    if len(lengths) == 0:
        lengths.append(outer_length)
        data = [data]
    return (data, lengths)  # pyright: ignore [reportUnknownVariableType]


def check_data_lengths(x_lengths: List[int], y_lengths: List[int]) -> None:
    if len(x_lengths) != len(y_lengths):
        raise ValueError(
            f"X and Y data has different number of entries, counted {len(x_lengths)} for X and {len(y_lengths)} for Y."
        )
    for i, (xl, yl) in enumerate(zip(x_lengths, y_lengths)):
        if xl != yl:
            raise ValueError(
                f"Found an entry with different number of X and Y coordinates: 'len(X[{i}])={xl}' and 'len(Y[{i}])={yl}'."
            )


def create_cycle_iter(attribute: Any) -> "cycle[Any]":
    if not isinstance(attribute, list):
        attribute = [attribute]
    return cycle(attribute)  # pyright: ignore [reportUnknownArgumentType]


def rgb2mixcolor(color: Union[Tuple[int, int, int], Tuple[float, float, float]]) -> str:
    if (
        not isinstance(color, tuple)  # pyright: ignore [reportUnnecessaryIsInstance]
        or len(color) != 3
    ):
        raise ValueError("Invalid color. Expected tuple with 3 numeric values.")
    r, g, b = 0, 0, 0
    if isinstance(color[0], int):
        r, g, b = (min(max(round(x), 0), 255) for x in color)
    elif isinstance(color[0], float):  # pyright: ignore [reportUnnecessaryIsInstance]
        r, g, b = (min(max(round(255 * x), 0), 255) for x in color)
    return f"rgb,255:red,{r};green,{g};blue,{b}"


# https://stackoverflow.com/a/214657/9318084
def hex2rgb(value: str) -> Tuple[int, int, int]:
    value = value.lstrip("#")
    _len = len(value)
    if _len != 6:
        raise ValueError(
            f"Expected color in hex format with 6 characters, input: '{value}'."
        )
    return tuple(int(value[i : i + 2], 16) for i in [0, 2, 4])


def handle_color(color: Union[None, Color, List[Union[None, Color]]]) -> List[str]:
    if not isinstance(color, list):
        color = [color]
    valid_colors: List[Any] = [None] * len(color)
    for i, c in enumerate(color):
        if c is None:
            valid_colors[i] = "none"
        elif isinstance(c, tuple):
            valid_colors[i] = rgb2mixcolor(c)
        elif isinstance(c, str):  # pyright: ignore [reportUnnecessaryIsInstance]
            if (
                c
                in NamedColor.__args__  # pyright: ignore [reportUnknownMemberType, reportGeneralTypeIssues]
            ):
                valid_colors[i] = c
            else:
                valid_colors[i] = rgb2mixcolor(hex2rgb(c))
        else:
            valid_colors[i] = str(c)
    return valid_colors


def decode_grid_style_code(code: str) -> Dict[str, Optional[str]]:
    options: Dict[str, Any] = {
        "xmajorgrids": None,
        "xminorgrids": None,
        "xminorticks": None,
        "minor x tick num": None,
        "ymajorgrids": None,
        "yminorgrids": None,
        "yminorticks": None,
        "minor y tick num": None,
    }
    axis: Optional[str] = None
    code = code.lower().replace("v", "|").replace("h", "_")
    for i, letter in enumerate(code):
        if letter == "|":
            axis = "x"
            options["xmajorgrids"] = True
        elif letter == "_":
            axis = "y"
            options["ymajorgrids"] = True
        elif letter == "#":
            options["xmajorgrids"] = True
            options["ymajorgrids"] = True
            axis = "both"
        else:
            num: int = -1
            try:
                num = int(letter)
            except ValueError:
                pass
            if axis is None:
                raise ValueError(f"Number with no axis specifier found at index {i}.")
            elif axis == "both":
                options["xminorgrids"] = True
                options["yminorgrids"] = True
                options["xminorticks"] = True
                options["yminorticks"] = True
                options["minor x tick num"] = num
                options["minor y tick num"] = num
            else:
                options[f"{axis}minorgrids"] = True
                options[f"{axis}minorticks"] = True
                options[f"minor {axis} tick num"] = num
    return {k: str(v).lower() if v is not None else None for k, v in options.items()}


def pgf_fixed_number_format(precision: int, zerofill: bool) -> Dict[str, Optional[str]]:
    return {
        "/pgf/number format/.cd": "",
        "fixed": "",
        "fixed zerofill": "" if zerofill else None,
        "precision": str(precision),
    }


#
# Plot function
#


def plot(
    _X: Any,
    _Y: Any,
    caption: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    grid: Optional[str] = None,
    mode: Union[AxisMode, Tuple[AxisMode, AxisMode]] = ("lin", "lin"),
    legend: Union[None, str, List[Union[None, str]]] = None,
    legend_pos: LegendPosition = "top right",
    legend_entry_align: Literal["l", "c", "r"] = "c",
    width: Optional[str] = None,
    height: Optional[str] = None,
    equal_axis: bool = False,
    xlimits: Optional[
        Union[Tuple[Optional[float], Optional[float]], Literal["exact"]]
    ] = None,
    ylimits: Optional[
        Union[Tuple[Optional[float], Optional[float]], Literal["exact"]]
    ] = None,
    precision: Union[int, Tuple[int, int]] = (2, 2),
    zerofill: Union[bool, Tuple[bool, bool]] = (False, False),
    label: Optional[str] = None,
    caption_pos: Literal["above", "below"] = "below",
    escape_caption: bool = True,
    position: str = "H",
    center: bool = True,
    line: Union[None, LineStyle, List[Union[None, LineStyle]]] = None,
    line_width: Union[str, List[str]] = "0.75pt",
    line_color: Union[None, Color, List[Union[None, Color]]] = ["blue", "red", "black"],
    line_opacity: Union[float, List[float]] = 1.0,
    mark: Union[None, MarkStyle, List[Union[None, MarkStyle]]] = "*",
    mark_size: Union[str, List[str]] = "2pt",
    mark_fill_color: Union[None, Color, List[Union[None, Color]]] = [
        "blue",
        "red",
        "black",
    ],
    mark_stroke_color: Union[None, Color, List[Union[None, Color]]] = None,
    mark_fill_opacity: Union[float, List[float]] = 1.0,
    mark_stroke_opacity: Union[float, List[float]] = 0.0,
) -> None:
    X, x_lengths = process_data(_X, "X")
    Y, y_lengths = process_data(_Y, "Y")
    check_data_lengths(x_lengths, y_lengths)
    lengths = x_lengths
    del x_lengths
    del y_lengths

    # show_extra_x_ticks: bool = False
    # show_extra_y_ticks: bool = False
    if xlimits == "exact":
        xmax, xmin = float("-inf"), float("inf")
        for x in X:
            xmax = max(xmax, max(x))  # pyright: ignore [reportGeneralTypeIssues]
            xmin = min(xmin, min(x))  # pyright: ignore [reportGeneralTypeIssues]
        xlimits = (xmin, xmax)
        # show_extra_x_ticks = True
    if ylimits == "exact":
        ymax, ymin = float("-inf"), float("inf")
        for y in Y:
            ymax = max(ymax, max(y))  # pyright: ignore [reportGeneralTypeIssues]
            ymin = min(ymin, min(y))  # pyright: ignore [reportGeneralTypeIssues]
        ylimits = (ymin, ymax)
        # show_extra_y_ticks = True

    if not isinstance(legend, list):
        legend = [legend]
    if not isinstance(mode, tuple):
        mode = (mode, mode)
    if not isinstance(precision, tuple):
        precision = (precision, precision)
    if not isinstance(zerofill, tuple):
        zerofill = (zerofill, zerofill)

    line_iter = create_cycle_iter(line)
    line_width_iter = create_cycle_iter(line_width)
    line_color_iter = create_cycle_iter(handle_color(line_color))
    line_opacity_iter = create_cycle_iter(line_opacity)
    mark_iter = create_cycle_iter(mark)
    mark_size_iter = create_cycle_iter(mark_size)
    mark_fill_color_iter = create_cycle_iter(handle_color(mark_fill_color))
    mark_stroke_color_iter = create_cycle_iter(handle_color(mark_stroke_color))
    mark_fill_opacity_iter = create_cycle_iter(mark_fill_opacity)
    mark_stroke_opacity_iter = create_cycle_iter(mark_stroke_opacity)

    #
    # Plot creation
    #
    plots: List[Plot] = []
    for length, x_iter, y_iter in zip(lengths, X, Y):
        if length == 0:
            continue

        next_line = next(line_iter)
        next_line_width = next(line_width_iter)
        next_line_color = next(line_color_iter)
        next_line_opacity = next(line_opacity_iter)
        next_mark = next(mark_iter)
        next_mark_size = next(mark_size_iter)
        next_mark_fill_color = next(mark_fill_color_iter)
        next_mark_stroke_color = next(mark_stroke_color_iter)
        next_mark_fill_opacity = next(mark_fill_opacity_iter)
        next_mark_stroke_opacity = next(mark_stroke_opacity_iter)

        next_line = line_symbol_to_style.get(next_line, next_line)

        plot_options: Dict[str, Any] = {}
        # Apply styles (options with no value)
        if next_line is None and next_mark is not None:
            plot_options["only marks"] = ""
        if next_line is not None:
            plot_options[next_line] = ""
        if next_mark is None:
            plot_options["no markers"] = ""
        plot_options.update(
            {
                # Marker options
                "mark": next_mark,
                "mark options": {
                    "solid": "",  # Marker stroke style
                    "fill": next_mark_fill_color,
                    "fill opacity": next_mark_fill_opacity,
                    "draw": next_mark_stroke_color,
                    "draw opacity": next_mark_stroke_opacity,
                },
                "mark size": next_mark_size,
                # Line options
                "fill": "none",
                "fill opacity": "0.0",
                "draw": next_line_color,
                "draw opacity": next_line_opacity,
                "line join": "round",
                "line cap": "round",
                "line width": next_line_width,
            }
        )

        # Circumvent pgfplots restriction
        # Manual 1.18.1: "Up to now, plot marks always have a stroke color
        # (some also have a fill color). This restriction may be lifted in upcoming versions."
        if (
            plot_options["mark options"]["fill"] == "none"
            or next_mark_fill_color == None
        ):
            plot_options["mark options"]["fill opacity"] = 0.0
        if (
            plot_options["mark options"]["draw"] == "none"
            or next_mark_stroke_color == None
        ):
            plot_options["mark options"]["draw opacity"] = 0.0
        if plot_options["draw"] == "none" or next_line == None:
            plot_options["draw opacity"] = 0.0

        plots.append(
            Plot(
                coordinates=zip(x_iter, y_iter),
                options=NoEscape(dict2str(plot_options)),
            )
        )

    #
    # General axis settings
    #
    axis_options: Dict[str, Any] = {
        "width": None if width is None else width,
        "height": None if height is None else height,
        # Axis settings
        "xlabel": xlabel,
        "ylabel": ylabel,
        "xmin": None if xlimits is None else xlimits[0],
        "xmax": None if xlimits is None else xlimits[1],
        "ymin": None if ylimits is None else ylimits[0],
        "ymax": None if ylimits is None else ylimits[1],
        "xmode": axis_mode_short_to_long.get(mode[0], mode[0]),
        "ymode": axis_mode_short_to_long.get(mode[1], mode[1]),
        "scaled ticks": "false",
        "axis equal": str(equal_axis).lower(),
        # "max space between x ticks": "60pt",
        # Legend settings
        "legend entries": ",".join(
            [f"{{{x}}}" if x is not None else "{}" for x in legend]
        ),
        "legend pos": legend_dir_to_pos.get(legend_pos, legend_pos),
        "legend columns": "1",  # -1 for fully horizontal legend
        "legend plot pos": "left",  # left|right|none
        "legend cell align": {"l": "left", "c": "center", "r": "right"}.get(
            legend_entry_align, legend_entry_align
        ),
    }

    # This could work but I think it is not that important.
    # The solution could be to calculate ticks manually.
    # if xlimits is not None and show_extra_x_ticks:
    #     axis_options.update(
    #         {
    #             "extra x ticks": f"{','.join([str(roundN(x, precision[0])) for x in xlimits])}",
    #             "enlarge x limits": 2 / ((xlimits[1] - xlimits[0]) * 10 ** precision[0]),
    #         }
    #     )
    # if ylimits is not None and show_extra_y_ticks:
    #     axis_options.update(
    #         {
    #             "extra y ticks": f"{','.join([str(roundN(y, precision[0])) for y in ylimits])}",
    #             "enlarge y limits": 2 / ((ylimits[1] - ylimits[0]) * 10 ** precision[1]),
    #         }
    #     )

    #
    # Number format settings
    #
    universal_log_settings: bool = False
    if ((mode[0] == "log") != (mode[1] == "log")) or (  # XOR: (bool) != (bool)
        mode[0] == "log"
        and mode[0] == "log"
        and precision[0] == precision[1]
        and zerofill[0] == zerofill[1]
    ):
        # Apply these settings if only one axis is logaritmic or
        # both are logaritmic and have the same precision and zerofill.
        i: int = 0 if mode[0] == "log" else 1
        axis_options["log plot exponent style/.style"] = pgf_fixed_number_format(
            precision[i], zerofill[i]
        )
        universal_log_settings = True
    for i, axis in [(0, "x"), (1, "y")]:
        if mode[i] == "lin":
            axis_options[f"{axis}ticklabel style"] = pgf_fixed_number_format(
                precision[i], zerofill[i]
            )
        elif mode[i] == "log" and not universal_log_settings:
            # This is bit of a hack for setting different exponent formats
            # for each of the logaritmic axis.
            # https://tex.stackexchange.com/a/656091/229475
            axis_options[f"{axis}ticklabel"] = (
                "\n\t"
                + r"\pgfkeys{"
                + dict2str(pgf_fixed_number_format(precision[i], zerofill[i]), level=2)
                + "\t"
                # I removed an unmatched bracket which was placed after "\logten" <- ")" and it still works
                + r"} $10^{\pgfmathparse{\tick/\logten}\pgfmathprintnumber{\pgfmathresult}}$"
            )

    #
    # Major/minor grid and tick settings
    #
    if grid is None:
        axis_options["grid"] = "none"
    else:
        # There is a problem with setting exact number of minor ticks
        # on logaritmic axis. There is either zero or 8 minor tick
        # whatever you do here. Solution could be to set the tick
        # values manually.
        axis_options.update(decode_grid_style_code(grid.strip()))

    #
    # Creation of LaTeX environments
    #
    figure = Float(position=position)
    figure._latex_name = "figure"  # pyright: ignore [reportPrivateUsage]
    figure.packages.append(  # pyright: ignore [reportUnknownMemberType]
        Package("float")
    )

    if center:
        figure.append(  # pyright: ignore [reportUnknownMemberType]
            CenteringFlagCommand()
        )

    if caption is not None:
        figure.append(  # pyright: ignore [reportUnknownMemberType]
            SetLengthCommand("abovecaptionskip", "1pt plus 1pt minus 1pt")
        )
        figure.append(  # pyright: ignore [reportUnknownMemberType]
            SetLengthCommand("belowcaptionskip", "5pt plus 2pt minus 2pt")
        )
        if caption_pos == "above":
            if escape_caption:
                figure.add_caption(caption)  # pyright: ignore [reportUnknownMemberType]
            else:
                figure.add_caption(  # pyright: ignore [reportUnknownMemberType]
                    NoEscape(caption)
                )
    axis = Axis(
        data=plots,
        options=NoEscape(dict2str(axis_options)),
    )
    axis.packages.append(Command("usetikzlibrary", "plotmarks"))
    tikz = TikZ(
        data=axis,
        options=NoEscape(
            dict2str(
                {
                    # These settings offset the figure body so that it can
                    # be centred relative to the text (e.g. caption).
                    "trim axis left": "",
                    "trim axis right": "",
                }
            )
        ),
    )
    figure.append(tikz)  # pyright: ignore [reportUnknownMemberType]

    if caption is not None and caption_pos == "below":
        if escape_caption:
            figure.add_caption(caption)  # pyright: ignore [reportUnknownMemberType]
        else:
            figure.add_caption(  # pyright: ignore [reportUnknownMemberType]
                NoEscape(caption)
            )

    if label is not None:
        figure.append(  # pyright: ignore [reportUnknownMemberType]
            Label2(label, "plot")
        )

    gdm().append(figure)
