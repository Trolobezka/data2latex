from typing import List, Literal, Optional

from pylatex import Section  # pyright: ignore [reportMissingTypeStubs]
from pylatex.utils import NoEscape  # pyright: ignore [reportMissingTypeStubs]
from pylatex.base_classes import LatexObject  # pyright: ignore [reportMissingTypeStubs]

from .dm import DocumentManager, gdm
from .environments import Text


def section(title: str, numbering: bool = False, label: Optional[str] = None) -> None:
    """
    Insert a section into the document.

    :param title: Section text.
    :type title: str
    :param numbering: ``True`` for numbering this section, defaults to ``False``.
    :type numbering: bool, optional
    :param label: Label for later referencing, use format ``"prefix:label"`` or just ``"label"`` with automatic prefix ``"sec"``, defaults to ``None``.
    :type label: Optional[str], optional
    """
    gdm().append(  # pyright: ignore [reportUnknownMemberType]
        Section(
            title,
            numbering=numbering,
            label=label,  # pyright: ignore [reportGeneralTypeIssues]
        )
    )


def text(content: str, escape: bool = True) -> None:
    """
    Add a paragraph of solid text.

    :param content: Content fo the paragraph.
    :type content: str
    :param escape: ``True`` for replacing special LaTeX characters, defaults to ``True``.
    :type escape: bool, optional
    """
    if escape:
        content = content.replace("_", r"\_")
    gdm().append(Text(content=content, escape=escape))


# This should offer some of the options as DocumentManager.__init__().
# Instead of copying all of the possible inputs, we could just put *args
# and **kwargs and transfer them into the __init__() through gdm().
# I like this more because it is more expressive and works well with type hinting.
def setup(
    document_class: str = "article",
    document_class_options: List[str] = [],
    font_size: Literal["10pt", "11pt", "12pt"] = "12pt",
    spacing: Optional[Literal["1x", "1.5x", "2x"]] = "1.5x",
    par_indent: Optional[str] = "2em",
    par_skip: Optional[str] = "0.5em",
    horizontal_margin: Optional[str] = "2cm",
    vertical_margin: Optional[str] = "2cm",
    page_numbers: bool = False,
    additional_packages: List[LatexObject | str] = [],
) -> None:
    """
    Optional setup for the LaTeX document. This must be called first and cannot be combined with ``use_standalone...`` functions.

    :param document_class: Document class, defaults to ``"article"``.
    :type document_class: str, optional

    :param document_class_options: Options for the document class, defaults to ``[]``.
    :type document_class_options: List[str], optional

    :param font_size: Main font size with unit, defaults to ``"12pt"``.
    :type font_size: Literal["10pt", "11pt", "12pt"], optional

    :param spacing: Size of spacing between lines. Uses ``setspace`` package. Defaults to ``"1.5x"``.
    :type spacing: Optional[Literal["1x", "1.5x", "2x"]], optional

    :param par_indent: Length of paragraph indentation with unit. Uses ``indentfirst`` package. Defaults to ``"2em"``.
    :type par_indent: Optional[str], optional

    :param par_skip: Size of gap between paragraphs with unit. Uses ``parskip`` package. Defaults to ``"0.5em"``
    :type par_skip: Optional[str], optional

    :param horizontal_margin: Horizontal page margin with unit. Uses ``geometry`` package and is incompatible with ``standalone`` document class. Defaults to ``"2cm"``.
    :type horizontal_margin: Optional[str], optional

    :param vertical_margin: Vertical page margin with unit. Uses ``geometry`` package and is incompatible with ``standalone`` document class. Defaults to ``"2cm"``.
    :type vertical_margin: Optional[str], optional

    :param page_numbers: ``True`` for numbering pages, defaults to ``False``.
    :type page_numbers: bool, optional

    :param additional_packages: Additional packages or commands which will be placed into the document preamble, defaults to ``[]``.
    :type additional_packages: List[LatexObject | str], optional

    :raises RuntimeError: Cannot call this setup function if document manager has been already used.
    """
    if DocumentManager._instance is not None:  # pyright: ignore [reportPrivateUsage]
        raise RuntimeError(
            "Cannot call this setup function if document manager has been already used."
        )
    DocumentManager.gdm(
        document_class=document_class,
        document_class_options=document_class_options,
        font_size=font_size,
        spacing=spacing,
        par_indent=par_indent,
        par_skip=par_skip,
        horizontal_margin=horizontal_margin,
        vertical_margin=vertical_margin,
        page_numbers=page_numbers,
        additional_packages=additional_packages,
    )


