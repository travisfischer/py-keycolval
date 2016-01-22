from keycolval.stores.abstract import KeyColValStore

from keycolval.persistence.query_persistor import QueryPersistor
from keycolval.persistence.query_persistor import persist


class DoubleDictKeyColValStore(KeyColValStore):
    """
    Implementation of a KeyColValStore which uses two-tier nested dict
    objects for storing key/column/value data points.

    dict is type of Hash Table which affords us really great average time
    direct access for operations like set, get, and delete.

    Note:

    Using nested Hash Tables is not optimal for sequential ordered access
    for operations like our get_slice and get_key.

    However, Python's sorted method which uses the Timsort algorithm allows
    us to sort small/medium sized collections fairly effeciency. In practice
    our nested dict implementation peforms very well with thousands of keys
    containing thousands of columns. It will probably slow down and become
    a memory hog at hundred's of thousands or millions of columns in a key.

    I decided to use this implementation in-spite of being told that
    get_slice would be the most common operation because without more
    information of the requirements for this data store in terms of size
    and structure of data, we can't actually know whether a structure with
    better algorithmic complexity will outperform in real time performance. 
    """
    def __init__(self, *args, **kwargs):
        self.keys = {}
        
        # We are using QueryPersistor to persist this data store so we 
        # first set a dummy persistor which will do nothing if called.
        self.query_persistor = lambda *args, **kwargs: None

        # Then if a data path was specified we initialize an actual
        # persistor object.
        if 'path' in kwargs:
            self.query_persistor = QueryPersistor(kwargs['path'], self)

    @persist
    def set(self, key, col, val):
        """ sets the value at the given key/column """

        if not key in self.keys:
            self.keys[key] = {}

        # Average O(1) performance.
        self.keys[key][col] = val

    def get(self, key, col):
        """ return the value at the specified key/column """

        if not key in self.keys or not col in self.keys[key]:
            return None
        
        # Average O(1) performance.
        return self.keys[key][col]

    def get_key(self, key):
        """ returns a sorted list of column/value tuples """
        if not key in self.keys:
            return []

        # This is going to be one of the slower operations as we first
        # iterate the entire column set and then we sort the entire
        # column set.
        columns = [(col, val) for col, val in self.keys[key].items()]

        # Sort using Timsort. Great for data that has already sorted
        # chunks.
        sorted_columns = sorted(columns, key=lambda tup: tup[0])
        return sorted_columns

    def get_keys(self):
        """ returns a set containing all of the keys in the store """
        return set(self.keys.keys())

    @persist
    def delete(self, key, col):
        """ removes a column/value from the given key """

        del self.keys[key][col]

    @persist
    def delete_key(self, key):
        """ removes all data associated with the given key """
        
        del self.keys[key]

    def get_slice(self, key, start, stop):
        """
        returns a sorted list of column/value tuples where the column
        values are between the start and stop values, inclusive of the
        start and stop values. Start and/or stop can be None values,
        leaving the slice open ended in that direction

        This is going to be the slowest operation because we are sorting and then searching
        unsorted data. I have already described above why I made this performance decision.

        We could easily improve the performance of this function by using an ordered collection
        for storing the columns but we would take a performance hit for all other operations.

        Some data structures to try would be sorted lists, ordered trees (binary tree)
        and balanced ordered trees (Splay Tree, etc...)
        """

        # This call iterates and then sorts all the columns in a key.
        columns = self.get_key(key)

        result_set = []
        
        cur_col = columns.pop(0) if columns else None
        done = False if cur_col else True

        while not done:
            # Run until we're done.

            if (start is None or cur_col[0] >= start) and (stop is None or cur_col[0] <= stop):
                # We have a column in our target range.
                result_set.append(cur_col)

            # Grab the next column if there is one.
            cur_col = columns.pop(0) if columns else None

            if not cur_col or (stop and cur_col[0] > stop):
                # We are done if we ran out of columns or if we ran past our stop_index.
                done = True

        return result_set
