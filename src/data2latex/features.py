from numbers import Integral, Number
from typing import Any, Callable, Dict, List, Literal, Optional, Union, cast

from pylatex import Table, Section  # pyright: ignore [reportMissingTypeStubs]
from pylatex.utils import (  # pyright: ignore [reportMissingTypeStubs]
    NoEscape,
    escape_latex,  # pyright: ignore [reportUnknownVariableType]
)

from .dm import DocumentManager, gdm
from .environments import (
    AdjustBoxCommand,
    CenteringFlagCommand,
    Label2,
    Parameters2,
    SetLengthCommand,
    Text,
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


def section(title: str, numbering: bool = False, label: Optional[str] = None) -> None:
    """
    Insert a section into the document.
    """
    doc = gdm().document
    doc.append(  # pyright: ignore [reportUnknownMemberType]
        Section(
            title,
            numbering=numbering,
            label=label,  # pyright: ignore [reportGeneralTypeIssues]
        )
    )


def table(
    data: Union[
        Sequence2D,
        KnownLengthIterable2D,
        DataFrameIterator,
        DataFrameLike,
        NDArrayLike,
    ],
    caption: Optional[str] = None,
    caption_pos: Literal["above", "bellow"] = "above",
    label: Optional[str] = None,
    center: bool = True,
    float_format: str = "{:0.3f}",
    str_format: str = "{{{{{{{:s}}}}}}}",
    str_convertor: Callable[[Any], str] = str,
    str_try_number: bool = True,
    line_style: Optional[Literal["border", "all", "header"]] = "all",
    header_dir: Optional[Literal["top", "left"]] = None,
    header_col_align: Optional[Literal["l", "c", "r", "j"]] = None,
    col_align: Literal["l", "c", "r", "j"] = "c",
    row_align: Literal["t", "m", "b", "h", "f"] = "m",
    position: str = "h!",
    escape_cells: bool = True,
    escape_caption: bool = True,
    use_adjustbox: bool = True,
    use_siunitx: bool = True,
    DF_column_names: bool = True,
    DF_row_names: bool = True,
) -> None:
    """
    Generate LaTeX table from input data. Table is created with tabularray package
    with optional siunitx usage for decimal number alignment. Table can be automatically
    scaled down with adjustbox package.
    """
    #
    # Handle different types of input data
    #
    if isinstance(data, DataFrameIterator):
        pass
    elif "DataFrame" in str(type(data)) and isinstance(data, DataFrameLike):
        data = DataFrameIterator(
            data, include_column_names=DF_column_names, include_row_names=DF_row_names
        )
    elif "ndarray" in str(type(data)) and isinstance(data, NDArrayLike):
        if data.ndim == 1:
            raise ValueError("Input data must have at least two dimensions.")
    elif isinstance(data, OuterKnownLengthIterable) and all(
        [isinstance(x, KnownLengthIterable) for x in data]
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

    #
    # Columns and rows configuration (header)
    #
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

    #
    # LaTeX environments completion
    #

    table = Table(position=position)
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
        "".join(colspec),
        "".join(rowspec),
        data=NoEscape(latex_data),
        arguments=additional_tblr_parameters,
    )

    if use_adjustbox:
        adjustbox = AdjustBoxCommand(data=tabular)
        table.append(adjustbox)  # pyright: ignore [reportUnknownMemberType]
    else:
        table.append(tabular)  # pyright: ignore [reportUnknownMemberType]

    if caption is not None and caption_pos == "bellow":
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


def text(content: str, escape: bool = True) -> None:
    gdm().append(Text(content=content, escape=escape))


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


def reset() -> None:
    """
    Reset the document. This will remove all the content which has been appended.
    """
    DocumentManager._instance = None  # pyright: ignore [reportPrivateUsage]
