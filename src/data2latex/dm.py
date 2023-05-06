from typing import Optional

# import matplotlib as mpl
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
# import pylatex as tex  # pyright: ignore [reportMissingTypeStubs]


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
            print("gdm")
            cls._instance = super().__new__(cls)
            cls._instance.__init__()
        return cls._instance

    def __new__(cls) -> None:
        raise NotImplementedError(
            (
                "DocumentManager is singleton class and cannot be instantiated."
                "Use DocumentManager.gdm() to get the instance."
            )
        )

    def __init__(self) -> None:
        pass


def gdm() -> DocumentManager:
    """
    Get current document manager instance.

    :return: Current document manager instance
    :rtype: DocumentManager
    """
    return DocumentManager.gdm()
