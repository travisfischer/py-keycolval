from keycolval.data_structures.binarytree import BinaryTree
from keycolval.stores.abstract import KeyColValStore


class BinaryTreeKeyColValStore(KeyColValStore):
    """
    A KeyColValStore implementation which uses a BinaryTree as the
    data structure for columns.

    BinaryTree's are generally good for sequential access to ordered collections
    as they are pre-sorted. You pay a price during storage of data but gain
    good performance during sequential access.
    """

    def __init__(self, *args, **kwargs):
        self.keys = {}

    def set(self, key, col, val):
        """ sets the value at the given key/column """
        if not key in self.keys:
            self.keys[key] = BinaryTree()

        self.keys[key].insert(col, val)


    def get(self, key, col):
        """ return the value at the specified key/column """
        if not key in self.keys:
            return None

        return self.keys[key].get(col)


    def get_key(self, key):
        """ returns a sorted list of column/value tuples """
        if not key in self.keys:
            return []

        return self.keys[key].all()

    def get_keys(self):
        """ returns a set containing all of the keys in the store """
        return set(self.keys.keys())

    def delete(self, key, col):
        """ removes a column/value from the given key """
        self.keys[key].delete(col)

    def delete_key(self, key):
        """ removes all data associated with the given key """
        del self.keys[key]

    def get_slice(self, key, start, stop):
        """
        returns a sorted list of column/value tuples where the column
        values are between the start and stop values, inclusive of the
        start and stop values. Start and/or stop can be None values,
        leaving the slice open ended in that direction
        """
        node_range = self.keys[key].find_range(start, stop)
        column_slice = [(node.key, node.value) for  node in node_range]
        return column_slice