def use_one_page_standalone(
    horizontal_border: str = "5pt", vertical_border: str = "5pt"
) -> None:
    """
    Optional setup for ``standalone`` document class with compilation into one cropped page. This is **experimental** feature and it can be incompatible with some other settings, e.g. ``geometry`` package and ``trim axis`` options for TikZ axis.

    :param horizontal_border: Horizontal page border with unit, defaults to ``"5pt"``.
    :type horizontal_border: str, optional
    :param vertical_border: Vertical page border with unit, defaults to ``"5pt"``.
    :type vertical_border: str, optional
    """
    DocumentManager.use_standalone(
        horizontal_border=horizontal_border,
        vertical_border=vertical_border,
        standalone_environment=None,
        crop=True,
        ignorerest=False,
        varwidth=True,
    )


def use_multi_page_standalone(
    horizontal_border: str = "5pt", vertical_border: str = "5pt"
) -> None:
    """
    Optional setup for ``standalone`` document class with compilation into many cropped pages. Each table and plot is placed on its own page. This can be used for generating all the figures into one long pdf and then using ``\\includegraphics[page=...]{...}`` in LaTeX to include the figures into your main document with sections, text, etc. This is **experimental** feature and it can be incompatible with some other settings, e.g. ``geometry`` package and ``trim axis`` options for TikZ axis.

    :param horizontal_border: Horizontal page border with unit, defaults to ``"5pt"``.
    :type horizontal_border: str, optional
    :param vertical_border: Vertical page border with unit, defaults to ``"5pt"``.
    :type vertical_border: str, optional
    """
    standalone_envs: List[str] = ["table", "figure"]
    DocumentManager.use_standalone(
        horizontal_border=horizontal_border,
        vertical_border=vertical_border,
        standalone_environment=standalone_envs,
        crop=True,
        ignorerest=True,
        varwidth=True,
        # This will renew the problematic float environments
        # and also locally (inside group) renew problem commands
        # such as centering, caption and label.
        additional_packages=[
            NoEscape(
                f"% This will disable float environment '{env}' for use in standalone multi mode\n"
                r"\renewenvironment{" + env + r"}[1][0]{%" + "\n"
                r"\renewcommand{\centering}{}%" + "\n"
                r"\renewcommand{\caption}[1]{}%" + "\n"
                r"\renewcommand{\label}[1]{}%" + "\n"
                r"%\begin{standalonepage}}{%" + "\n"
                r"%\end{standalonepage}}%" + "\n"
                r"}{}%" + "\n"
            )
            for env in standalone_envs
        ],
    )


def finish(
    filepath: str = "document",
    generate_tex: bool = True,
    compile_tex: bool = True,
    compiler: Optional[Literal["pdflatex", "latexmk"]] = "pdflatex",
) -> None:
    """
    Generate LaTeX source code and compile the document.

    :param filepath: File name or file path without extension, defaults to ``"document"``.
    :type filepath: str, optional
    :param generate_tex: ``True`` for generating .tex file, defaults to ``True``.
    :type generate_tex: bool, optional
    :param compile_tex: ``True`` for compiling the document into .pdf file, defaults to ``True``.
    :type compile_tex: bool, optional
    :param compiler: Compiler name, ``pdflatex`` could be faster then ``latexmk``, defaults to ``"pdflatex"``.
    :type compiler: Optional[Literal["pdflatex", "latexmk"]], optional
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

    :param filepath: File name or file path without extension, defaults to ``"document"``.
    :type filepath: str, optional
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
    Compile the document without saving the .tex file.

    :param filepath: File name or file path without extension, defaults to ``"document"``.
    :type filepath: str, optional
    :param compiler: Compiler name, ``pdflatex`` could be faster then ``latexmk``, defaults to ``"pdflatex"``.
    :type compiler: Optional[Literal["pdflatex", "latexmk"]], optional
    """
    gdm().finish(
        filepath=filepath, generate_tex=False, compile_tex=True, compiler=compiler
    )


def reset() -> None:
    """
    Reset the current document. This will remove all the content which has been appended. You can use the setup functions after calling this, e.g. compile two documents with different document class in one script.
    """
    DocumentManager._instance = None  # pyright: ignore [reportPrivateUsage]
