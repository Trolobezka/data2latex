from numbers import Number
from typing import (
    Callable,
    List,
    Literal,
    Optional,
    TypeAlias,
    Union,
    cast,
    Sequence,
)
from functools import reduce

import numpy as np
import pylatex as tex  # pyright: ignore [reportMissingTypeStubs]

from .dm import gdm, gd
from .environments import *

SimpleArray: TypeAlias = Sequence[Sequence[Union[str, int, float, Number]]]
NDArrayAny: TypeAlias = "np.ndarray[Any, np.dtype[Any]]"


def section(title: str, numbering: bool = False, label: Optional[str] = None) -> None:
    """
    Inserts a section into the document.

    :param title: Title text
    :type title: str
    :param numbering: True for numbering this section, defaults to False
    :type numbering: bool, optional
    :param label: Label for referencing, "label" or "prefix:label", defaults to None
    :type label: Optional[str], optional
    """
    doc = gdm().document
    doc.append(  # pyright: ignore [reportUnknownMemberType]
        tex.Section(
            title,
            numbering=numbering,
            label=label,  # pyright: ignore [reportGeneralTypeIssues]
        )
    )


def iterability_check(item: Any) -> bool:
    return (
        hasattr(item, "__iter__")
        and hasattr(item, "__getitem__")
        and hasattr(item, "__len__")
    )


def dict2str(data: Any | Dict[Any, Any], enclose: bool = False):
    result: str = ""
    if isinstance(data, dict):
        parts: List[str] = []
        for key, value in data.items():
            if not isinstance(key, str) or len(key) == 0 or value is None:
                continue
            elif value == "":
                if key[0] == "`":
                    parts.append(key[1:])
                else:
                    parts.append(key)
            else:
                new_value: str = dict2str(value, True)
                if new_value == "{}":
                    continue
                parts.append(f"{key}={new_value}")
        result = ",".join(parts)
    else:
        result = str(data)
    return f"{{{result}}}" if enclose else f"{result}"


def table(
    data: Union[SimpleArray, NDArrayAny],
    caption: Optional[str] = None,
    label: Optional[str] = None,
    center: bool = True,
    number_format: str = "{:0.3f}",
    str_format: str = "{{{{{{{:s}}}}}}}",
    str_convertor: Callable[[Any], str] = str,
    str_try_float: bool = True,
    line_style: Optional[Literal["border", "all", "header"]] = "all",
    header_dir: Optional[Literal["top", "left"]] = None,
    header_col_align: Optional[Literal["l", "c", "r", "j"]] = None,
    col_align: Literal["l", "c", "r", "j"] = "c",
    row_align: Literal["t", "m", "b", "h", "f"] = "m",
    position: str = "h!",
    escape_caption: bool = True,
    use_adjustbox: bool = True,
    use_siunitx: bool = True,
) -> None:
    if isinstance(data, np.ndarray):
        data = data.tolist()
    if not iterability_check(data) or not reduce(
        lambda acc, item: acc and iterability_check(item), data, True
    ):
        raise ValueError(
            "Data are not iterable in two dimensions. "
            "Both dimensions must implement __iter__, __getitem__ and __len__ functions."
        )
    data = cast(SimpleArray, data)
    max_column_count = max((len(row) for row in data))

    latex_rows: str = ""
    row_data: List[str] = [""] * max_column_count
    max_pre: List[int] = [0] * max_column_count
    max_post: List[int] = [0] * max_column_count
    for row in data:
        for i, item in enumerate(row):
            if isinstance(item, Number):
                row_data[i] = number_format.format(item)
            else:
                item2: str = ""
                if isinstance(item, str):
                    item2 = item
                else:
                    item2 = str_convertor(item)
                if str_try_float:
                    try:
                        item2 = number_format.format(float(item2))
                    except:
                        item2 = str_format.format(item2)
                else:
                    item2 = str_format.format(item2)
                row_data[i] = item2

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
        latex_rows += " & ".join(row_data) + r" \\" + "\n"

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
        print(colspec[i])

    if line_style == "border":
        colspec = ["|", "".join(colspec), "|"]
        rowspec = ["|", "".join(rowspec), "|"]
    elif line_style == "all":
        colspec = ["|", "|".join(colspec), "|"]
        rowspec = ["|", "|".join(rowspec), "|"]
    elif line_style == "header":
        if header_dir == None or header_dir == "top":
            rowspec = [
                "|",
                rowspec[0],
                "|",
                "".join(rowspec[1:] if len(rowspec) > 1 else []),
            ]
        elif header_dir == "left":
            colspec = [
                "|",
                colspec[0],
                "|",
                "".join(colspec[1:] if len(colspec) > 1 else []),
            ]

    additional_tblr_parameters = {}
    if header_dir == "top":
        if header_col_align is None:
            additional_tblr_parameters["row{1}"] = Parameters2({"font": r"\bfseries"})
        else:
            additional_tblr_parameters["row{1}"] = Parameters2(
                {"font": r"\bfseries", "halign": header_col_align}
            )
    elif header_dir == "left":
        if header_col_align is None:
            additional_tblr_parameters["column{1}"] = Parameters2(
                {"font": r"\bfseries"}
            )
        else:
            additional_tblr_parameters["column{1}"] = Parameters2(
                {"font": r"\bfseries", "halign": header_col_align}
            )

    table = tex.Table(position=position)
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
        if escape_caption:
            table.add_caption(caption)  # pyright: ignore [reportUnknownMemberType]
        else:
            table.add_caption(  # pyright: ignore [reportUnknownMemberType]
                NoEscape(caption)
            )

    tabular = tblr(
        "".join(colspec),
        "".join(rowspec),
        data=tex.utils.NoEscape(latex_rows),
        arguments=additional_tblr_parameters,
    )

    if use_adjustbox:
        adjustbox = AdjustBoxCommand(data=tabular)
        table.append(adjustbox)  # pyright: ignore [reportUnknownMemberType]
    else:
        table.append(tabular)  # pyright: ignore [reportUnknownMemberType]

    if label is not None:
        table.append(  # pyright: ignore [reportUnknownMemberType]
            Label2(label, "table")
        )

    gdm().document.append(table)  # pyright: ignore [reportUnknownMemberType]


def text(content: str, escape: bool = True) -> None:
    gd().append(  # pyright: ignore [reportUnknownMemberType]
        Text(content=content, escape=escape)
    )


def finish(
    filepath: str = "document",
    generate_tex: bool = True,
    compile_tex: bool = True,
    compiler: Optional[Literal["pdflatex"]] = "pdflatex",
) -> None:
    """
    Generate LaTeX source code and compile the document.
    """
    gdm().finish(
        filepath=filepath,
        generate_tex=generate_tex,
        compile_tex=compile_tex,
        compiler=compiler,
    )


def latex(filepath: str = "document") -> None:
    """
    Generate LaTeX source code.
    """
    gdm().finish(
        filepath=filepath,
        generate_tex=True,
        compile_tex=False,
    )


def pdf(
    filepath: str = "document", compiler: Optional[Literal["pdflatex"]] = "pdflatex"
) -> None:
    """
    Compile the document.
    """
    gdm().finish(
        filepath=filepath, generate_tex=False, compile_tex=True, compiler=compiler
    )
