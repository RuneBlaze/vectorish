from __future__ import annotations

from vectorish.vectorish import Vectorish as EfficientVector
from typing import Iterator, TypeVar, Sequence, overload
from itertools import chain

T = TypeVar("T")


def vector(it: Iterator[T] | None = None) -> Vector[T]:
    """
    Create a Vector object from an iterator.

    Args:
        it (Optional[Iterator[T]]): An iterator to create the Vector from. Defaults to None.

    Returns:
        Vector[T]: A Vector object containing the elements from the iterator.
    """
    if it is None:
        return Vector()
    vector = Vector()
    for item in it:
        vector.append(item)
    return vector


class Vector(Sequence[T]):
    _inner: EfficientVector

    def __init__(self):
        """
        Initialize an empty Vector.
        """
        self._inner = EfficientVector()

    def __iter__(self) -> Iterator:
        """
        Return an iterator over the elements of the Vector.

        Returns:
            Iterator: An iterator over the elements.
        """
        return (self._inner[i] for i in range(len(self)))

    def __len__(self) -> int:
        """
        Return the number of elements in the Vector.

        Returns:
            int: The number of elements.
        """
        return len(self._inner)

    @overload
    def __getitem__(self, index: int) -> T:
        """
        Get the element at the specified index.

        Args:
            index (int): The index of the element.

        Returns:
            T: The element at the specified index.
        """
        pass

    @overload
    def __getitem__(self, index: slice) -> Vector[T]:
        """
        Get a slice of the Vector.

        Args:
            index (slice): The slice to retrieve.

        Returns:
            Vector[T]: A new Vector containing the elements in the slice.
        """
        pass

    def __getitem__(self, index):
        """
        Get the element or slice at the specified index.

        Args:
            index (int or slice): The index or slice of the element(s).

        Returns:
            T or Vector[T]: The element or a new Vector containing the elements in the slice.
        """
        if isinstance(index, slice):
            rng = range(len(self))[index]
            return vector(self._inner[i] for i in rng)
        if index < 0:
            index = len(self) + index
        return self._inner[index]

    def __setitem__(self, index: int, value: T):
        """
        Set the element at the specified index to a new value.

        Args:
            index (int): The index of the element to set.
            value (T): The new value for the element.
        """
        self._inner[index] = value

    def pop(self, index: int | None = None) -> T:
        """
        Remove and return an element from the vector at the specified index.

        If no index is provided, the last element is removed and returned.

        If a negative index is provided, it is treated as an offset from the end of the vector.

        Args:
            index (int | None, optional): The index of the element to remove. Defaults to None.

        Returns:
            T: The removed element.

        Raises:
            IndexError: If the index is out of range.
        """
        if index is None:
            return self._inner.pop()
        if index < 0:
            index = len(self) + index
        return self._inner.pop(index)

    def popleft(self) -> T:
        """
        Remove and return the first element from the Vector.

        Returns:
            T: The removed element.

        Raises:
            IndexError: If the Vector is empty.
        """
        return self.pop(0)

    def reverse(self):
        """
        Reverse the elements of the Vector in place.
        """
        self._inner.reverse()

    def index(self, value: T) -> int:
        """
        Return the index of the first occurrence of the specified value.

        Args:
            value (T): The value to find.

        Returns:
            int: The index of the first occurrence.

        Raises:
            ValueError: If the value is not found.
        """
        for i, item in enumerate(self):
            if item == value:
                return i
        raise ValueError(f"{value} is not in the vector")

    def copy(self) -> Vector[T]:
        """
        Return a copy of the Vector.

        Returns:
            Vector[T]: A copy of the Vector.
        """
        return vector(self)

    def count(self, value: T) -> int:
        """
        Count the number of occurrences of the specified value.

        Args:
            value (T): The value to count.

        Returns:
            int: The number of occurrences.
        """
        return sum(1 for item in self if item == value)

    def clear(self) -> None:
        """
        Remove all elements from the Vector.
        """
        self._inner.clear()

    def extend(self, it: Iterator[T]) -> None:
        """
        Extend the Vector by appending elements from the iterator.

        Args:
            it (Iterator[T]): The iterator with elements to append.
        """
        for item in it:
            self.append(item)

    def sort(self, key=None, reverse=False):
        """
        Sort the elements of the Vector in place.

        Args:
            key (callable, optional): A function of one argument that is used to extract a comparison key from each list element. Defaults to None.
            reverse (bool, optional): If True, the list elements are sorted as if each comparison were reversed. Defaults to False.
        """
        coll = list(self)
        self._inner.clear()
        coll.sort(key=key, reverse=reverse)
        self.extend(coll)

    def append(self, value: T) -> None:
        """
        Append an element to the end of the Vector.

        Args:
            value (T): The element to append.
        """
        self._inner.append(value)

    def __repr__(self) -> str:
        """
        Return a string representation of the Vector.

        Returns:
            str: A string representation of the Vector.
        """
        return repr(self._inner)

    def __str__(self) -> str:
        """
        Return a string representation of the Vector.

        Returns:
            str: A string representation of the Vector.
        """
        return str(self._inner)

    def insert(self, index: int, value: T) -> None:
        """
        Insert an element at the specified index.

        Args:
            index (int): The index to insert the element at.
            value (T): The element to insert.
        """
        if index < 0:
            index = len(self) + index
        self._inner.insert(index, value)

    def __add__(self, other: Vector[T]) -> Vector[T]:
        """
        Concatenate two Vectors.

        Args:
            other (Vector[T]): The Vector to concatenate with.

        Returns:
            Vector[T]: A new Vector containing the elements of both Vectors.
        """
        if not isinstance(other, Vector):
            raise TypeError(f"unsupported operand type(s) for +: 'Vector' and '{type(other).__name__}'")
        return vector(chain(self, other))
    
    def __iadd__(self, other: Vector[T]) -> Vector[T]:
        """
        Concatenate two Vectors in place.

        Args:
            other (Vector[T]): The Vector to concatenate with.

        Returns:
            Vector[T]: The Vector with the elements of both Vectors.
        """
        if not isinstance(other, Vector):
            raise TypeError(f"unsupported operand type(s) for +: 'Vector' and '{type(other).__name__}'")
        self.extend(other)
        return self
    
    def __mul__(self, n: int) -> Vector[T]:
        """
        Repeat the Vector n times.

        Args:
            n (int): The number of times to repeat the Vector.

        Returns:
            Vector[T]: A new Vector containing the elements of the Vector repeated n times.
        """
        return vector(chain.from_iterable(self for _ in range(n)))
