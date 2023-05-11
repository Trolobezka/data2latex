from typing import List, Literal, Optional

from pylatex import Section  # pyright: ignore [reportMissingTypeStubs]
from pylatex.utils import NoEscape  # pyright: ignore [reportMissingTypeStubs]

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


def use_one_page_standalone(
    horizontal_border: str = "5pt", vertical_border: str = "5pt"
) -> None:
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
