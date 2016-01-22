from abc import ABCMeta
from abc import abstractmethod


class KeyColValStore(object):
    """
    This is the abstract class which defines the interface for KeyColValStore
    objects.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def set(self, key, col, val):
        """ sets the value at the given key/column """
    
    @abstractmethod
    def get(self, key, col):
        """ return the value at the specified key/column """
    
    @abstractmethod
    def get_key(self, key):
        """ returns a sorted list of column/value tuples """
    
    @abstractmethod
    def get_keys(self):
        """ returns a set containing all of the keys in the store """
    
    @abstractmethod
    def delete(self, key, col):
        """ removes a column/value from the given key """
    
    @abstractmethod
    def delete_key(self, key):
        """ removes all data associated with the given key """
    
    @abstractmethod
    def get_slice(self, key, start, stop):
        """
        returns a sorted list of column/value tuples where the column
        values are between the start and stop values, inclusive of the
        start and stop values. Start and/or stop can be None values,
        leaving the slice open ended in that direction
        """
