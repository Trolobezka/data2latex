from numbers import Integral, Number
from typing import Any, Callable, Dict, List, Literal, Optional, Union, cast, Set

from pylatex import Table, Package  # pyright: ignore [reportMissingTypeStubs]
from pylatex.utils import (  # pyright: ignore [reportMissingTypeStubs]
    NoEscape,
    escape_latex,  # pyright: ignore [reportUnknownVariableType]
)

from .dm import gdm
from .environments import (
    AdjustBoxCommand,
    CenteringFlagCommand,
    Label2,
    Parameters2,
    SetLengthCommand,
    tblr,
)
from .iter_protocols import (
    DataFrameIterator,
    DataFrameLike,
    KnownLengthIterable,
    KnownLengthIterable2D,
    NDArrayLike,
    OuterKnownLengthIterable,
    Sequence2D,
    dict2str,
)


class Rule:
    INNER_BODY = 0
    BEFORE_HEADER = 1
    AFTER_HEADER = 2
    AFTER_BODY = 3
    COL = "v"
    ROW = "h"
    ALLOWED: Set[int] = {0, 1, 2, 3}


def set_add(s: Optional[Set[int]], num: Union[int, List[int]], i: int) -> None:
    if not isinstance(num, list):
        num = [num]
    if s is None:
        raise ValueError(f"Number with no direction specifier found at index {i}.")
    elif len(set(num).difference(Rule.ALLOWED)) != 0:
        raise ValueError(f"Invalid number found at index {i}.")
    else:
        s.update(num)


def decode_rule_style_code(code: str) -> Dict[Literal["v", "h"], Set[int]]:
    v: Set[int] = set()
    h: Set[int] = set()
    last_seen: Optional[Set[int]] = None
    code = code.replace("V", "v").replace("H", "h")
    for i, letter in enumerate(code):
        if letter == "|" or letter == "v":
            last_seen = v
        elif letter == "_" or letter == "h":
            last_seen = h
        elif letter == "#":
            set_add(v, [0, 1, 2, 3], i)
            set_add(h, [0, 1, 2, 3], i)
        elif letter == "O":
            set_add(v, [1, 3], i)
            set_add(h, [1, 3], i)
        elif letter == "o":
            set_add(v, [2, 3], i)
            set_add(h, [2, 3], i)
        elif letter == "A":
            set_add(last_seen, [0, 1, 2, 3], i)
        elif letter == "a":
            set_add(last_seen, [0, 2], i)
        elif letter == "B":
            set_add(last_seen, [0, 2, 3], i)
        elif letter == "b":
            set_add(last_seen, [0], i)
        else:
            num: int = -1
            try:
                num = int(letter)
            except ValueError:
                pass
            set_add(last_seen, num, i)
    return {"v": v, "h": h}


