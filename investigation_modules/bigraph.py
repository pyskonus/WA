import numpy
import ctypes


# this class was defined as a helping class for DynamicArray
class Array:
    def __init__(self, size):
        """
        Creates an array with size elements.

        :param size:
        """
        if size <= 0:
            raise ValueError("Array size must be > 0")
        self._size = size
        # Create the array structure using the ctypes module.
        PyArrayType = ctypes.py_object * size
        self._elements = PyArrayType()
        # Initialize each element.
        self.clear(None)

    def __len__(self):
        """
        # Returns the size of the array.

        :return:
        """
        return self._size

    def __getitem__(self, index):
        """
        # Gets the contents of the index element.

        :param index:
        :return:
        """
        if index < 0 or index >= len(self):
            raise IndexError("Array subscript out of range")
        return self._elements[index]

    def __setitem__(self, index, value):
        """
        # Puts the value in the array element at index position.

        :param index:
        :param value:
        :return:
        """
        if index < 0 or index >= len(self):
            raise IndexError("Array subscript out of range")
        self._elements[index] = value

    def clear(self, value):
        """
        # Clears the array by setting each element to the given value.

        :param value:
        :return:
        """
        for i in range(len(self)):
            self._elements[i] = value

    # Returns the array's iterator for traversing the elements.
    def __iter__(self):
        return _ArrayIterator(self._elements)

    def __str__(self):
        result = '|'
        for el in self._elements:
            result += str(el) + ', '
        result = result[:-2] + '|'

        return result


# An iterator for the Array ADT.
class _ArrayIterator:
    def __init__(self, the_array):
        self._array_ref = the_array
        self._cur_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._cur_index < len(self._array_ref):
            entry = self._array_ref[self._cur_index]
            self._cur_index += 1
            return entry
        else:
            raise StopIteration


# this class was defined as a helping class for Bigraph
class DynamicArray:
    """
    A dynamic array class akin to a simplified Python list
    """

    def __init__(self):
        """
        Create an empty array
        """
        self._n = 0  # count actual elements
        self._A = self._make_array(1)  # low-level array

    def __len__(self):
        """Return number of elements stored in the array."""
        return self._n

    def __getitem__(self, k):
        """Return element at index k."""
        if not 0 <= k < self._n:
            raise IndexError('invalid index')
        return self._A[k]  # retrieve from array

    def append(self, obj):
        """
        Add object to end of the array
        """
        if self._n == len(self._A):  # not enough room
            self._resize(2 * len(self._A))  # so double capacity
        self._A[self._n] = obj
        self._n += 1

    def _resize(self, c):  # nonpublic utility
        """
        Resize internal array to capacity c
        """
        B = self._make_array(c)  # new (bigger) array
        for k in range(self._n):  # for each existing value
            B[k] = self._A[k]
        self._A = B  # use the bigger array

    def _make_array(self, c):  # nonpublic utility
        """
        Return new array with capacity c
        """
        return Array(c)  # see ctypes documentation

    def __iter__(self):
        if self._n == 0:
            return iter([])
        temp_array = Array(self._n)
        for i in range(self._n):
            temp_array[i] = self._A[i]
        return iter(temp_array)

    def insert(self, k, value):
        """Insert value at index k, shifting subsequent values rightward."""
        # (for simplicity, we assume 0 <= k <= n in this version)
        if self._n == len(self._A):  # not enough room
            self._resize(2 * len(self._A))  # so double capacity
        for j in range(self._n, k, -1):  # shift rightmost first
            self._A[j] = self._A[j - 1]
        self._A[k] = value  # store newest element
        self._n += 1

    def remove(self, value):
        """
        Remove first occurrence of value(or raise ValueError)
        """
        # note: we do not consider shrinking the dynamic array in this version
        for k in range(self._n):
            if self._A[k] == value:  # found a match!
                for j in range(k, self._n - 1):  # shift others to fill gap
                    self._A[j] = self._A[j + 1]
                self._A[self._n - 1] = None  # help garbage collection
                self._n -= 1  # we have one less item

                return  # exit immediately
        raise ValueError("value not found")  # only reached if no match

    def __str__(self):
        result = '|'
        for el in self._A:
            if el is None:
                break
            result += str(el) + ', '
        result = result[:-2] + '|'

        return result


