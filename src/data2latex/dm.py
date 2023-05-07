from typing import Literal, Optional

# import matplotlib as mpl
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
import pylatex as tex  # pyright: ignore [reportMissingTypeStubs]


class DocumentManager:
    """
    Document Manager is a singleton class for storing information about current LaTeX document.

    :raises NotImplementedError: DocumentManager is singleton class and cannot be instantiated.
        Use DocumentManager.gdm() to get the instance.
    """

    _instance: Optional["DocumentManager"] = None

    @classmethod
    def gdm(cls) -> "DocumentManager":
        """
        Get current document manager instance.

        :return: Current document manager instance
        :rtype: DocumentManager
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.__init__()
        return cls._instance

    @classmethod
    def gd(cls) -> tex.Document:
        """
        Get current PyLaTeX document.

        :return: Current PyLaTeX document
        :rtype: tex.Document
        """
        return cls.gdm().document

    def __new__(cls) -> None:
        raise NotImplementedError(
            (
                "DocumentManager is singleton class and cannot be instantiated. "
                "Use DocumentManager.gdm() to get the instance."
            )
        )

    def __init__(self) -> None:
        self.document = tex.Document(
            documentclass="article",  # standalone
            document_options=["12pt"],  # "border=12pt", "varwidth"
            indent=False,
        )

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


def gd() -> tex.Document:
    """
    Get current PyLaTeX document.

    :return: Current PyLaTeX document
    :rtype: tex.Document
    """
    return DocumentManager.gd()
