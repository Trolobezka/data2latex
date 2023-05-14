from typing import Any, Dict, List, Optional, Union

from pylatex import (  # pyright: ignore [reportMissingTypeStubs]
    Label,
    Marker,
    Package,
)
from pylatex.base_classes import (  # pyright: ignore [reportMissingTypeStubs]
    Command,
    Container,
    Environment,
    LatexObject,
)
from pylatex.base_classes.command import (  # pyright: ignore [reportMissingTypeStubs]
    Parameters,
)
from pylatex.utils import (
    NoEscape,
    escape_latex,
)  # pyright: ignore [reportMissingTypeStubs]


class CommandEnvironment(Container):
    r"""
    Creates an environment with command syntax.

    :param command: Name of the command
    :type command: str
    :param arguments: Command arguments, defaults to None
    :type arguments: Optional[Union[str, List[str], Parameters]], optional
    :param options: Command options, defaults to None
    :type options: Optional[Union[str, List[str], Parameters]], optional

    .. highlight:: python
    .. code-block:: python

        CommandEnvironment("command", "arguments", "options", data="data")

    .. highlight:: latex
    .. code-block:: latex

        \command{arguments}[options]{data}
    """

    #: Set to ``True`` if this full container should be equivalent to an empty
    #: string if it has no content.
    omit_if_empty = False

    def __init__(
        self,
        command: str,
        arguments: Optional[Union[str, List[str], Parameters]] = None,
        options: Optional[Union[str, List[str], Parameters]] = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)  # pyright: ignore [reportUnknownMemberType]
        self.command = command
        self.arguments = arguments
        self.options = options

    def dumps(self) -> str:  # pyright: ignore [reportIncompatibleMethodOverride]
        """
        Represent the class as a string in LaTeX syntax.

        :meta private:
        """
        content = self.dumps_content()  # pyright: ignore [reportUnknownMemberType]
        if not content.strip() and self.omit_if_empty:
            return ""
        return Command(
            command=self.command,
            arguments=self.arguments,
            options=self.options,
            extra_arguments=content,
        ).dumps()


class Label2(Label):
    _latex_name = "label"

    def __init__(self, label: str, default_prefix: str = "prefix"):
        prefix = default_prefix
        if ":" in label:
            parts = label.split(":", 1)
            prefix = parts[0]
            label = parts[1]
        super().__init__(Marker(label, prefix))


class SetLengthCommand(Command):
    def __init__(
        self,
        name: str,
        value: str = "0pt",
        escape_value: bool = True,
        *args: Any,
        **kwargs: Any,
    ):
        if not escape_value:
            value = NoEscape(value)
        super().__init__(  # pyright: ignore [reportUnknownMemberType]
            command="setlength",
            arguments=NoEscape("\\" + name),
            extra_arguments=value,
            *args,
            **kwargs,
        )


class CenteringFlagCommand(Command):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(  # pyright: ignore [reportUnknownMemberType]
            command="centering", *args, **kwargs
        )


class Parameters2(Parameters):
    def __init__(
        self,
        *args: Any,
        escape: bool = False,
        enclose: bool = True,
        opening: str = "%\n\t",
        separator: str = ",%\n\t",
        closing: str = ",%\n",
        **kwargs: Any,
    ):
        self._positional_args: List[Union[str, LatexObject]]
        self._key_value_args: Dict[str, Union[str, LatexObject]]
        super().__init__(*args, **kwargs)  # pyright: ignore [reportUnknownMemberType]
        self.escape = escape
        self.enclose = enclose
        self.opening = opening
        self.separator = separator
        self.closing = closing

    def _list_args_kwargs(self) -> List[Any]:
        """
        Make a list of strings representing al parameters.

        :return: List of arguments
        :rtype: List[Any]
        """
        params: List[Any] = []
        params.extend(self._positional_args)
        _format: str = "{k}={{{v}}}" if self.enclose else "{k}={v}"
        params.extend(
            [
                "{k}={{{v}}}".format(k=k, v=v.dumps())
                if isinstance(v, Parameters2)
                else _format.format(k=k, v=v)
                for k, v in self._key_value_args.items()
            ]
        )
        return params

    def dumps(self) -> str:  # pyright: ignore [reportIncompatibleMethodOverride]
        return self._format_contents(  # pyright: ignore [reportUnknownMemberType]
            self.opening, self.separator, self.closing
        )


class AdjustBoxCommand(CommandEnvironment):
    packages = [Package("adjustbox")]
    omit_if_empty = False

    def __init__(
        self,
        max_width: Union[str, float] = 0.99,
        **kwargs: Any,
    ):
        if isinstance(max_width, float):
            max_width = f"{max_width:.2}\\linewidth"
        super().__init__(
            command="adjustbox",
            arguments=Parameters2({"max width": r"0.99\linewidth"}),
            options=None,
            **kwargs,
        )


class tblr(Environment):
    packages = [Package("tabularray"), Command("UseTblrLibrary", "siunitx")]
    omit_if_empty = False

    def __init__(
        self,
        colspec: str = "",
        rowspec: str = "",
        arguments: Dict[str, Union[str, LatexObject]] = {},
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)  # pyright: ignore [reportUnknownMemberType]
        self.arguments = Parameters2(colspec=colspec, rowspec=rowspec, **arguments)

    @property
    def colspec(self) -> str | LatexObject:
        return self.arguments._key_value_args[  # pyright: ignore [reportPrivateUsage]
            "colspec"
        ]

    @colspec.setter
    def colspec(self, value: str) -> None:
        self.arguments._key_value_args[  # pyright: ignore [reportPrivateUsage]
            "colspec"
        ] = value

    @property
    def rowspec(self) -> str | LatexObject:
        return self.arguments._key_value_args[  # pyright: ignore [reportPrivateUsage]
            "rowspec"
        ]

    @rowspec.setter
    def rowspec(self, value: str) -> None:
        self.arguments._key_value_args[  # pyright: ignore [reportPrivateUsage]
            "rowspec"
        ] = value


class Text(LatexObject):
    begin_paragraph = True
    end_paragraph = True
    separate_paragraph = True

    def __init__(self, content: Union[str, LatexObject], escape: bool = True):
        super().__init__()
        self.content = content
        self.escape = escape

    def dumps(self) -> str:  # pyright: ignore [reportIncompatibleMethodOverride]
        string: str = ""
        if isinstance(self.content, LatexObject):
            string = self.content.dumps()  # pyright: ignore [reportGeneralTypeIssues]
        else:
            if self.escape:
                string = escape_latex(self.content)
            else:
                string = self.content
        return string