class Bigraph:
    """
    This class represents a bipartite graph and uses dictionary, numpy array and
    DynamicArray data types.

    Methods defined here:

    add(incentive, reactions):
    adds a new incentive with its reactions to the bigraph
    """
    # If you find a collocation "left/right vertexes" in any further docstrings
    # or comments, "left vertexes" means stimulus words and "right vertexes"
    # means words-reactions.
    def __init__(self):
        """
        self._incentives contains incentive (stimulus) words as keys and indices as values.
        For example, if self._incentives contains an item ('rabbit': 45) then
        self._numbers[45] contains a row that contains either 0 or any positive integer.
        If, for example, self._numbers[45][123] contains, for instance, integer 30,
        then 30 people answered with self._reactions_ordered[123] to the word 'rabbit'.
        If self._numbers[45][124] contains 0, then no one answered with
        self._reactions_ordered[124] to the word 'rabbit'.
        """
        self._incentives = dict()
        self._reactions = dict()
        self._incentives_ordered = DynamicArray()
        self._reactions_ordered = DynamicArray()
        self._numbers = numpy.array([[]], dtype=numpy.uint8)

    def __setitem__(self, incentive, reactions):
        # if the incentive is already in the graph, raise an exception with a corresponding message
        if incentive in self._incentives:
            raise ValueError("The given incentive is already present in the graph")
        # if the bigraph is empty
        if len(self._incentives) == 0:
            # add the incentive to left vertexes
            self._incentives[incentive] = 0
            self._incentives_ordered.append(incentive)
            # add the reactions to right vertexes
            i = 0
            for el in reactions:
                self._reactions[el[0]] = i
                self._reactions_ordered.append(el[0])
                i += 1
            # change the self._numbers matrix accordingly
            for el in self._reactions:
                for element in reactions:
                    if element[0] == el:
                        self._numbers = numpy.append(self._numbers, numpy.uint8(element[1]))
                        break
            # reshape the self._numbers matrix
            self._numbers = self._numbers.reshape((1, len(reactions)))
            assert self._numbers.size == self._numbers.shape[0] * self._numbers.shape[1]
            return None  # This return statement was added just to avoid putting all the rest
            # of the function inside an else branch
        else:
            # add the incentive to left vertexes
            self._incentives[incentive] = self._numbers.shape[0]
            self._incentives_ordered.append(incentive)
            # divide the given reactions into those that are present in the right vertexes and those that are not
            absent = set()
            present = set()
            for el in reactions:
                if el[0] in self._reactions:
                    present.add(el)
                else:
                    absent.add(el)
            # add the absent reactions to right vertexes
            i = self._numbers.shape[1]
            for el in absent:
                self._reactions[el[0]] = i
                self._reactions_ordered.append(el[0])
                i += 1
            # find out what the shape and size of the matrix will be after this step
            former_shape = self._numbers.shape
            next_shape = self._numbers.shape
            next_shape = list(next_shape)
            next_shape[0] += 1              # add one to shape[0] because one vertex is added to left vertexes
            next_shape[1] += i - self._numbers.shape[1]
            # add the right numbers to the self._numbers matrix
            self._numbers.reshape(self._numbers.size)
            for k in range(self._numbers.size, 0, -self._numbers.shape[1]):
                for _ in range(len(absent)):
                    self._numbers = numpy.insert(self._numbers, k, numpy.uint8(0))
            temp = numpy.array([0] * former_shape[1], dtype=numpy.uint8)
            for el in present:
                temp[self._reactions[el[0]]] = numpy.uint8(el[1])
            for el in absent:
                temp = numpy.append(temp, numpy.uint(el[1]))
            self._numbers = self._numbers.reshape(self._numbers.size)
            self._numbers = numpy.concatenate((self._numbers, temp))
            # reshape the self._numbers matrix
            self._numbers = self._numbers.reshape(next_shape)
            assert self._numbers.size == self._numbers.shape[0] * self._numbers.shape[1]

        return None

    def __getitem__(self, word):
        if word in self._incentives:
            res = []
            for i in range(self._numbers.shape[1]):
                if self._numbers[self._incentives[word], i]:
                    res.append((self._reactions_ordered[i], int(self._numbers[self._incentives[word], i])))
            return res
        else:
            raise ValueError("The element is not in the graph")

    def __str__(self):
        res = '  '
        for el in self._reactions_ordered:
            res += str(el)
        res += ' ' * len(res) + '\n'
        for el1 in self._incentives_ordered:
            res += str(el1) + ' '
            for el in self._numbers[self._incentives[el1]]:
                res += str(el)
            res += '\n'

        return res[:-1]

    def __iter__(self):
        return iter(self._incentives_ordered)

    def get_incentives(self, word):
        if word in self._reactions:
            res = set()
            for i in range(self._numbers.shape[0]):
                if self._numbers[i, self._reactions[word]]:
                    res.add((self._incentives_ordered[i], self._numbers[i, self._reactions[word]]))
            return res
        else:
            raise ValueError("The element is not in the graph")
