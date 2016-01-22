
"""
This file contains a class which runs a number of performance "bench marks." These
benchmarks are dependant on the existence of a test data file which can be generated
using the generate_data.py script in the same directory. The generate_data.py script
can be tweaked to generate various test data profiles.

This script currently doesn't do any meaningful statistical analysis it just gets
a rough time for setting and getting all of the data in the test data file.

You can also pass a --profile option which will use cProfile to show you the
performance profile of your data store's implementation.

Usage:
python -m keycolval.scripts.benchmark_performance /path/to/test/data [--profile]
"""

import csv
import sys
import unittest
from datetime import datetime
import random

import cProfile


from keycolval.stores.doubledict import DoubleDictKeyColValStore
from keycolval.stores.binarytreestore import BinaryTreeKeyColumnValueStore


# Define which data store implementation you want to test.
STORE_CLASS = DoubleDictKeyColValStore


class PerformanceTestClass(object):

    def __init__(self, store_class, test_data_file, *args, **kwargs):
        self._store = store_class()
        self._test_data_filepath = test_data_file

    def run_performance_tests(self):
        print "Running performance tests against %s class." % STORE_CLASS

        self._load_test_data()

        self._run_get_key_on_all_keys()

        self._run_get_on_all_columns()

        self._run_all_get_slices()

    def _load_test_data(self):
        print "Loading test data from file %s." % self._test_data_filepath

        csv_file = open(self._test_data_filepath, 'rb')
        test_data_reader = csv.reader(csv_file)

        start_time = datetime.now()

        for key, column, value in test_data_reader:
            self._store.set(key, column, value)

        end_time = datetime.now()
        
        load_time = end_time - start_time

        print "Took %s to load test data from file %s." % (load_time,
                                                           self._test_data_filepath)

    def _run_get_key_on_all_keys(self):
        keys = list(self._store.get_keys())
        # Randomize access pattern
        random.shuffle(keys)

        start_time = datetime.now()

        for key in keys:
            self._store.get_key(key)

        end_time = datetime.now()

        total_time = end_time - start_time

        print "Took %s to run get_key on all %s keys." % (total_time, len(keys))

    def _run_get_on_all_columns(self):
        column_lookup = self._get_key_column_lookup()

        start_time = datetime.now()

        for key in column_lookup.keys():
            for col in column_lookup[key]:
                self._store.get(key, col)
        
        end_time = datetime.now()

        total_time = end_time - start_time

        print "Took %s to run get on all %s keys and %s columns." % (
                                                total_time,
                                                len(column_lookup.keys()),
                                                len(column_lookup[column_lookup.keys()[0]]))

    def _get_key_column_lookup(self):
        lookup_table = {}
        keys = list(self._store.get_keys())

        # Randomize access pattern
        random.shuffle(keys)

        for key in keys:
            cols = self._store.get_key(key)
            
            # Randomize access pattern
            random.shuffle(cols)

            lookup_table[key] = [col_pair[0] for col_pair in cols]

        return lookup_table

    def _run_all_get_slices(self):
        slice_indices_lookup = self._get_slice_indices_lookup()

        start_time = datetime.now()

        for key, (start, end) in slice_indices_lookup.items():
            self._store.get_slice(key, start, end)

        end_time = datetime.now()

        total_time = end_time - start_time

        print "Took %s to run %s get slices." % (total_time,
                                                 len(slice_indices_lookup.keys()))

    def _get_slice_indices_lookup(self):
        keys = list(self._store.get_keys())
        random.shuffle(keys)

        indices_lookup = {}

        for key in keys:
            cols = self._store.get_key(key)
            start_column = cols[0][0]
            end_column = cols[-1][0]

            indices_lookup[key] = (start_column, end_column)

        return indices_lookup

if __name__ == "__main__":
    file_path = sys.argv[1]

    if len(sys.argv) > 2:
        run_profiler = True if sys.argv[2] == '--profile' else False
    else:
        run_profiler = False

    test_runner = PerformanceTestClass(STORE_CLASS, file_path)
    
    if run_profiler:
        cProfile.run('test_runner.run_performance_tests()')
    else:
        test_runner.run_performance_tests()
