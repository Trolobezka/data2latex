from numbers import Integral, Number
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Protocol,
    Sequence,
    Tuple,
    TypeAlias,
    Union,
    runtime_checkable,
)


def replace_multiple(
    source: str, to_be_replaced: List[str], replace_with: str = ""
) -> str:
    result: str = source
    for substring in to_be_replaced:
        result = result.replace(substring, replace_with)
    return result


def dict2str(
    data: Any | Dict[Any, Any],
    enclose: bool = False,
    level: int = 1,
) -> str:
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
                new_value: str = dict2str(value, enclose=True, level=level + 1)
                if replace_multiple(new_value, ["\t", "\n", " ", "%"]) == "{}":
                    continue
                parts.append(f"{key}={new_value}")
        tabs = "\t" * level
        result = f"%\n{tabs}" + (",%\n" + tabs).join(parts) + "%\n"
        if enclose:
            result += "\t" * max(level - 1, 0)
    else:
        result = str(data)
    return f"{{{result}}}" if enclose else f"{result}"


@runtime_checkable
class KnownLengthIterable(Protocol):
    def __iter__(self) -> Iterator[Any]:
        ...

    def __len__(self) -> int:
        ...


@runtime_checkable
class OuterKnownLengthIterable(
    Protocol,
):
    def __iter__(self) -> Iterator[KnownLengthIterable]:
        ...

    def __len__(self) -> int:
        ...


@runtime_checkable
class NDArrayLike(Protocol):
    ndim: Any
    shape: Any

    def tolist(self) -> Any:
        ...

    def __array__(self) -> Any:
        ...


@runtime_checkable
class DataFrameLike(Protocol):
    columns: Any
    index: Any
    shape: Any

    def __array__(self) -> Any:
        ...

    def __getitem__(self, idx: Any) -> Any:
        ...


def is_2D_iterable(obj: object) -> bool:
    return isinstance(obj, OuterKnownLengthIterable) and all(
        [isinstance(x, KnownLengthIterable) for x in obj]
    )


def is_ndarray(obj: object) -> bool:
    return "ndarray" in str(type(obj)) and isinstance(obj, NDArrayLike)


def is_DataFrame(obj: object) -> bool:
    return "DataFrame" in str(type(obj)) and isinstance(obj, DataFrameLike)


class KnownLengthIteratorChain:
    def __init__(self, length: int, *args: Iterator[Any]) -> None:
        if len(args) == 0:
            raise ValueError("Cannot create a chain without any iterators.")
        self.length = length
        self.iterators: Tuple[Iterator[Any]] = args
        self.iter_index: int = 0
        self.buffer_index: int = -1
        self.use_buffer: bool = False
        self.buffer: List[Any] = [None] * length

    def __reset__(self) -> None:
        self.use_buffer = True
        self.buffer_index = -1

    def __iter__(self) -> Iterator[Any]:
        return self

    def __next_inner__(self) -> Any:
        try:
            return next(self.iterators[self.iter_index])
        except StopIteration:
            self.iter_index += 1
            if self.iter_index >= len(self.iterators):
                self.__reset__()
                raise StopIteration
            return self.__next_inner__()

    def __next__(self) -> Any:
        item: Any = None
        if self.use_buffer:
            self.buffer_index += 1
            if self.buffer_index >= self.length:
                self.__reset__()
                raise StopIteration
            item = self.buffer[self.buffer_index]
        else:
            item = self.__next_inner__()
        self.buffer_index += 1
        if self.buffer_index >= self.length:
            raise ValueError("Length of the chain is insufficient.")
        self.buffer[self.buffer_index] = item
        return item

    def __len__(self) -> int:
        return self.length


class DataFrameInnerIterator:
    def __init__(self, dataframe: DataFrameLike, row_index: int):
        self.dataframe: DataFrameLike = dataframe
        self.row_count, self.column_count = dataframe.shape
        self.column_index: int = -1
        self.row_index: int = row_index

    def __reset__(self) -> None:
        self.column_index: int = -1

    def __iter__(self) -> Iterator[Any]:
        return self

    def __next__(self) -> Any:
        self.column_index += 1
        if self.column_index >= self.column_count:
            self.__reset__()
            raise StopIteration
        return self.dataframe[self.dataframe.columns[self.column_index]][
            self.row_index
        ]  # pyright: ignore [reportUnknownVariableType]

    def __len__(self) -> int:
        return self.column_count


class DataFrameOuterIterator:
    """
    Abstraction for iterating over :class:`pandas.DataFrame`. This class
    implements the interator interface which goes through the rows and outputs
    an iterator for each of them. Other possibility is to convert
    the :class:`pandas.DataFrame` and its columns/indices
    into :class:`numpy.ndarray` and concatinate them together. ::

        np.concatenate([np.expand_dims(data.columns.__array__(), 0), data.__array__()], axis=0)
    """

    def __init__(
        self,
        dataframe: DataFrameLike,
        include_column_names: bool = True,
        include_row_names: bool = True,
    ):
        self.dataframe: DataFrameLike = dataframe
        self.include_column_names: bool = include_column_names
        self._include_column_names: bool = include_column_names
        self.include_row_names: bool = include_row_names
        self.row_count, self.column_count = dataframe.shape
        self.row_index: int = -1

    def __reset__(self) -> None:
        self._include_column_names = self.include_column_names
        self.row_index = -1

    def __iter__(self) -> Iterator[Iterator[Any]]:
        return self

    def __next__(self) -> Iterator[Any]:
        if self._include_column_names:
            self._include_column_names = False
            if self.include_row_names:
                return KnownLengthIteratorChain(
                    self.column_count + 1, iter([""]), iter(self.dataframe.columns)
                )
            else:
                return KnownLengthIteratorChain(
                    self.column_count, iter(self.dataframe.columns)
                )
        self.row_index += 1
        if self.row_index >= self.row_count:
            self.__reset__()
            raise StopIteration
        if self.include_row_names:
            return KnownLengthIteratorChain(
                self.column_count + 1,
                iter([self.dataframe.index[self.row_index]]),
                DataFrameInnerIterator(self.dataframe, self.row_index),
            )
        else:
            return DataFrameInnerIterator(self.dataframe, self.row_index)

    def __len__(self) -> int:
        return self.row_count + (1 if self.include_column_names else 0)


DataFrameIterator = DataFrameOuterIterator
ValidDataType: TypeAlias = Union[str, int, Integral, float, Number]
KnownLengthIterable2D: TypeAlias = OuterKnownLengthIterable
Sequence2D: TypeAlias = Sequence[Sequence[Any]]
# NDArrayAny: TypeAlias = "np.ndarray[Any, np.dtype[Any]]"