def table(
    data: Union[
        Sequence2D,
        KnownLengthIterable2D,
        DataFrameIterator,
        DataFrameLike,
        NDArrayLike,
    ],
    rules: str = "",
    caption: Optional[str] = None,
    caption_pos: Literal["above", "below"] = "above",
    escape_caption: bool = True,
    label: Optional[str] = None,
    position: str = "H",
    center: bool = True,
    float_format: str = "{:0.3f}",
    str_format: str = "{{{{{{{:s}}}}}}}",  # siunitx wants text enclosed in {{{...}}}
    str_convertor: Callable[[Any], str] = str,
    str_try_number: bool = True,
    escape_cells: bool = True,
    col_align: Literal["l", "c", "r", "j"] = "c",
    row_align: Literal["t", "m", "b", "h", "f"] = "m",
    left_head_bold: bool = False,
    left_head_col_align: Optional[Literal["l", "c", "r", "j"]] = None,
    top_head_bold: bool = False,
    top_head_col_align: Optional[Literal["l", "c", "r", "j"]] = None,
    use_adjustbox: bool = True,
    use_siunitx: bool = True,
    dataframe_column_names: bool = True,
    dataframe_row_names: bool = True,
) -> None:
    """
    Generate LaTeX table from input data. Table is created with ``tabularray`` package (``tblr`` environment) with optional ``siunitx`` usage for decimal number alignment. Table can be automatically scaled down with ``adjustbox`` package.

    **Examples of usage**

    .. highlight:: python
    .. code-block:: python

        import data2latex as dtol
        data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        dtol.table(data)
        dtol.finish()

    .. highlight:: python
    .. code-block:: python

        import data2latex as dtol
        data = pd.DataFrame(
            [["purple", "cyan"], ["blue", "yellow"]],
            ["C1", "C2"], ["R1", "R2"]
        )
        dtol.table(
            data,
            caption="Data from pandas.DataFrame",
            rules="|2_2",
            top_head_bold=True,
            left_head_bold=True,
        )
        dtol.finish()

    :param data: 2D structure holding your data. Supported data types are ``List[List[Any]]``, ``numpy.ndarray{ndim >= 2}`` and ``pandas.DataFrame``.
    :type data: Union[Sequence2D, KnownLengthIterable2D, DataFrameIterator, DataFrameLike, NDArrayLike]

    :param rules: Rule settings using custom syntax, defaults to ``""``.

        ======  ======
        Symbol  Meaning
        ======  ======
        ``|``   Select the vertical rules.
        ``_``   Select the horizontal rules.
        ``1``   Apply rule before header in selected direction.
        ``2``   Apply rule after header in selected direction.
        ``3``   Apply rule after table body in selected direction.
        ``A``   Apply every rule in selected direction.
        ``a``   Apply every rule in selected direction except the border ones.
        ``B``   Apply every rule in table body in selected direction.
        ``b``   Apply every rule in table body in selected direction except the border ones.
        ``#``   Apply every rule in both direction, every cell has full border.
        ``O``   Apply every rule around table.
        ``o``   Apply every rule around table body.
        ======  ======

        Symbols ``#``, ``O``, ``o`` don't need selected direction.

    :type rules: str, optional

    :param caption: Caption text, defaults to ``None``.
    :type caption: Optional[str], optional

    :param caption_pos: Position caption above or below the table, defaults to ``"above"``.
    :type caption_pos: Literal["above", "below"], optional

    :param escape_caption: ``True`` for escaping special LaTeX symbols in caption text, defaults to ``True``.
    :type escape_caption: bool, optional

    :param label: Label for later referencing, use format ``"prefix:label"`` or just ``"label"`` with automatic prefix ``"table"``, defaults to ``None``.
    :type label: Optional[str], optional

    :param position: Float position on the page for ``table`` environment, defaults to ``"h!"``.
    :type position: str, optional

    :param center: ``True`` for centering the table on the page, defaults to ``True``.
    :type center: bool, optional

    :param float_format: Format for formatting ``float`` numbers with :func:`str.format`. Here you can change the number of printed decimal places, ``int`` numbers are printed without any format, defaults to ``"{:0.3f}"``.
    :type float_format: str, optional

    :param str_format: Format for formatting strings with :func:`str.format`. Text must be enclosed in triple curly brackets if you use the ``siunitx`` package, defaults to ``"{{{{{{{:s}}}}}}}"``.
    :type str_format: str, optional

    :param str_convertor: Function for converting objects into strings, defaults to ``str``.
    :type str_convertor: Callable[[Any], str]

    :param str_try_number: ``True`` for trying to convert ``str`` to ``int`` and ``float``. This process is done after formatting numbers and converting objects into strings. Turn this off if you do not need it. Defaults to ``True``.
    :type str_try_number: bool, optional

    :param escape_cells: ``True`` for escaping every cells content, defaults to ``True``.
    :type escape_cells: bool, optional

    :param col_align: Classic column (horizontal) contenet alignment setting, defaults to ``"c"``.
    :type col_align: Literal["l", "c", "r", "j"], optional

    :param row_align: Classis row (vertical) content alignment setting, defaults to ``"m"``.
    :type row_align: Literal["t", "m", "b", "h", "f"], optional

    :param left_head_bold: ``True`` for bold left header text, defaults to ``False``.
    :type left_head_bold: bool, optional

    :param left_head_col_align: Left header text vertical alignment setting, defaults to ``None``.
    :type left_head_col_align: Optional[Literal["l", "c", "r", "j"]], optional

    :param top_head_bold: ``True`` for bold top header text, defaults to ``False``.
    :type top_head_bold: bool, optional

    :param top_head_col_align: Top header text vertical alignment setting, defaults to ``None``.
    :type top_head_col_align: Optional[Literal["l", "c", "r", "j"]], optional

    :param use_adjustbox: ``True`` for wrapping the whole ``tblr`` environment in ``adjustbox`` macro, which will shrink the table if it is wider then ``linewidth``, defaults to ``True``.
    :type use_adjustbox: bool, optional

    :param use_siunitx: ``True`` for using ``siunitx`` package for aligning numbers. To allow custom vertical alignment, we must know max number of digits each column will store. There is currently implemented some sort of heuristic approach for obtaining this information. Turn this off if you do not need it. It does not work with numbers in scientific notation. Defaults to ``True``.
    :type use_siunitx: bool, optional

    :param dataframe_column_names: ``True`` for showing column names if the input data is ``pandas.DataFrame``, defaults to ``True``.
    :type dataframe_column_names: bool, optional

    :param dataframe_row_names: ``True`` for showing row names if the input data is ``pandas.DataFrame``, defaults to ``True``.
    :type dataframe_row_names: bool, optional

    :raises ValueError: Input data must have at least two dimensions.
    :raises ValueError: Unknown input data type. Supporting ``List[List[Any]]``, ``numpy.ndarray{ndim >= 2}`` and ``pandas.DataFrame``.
    """
    #
    # Handle different types of input data
    #
    if isinstance(data, DataFrameIterator):
        pass
    elif "DataFrame" in str(type(data)) and isinstance(data, DataFrameLike):
        data = DataFrameIterator(
            data,
            include_column_names=dataframe_column_names,
            include_row_names=dataframe_row_names,
        )
    elif "ndarray" in str(type(data)) and isinstance(data, NDArrayLike):
        if data.ndim <= 1:
            raise ValueError("Input data must have at least two dimensions.")
    elif isinstance(data, OuterKnownLengthIterable) and all(
        [
            isinstance(
                x, KnownLengthIterable
            )  # pyright: ignore [reportUnnecessaryIsInstance]
            for x in data
        ]
    ):
        pass
    else:
        raise ValueError(
            "Unknown input data type. "
            "Supporting List[List[Any]], numpy.ndarray{ndim >= 2} and pandas.DataFrame."
        )
    data = cast(KnownLengthIterable2D, data)

    #
    # Build the string representation of the table
    #
    latex_data: str = ""
    max_column_count = max((len(row) for row in data))
    row_data: List[str] = [""] * max_column_count
    max_pre: List[int] = [0] * max_column_count
    max_post: List[int] = [0] * max_column_count
    for row in data:
        for i, item in enumerate(row):
            if isinstance(item, bool):
                row_data[i] = str_format.format(str(item))
            elif isinstance(item, Integral):  # standard int + numpy.int
                row_data[i] = str(item)
            elif isinstance(item, Number):
                row_data[i] = float_format.format(item)
            else:
                item2: str = ""
                converted: bool = False
                if isinstance(item, str):
                    item2 = item
                else:
                    item2 = str_convertor(item)
                if str_try_number:
                    try:
                        item2 = str(int(item2))
                        converted = True
                    except ValueError:
                        try:
                            item2 = float_format.format(float(item2))
                            converted = True
                        except ValueError:
                            converted = False
                if converted:
                    row_data[i] = item2
                else:
                    if escape_cells:
                        item2 = escape_latex(item2)
                    row_data[i] = str_format.format(item2)

            # Measuring width of the numbers for the siunitx package.
            # Doing it here so we don't skip numbers that where saved
            # as string in the original data. We will also catch all the
            # possible numbers from custom number/str_format and str_convertor().
            if use_siunitx:
                try:
                    item2 = row_data[i].strip(" {}$")
                    # float() will error on text and we will skip the max_pre/post measurement
                    float(item2)
                    parts = item2.split(".")
                    if len(parts) >= 1:
                        max_pre[i] = max(max_pre[i], len(parts[0]))
                    if len(parts) >= 2:
                        max_post[i] = max(max_post[i], len(parts[1].split("e")[0]))
                except:
                    pass
        latex_data += " & ".join(row_data) + r" \\" + "\n"

    #
    # Columns and rows configuration (align)
    #
    column_type: Dict[str, Any] = {
        "si": {"table-format": None, "table-number-alignment": None}
    }
    column_type[col_align] = ""
    if use_siunitx:
        column_type["si"]["table-number-alignment"] = {
            "l": "left",
            "c": "center",
            "r": "right",
        }.get(col_align, "center")

    rowspec: List[str] = [f"Q[{row_align}]"] * len(data)
    colspec: List[str] = [""] * max_column_count
    for i, (max_pre_i, max_post_i) in enumerate(zip(max_pre, max_post)):
        if use_siunitx:
            column_type["si"]["table-format"] = f"{max_pre_i}.{max_post_i}"
        colspec[i] = f"Q[{dict2str(column_type)}]"

    #
    # Columns and rows configuration (rules/lines)
    #
    RULES = decode_rule_style_code(rules)
    colspec_header: str = ""
    colspec_body: List[str] = []
    if len(colspec) == 0:
        pass  # Maybe error?
    elif len(colspec) == 1:
        colspec_header = colspec[0]
    else:
        colspec_header = colspec[0]
        colspec_body = colspec[1:]
    colspec = [
        "%\n",
        "|" if Rule.BEFORE_HEADER in RULES[Rule.COL] else "",
        colspec_header,
        "|" if Rule.AFTER_HEADER in RULES[Rule.COL] else "",
        ("|" if Rule.INNER_BODY in RULES[Rule.COL] else "").join(colspec_body),
        "|" if Rule.AFTER_BODY in RULES[Rule.COL] and len(colspec_body) > 0 else "",
        "%\n",
    ]
    rowspec_header: str = ""
    rowspec_body: List[str] = []
    if len(rowspec) == 0:
        pass  # Maybe error?
    elif len(rowspec) == 1:
        rowspec_header = rowspec[0]
    else:
        rowspec_header = rowspec[0]
        rowspec_body = rowspec[1:]
    rowspec = [
        "|" if Rule.BEFORE_HEADER in RULES[Rule.ROW] else "",
        rowspec_header,
        "|" if Rule.AFTER_HEADER in RULES[Rule.ROW] else "",
        ("|" if Rule.INNER_BODY in RULES[Rule.ROW] else "").join(rowspec_body),
        "|" if Rule.AFTER_BODY in RULES[Rule.ROW] and len(rowspec_body) > 0 else "",
    ]

    #
    # Columns and rows configuration (header)
    #
    additional_tblr_parameters = {}
    first_row_params: Dict[str, str] = {}
    if top_head_bold:
        first_row_params["font"] = r"\bfseries"
    if top_head_col_align is not None:
        first_row_params["halign"] = top_head_col_align
    additional_tblr_parameters["row{1}"] = Parameters2(first_row_params)
    first_col_params: Dict[str, str] = {}
    if left_head_bold:
        first_col_params["font"] = r"\bfseries"
    if left_head_col_align is not None:
        first_col_params["halign"] = left_head_col_align
    additional_tblr_parameters["column{1}"] = Parameters2(first_col_params)

    #
    # LaTeX environments completion
    #

    table = Table(position=position)
    table.packages.append(Package("float"))  # pyright: ignore [reportUnknownMemberType]
    table.separate_paragraph = False  # Fix new lines before \begin{table}

    if center:
        table.append(  # pyright: ignore [reportUnknownMemberType]
            CenteringFlagCommand()
        )

    if caption is not None:
        table.append(  # pyright: ignore [reportUnknownMemberType]
            SetLengthCommand("abovecaptionskip", "5pt plus 2pt minus 2pt")
        )
        table.append(  # pyright: ignore [reportUnknownMemberType]
            SetLengthCommand("belowcaptionskip", "5pt plus 2pt minus 2pt")
        )
        if caption_pos == "above":
            if escape_caption:
                table.add_caption(caption)  # pyright: ignore [reportUnknownMemberType]
            else:
                table.add_caption(  # pyright: ignore [reportUnknownMemberType]
                    NoEscape(caption)
                )

    tabular = tblr(
        colspec="".join(colspec),
        rowspec="".join(rowspec),
        data=NoEscape(latex_data),
        arguments=additional_tblr_parameters,
    )

    if use_adjustbox:
        adjustbox = AdjustBoxCommand(data=tabular)
        table.append(adjustbox)  # pyright: ignore [reportUnknownMemberType]
    else:
        table.append(tabular)  # pyright: ignore [reportUnknownMemberType]

    if caption is not None and caption_pos == "below":
        if escape_caption:
            table.add_caption(caption)  # pyright: ignore [reportUnknownMemberType]
        else:
            table.add_caption(  # pyright: ignore [reportUnknownMemberType]
                NoEscape(caption)
            )

    if label is not None:
        table.append(  # pyright: ignore [reportUnknownMemberType]
            Label2(label, "table")
        )

    gdm().append(table)
