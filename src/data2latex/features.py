from typing import Literal, Optional

from pylatex import Section  # pyright: ignore [reportMissingTypeStubs]

from .dm import DocumentManager, gdm
from .environments import Text


def section(title: str, numbering: bool = False, label: Optional[str] = None) -> None:
    """
    Insert a section into the document.
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
    Add paragraph of solid text.
    """
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
