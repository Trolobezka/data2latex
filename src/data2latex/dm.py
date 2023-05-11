from typing import Any, List, Literal, Optional, Set, Union, cast

from pylatex import (  # pyright: ignore [reportMissingTypeStubs]
    Command,
    Document,
    Package,
    UnsafeCommand,
)
from pylatex.base_classes import LatexObject  # pyright: ignore [reportMissingTypeStubs]
from pylatex.utils import NoEscape  # pyright: ignore [reportMissingTypeStubs]


# TODO: Add options for geometry package
class DocumentManager:
    """
    Document Manager is a singleton class for storing information about current LaTeX document.

    :raises NotImplementedError: DocumentManager is singleton class and cannot be instantiated.
        Use DocumentManager.gdm() to get the instance.
    """

    _instance: Optional["DocumentManager"] = None

    @classmethod
    def gdm(cls, *args: Any, **kwargs: Any) -> "DocumentManager":
        """
        Get current document manager instance.

        :return: Current document manager instance
        :rtype: DocumentManager
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init__(*args, **kwargs)
        return cls._instance

    @classmethod
    def gd(cls) -> Document:
        """
        Get current PyLaTeX document.

        :return: Current PyLaTeX document
        :rtype: Document
        """
        return cls.gdm().document

    def __new__(cls) -> None:
        raise NotImplementedError(
            (
                "DocumentManager is singleton class and cannot be instantiated. "
                "Use DocumentManager.gdm() to get the instance."
            )
        )

    def __init__(  # pyright: ignore [reportInconsistentConstructor]
        self,
        document_class: str = "article",
        document_class_options: List[str] = [],
        # Default allowed sizes for article, report and book
        font_size: Literal["10pt", "11pt", "12pt"] = "12pt",
        spacing: Optional[Literal["1x", "1.5x", "2x"]] = "1.5x",  # setspace package
        par_indent: Optional[str] = "2em",  # parskip package
        par_skip: Optional[str] = "0.5em",  # indentfirst package
        page_numbers: bool = False,
        additional_packages: List[LatexObject | str] = [],
    ) -> None:
        self.document_class = document_class
        self.document_class_options = document_class_options
        self.font_size = font_size
        self.spacing = spacing
        self.par_indent = par_indent
        self.par_skip = par_skip
        self.page_numbers = page_numbers
        self.packages = additional_packages

        self.using_standalone: bool = False
        self.using_standalone_multi: bool = False

        self.document = Document(
            documentclass=self.document_class,
            document_options=[font_size, *document_class_options],
            page_numbers=page_numbers,
        )
        document_packages: Set[LatexObject | str] = cast(
            Set[Any],
            self.document.packages,  # pyright: ignore [reportUnknownMemberType]
        )
        if self.spacing is not None:
            document_packages.add(Package("setspace"))
            document_packages.add(
                Command(
                    {
                        "1x": "singlespacing",
                        "1.5x": "onehalfspacing",
                        "2x": "doublespacing",
                    }.get(self.spacing, self.spacing)
                )
            )
        # Parskip package must be loaded before parindent
        # package because it sets parindent equal to zero.
        if self.par_skip is not None:
            document_packages.add(Package("parskip"))
            document_packages.add(
                UnsafeCommand(
                    "setlength", r"\parskip", None, extra_arguments=self.par_skip
                )
            )
        if self.par_indent is not None:
            document_packages.add(Package("indentfirst"))
            document_packages.add(
                UnsafeCommand(
                    "setlength", r"\parindent", None, extra_arguments=self.par_indent
                )
            )

        for p in self.packages:
            document_packages.add(p)

    @classmethod
    def use_standalone(
        cls,
        horizontal_border: str = "5pt",
        vertical_border: str = "5pt",
        standalone_environment: Union[None, str, List[str]] = "standalonepage",
        crop: bool = True,
        ignorerest: bool = True,
        varwidth: bool = True,
        additional_packages: List[LatexObject | str] = [],
    ) -> None:
        if cls._instance is not None:
            raise RuntimeError(
                "Cannot call this setup function if document manager was already used."
            )

        # Building document class options as simple list of string
        # because I don't want to import dict2str from other file as
        # it could cause circular imports. Better file structure is needed.
        doc_cls_opts: List[str] = []
        doc_cls_opts.append(
            NoEscape(f"border={{{horizontal_border} {vertical_border}}}")
        )
        if standalone_environment is not None:
            if isinstance(standalone_environment, list):
                standalone_environment = ",".join(standalone_environment)
            doc_cls_opts.append(NoEscape(f"multi={{{standalone_environment}}}"))
        doc_cls_opts.append(f"crop=" + str(crop).lower())
        doc_cls_opts.append(f"ignorerest=" + str(ignorerest).lower())
        doc_cls_opts.append(f"varwidth=" + str(varwidth).lower())

        docman = cls.gdm(
            document_class="standalone",
            document_class_options=doc_cls_opts,
            additional_packages=additional_packages,
        )
        docman.using_standalone = True
        docman.using_standalone_multi = standalone_environment != None

    def append(self, content: Union[str, LatexObject]) -> None:
        """
        Append LaTeX content into the document.
        """
        self.document.append(content)  # pyright: ignore [reportUnknownMemberType]

    def finish(
        self,
        filepath: str = "document",
        generate_tex: bool = True,
        compile_tex: bool = True,
        compiler: Optional[Literal["pdflatex"]] = "pdflatex",
    ) -> None:
        """
        Compile the document.

        :param filepath: File path without extension, defaults to "document"
        :type filepath: str, optional
        :param keep_tex: True for removing generated .tex file, defaults to False
        :type keep_tex: bool, optional
        """
        if generate_tex and not compile_tex:
            self.document.generate_tex(  # pyright: ignore [reportUnknownMemberType]
                filepath
            )
        if compile_tex:
            self.document.generate_pdf(  # pyright: ignore [reportUnknownMemberType]
                filepath, clean_tex=not generate_tex, compiler=compiler
            )


def gdm() -> DocumentManager:
    """
    Get current document manager instance.

    :return: Current document manager instance
    :rtype: DocumentManager
    """
    return DocumentManager.gdm()


def gd() -> Document:
    """
    Get current PyLaTeX document.

    :return: Current PyLaTeX document
    :rtype: Document
    """
    return DocumentManager.gd()
