from os.path import isfile

class QueryPersistorNotInitializedError(Exception):
    """
    Exception raised when a function that is decorated with the
    persist decorator is called on an object that doesn't have a
    query_persistor.
    """


class QueryPersistor(object):
    """
    A callable classa which allows you to persist some data store object
    by attaching an instance of QueryPersistor to an attribute called
    query_persistor and then decoratoring data manipulating function
    calls with the @persist decorator defined below.

    QueryPersistor is only effective when initialized in the persisted objects
    __init__ function and when that object has @persist decorated functions.
    """
    def __init__(self, data_file_path, persisted_obj):
        """
        Initialize a QueryPersistor object.
        """
        # Start by loading an already existing data into
        # the object being persisted.
        self._load_data(data_file_path, persisted_obj)
        # Open up the data file in append mode so we don't
        # overwrite out previously stored data.
        self.query_log_file = open(data_file_path, 'a')

    def __call__(self, *args, **kwargs):
        """
        Callable which persists whatever is passed in as args in a format
        that can be later deserialized.
        """
        # In case we are handed objects we cast everything to a string.
        # This only works for objects that can be cleanly serialized with
        # bytestring casting. Since our current usage is only strings
        # this is fine.
        query_parts = [str(part) for part in args]
        # We are using CSV for serialization format.
        query_log = ','.join(query_parts)
        # Write newline delimited lines to the data log file.
        self.query_log_file.write('%s\n' % query_log)

    def _load_data(self, file_path, persisted_obj):
        """
        Load previously persisted data into a persisted object by calling
        the series of function calls that were persisted on the object in order.
        """
        # Check that there is a file or this operation is meaningless.
        if isfile(file_path):
            data_file = open(file_path, 'r')
            
            for query in data_file:
                # We strip newlines and split on commas.
                # This implementation is fragile because it will break if the data
                # persisted contains newlines.
                query_parts = query.strip('\n').split(',')
                
                # The function name is always the first data point.
                func_name = query_parts[0]
                # Everything else is function args.
                args = query_parts[1:]

                # Call the function on the persisted object passing in the args.
                getattr(persisted_obj, func_name)(*args)

            # Cleanup by closing the file.
            data_file.close()




def persist(func):
    """
    The persist decorator allows you to persist some data store object by attaching
    a QueryPersistor to the persisted object and then decorating any data alterning
    methods with this decorator.

    It works by storing the data alter function's name and the args that were passed
    to that function so that the actions can be replayed at a later time.
    """
    def wrapper(obj, *args, **kwargs):
        """
        inner function wrapper
        """

        # It's an error if you try to persist a function which doesn't have a
        # query_persistor defined.
        if not hasattr(obj, 'query_persistor'):

            message = "The object you are trying to persist queries on \
                       does not have a query_persistor attribute available."
            raise QueryPersistorNotInitializedError(message)

        # Persist the function call.
        # Note: This call is going to block for every data altering function call
        # on the persisted object. If write speed becomes important the QueryPersistor
        # should be updated to buffer data and write to disk using non-blocking means.
        obj.query_persistor(func.__name__, *args)

        # Call the original function.
        return func(obj, *args, **kwargs)

    return wrapper
