"""
Quick and dirty script for generating a file that contains a configurable amount
of key/column/value data.

This can be used in combination with benchmark_performance.py to test the performance
of some KeyColumnValueStore implementation.

Usage:
  python generate_data.py /path/to/data/file
"""


import string
import uuid
from itertools import permutations
import sys
import random


def generate_unique_value():
	"""
	Generates a unique value.
	"""
	return str(uuid.uuid4())

# Generate 3 char permutations of first 18 ascii lowercase letters.
# N = 12, R = 3, Permutations = 1320
key_n = 12
key_r = 3

key_members = string.ascii_lowercase[:key_n]
key_perms = permutations(key_members, key_r)
keys = [''.join(parts) for parts in key_perms]

# We shuffle the keys so that they get written (and eventually inserted) out of order.
random.shuffle(keys)

# Generate 4 char permutations of first 8 digits
# N = 8, R = 4, Perumutations = 1680
col_members = '12345678'
col_r = 4
col_perms = permutations(col_members, col_r)
cols = [''.join(parts) for parts in col_perms]

# We shuffle the columns so that they get written (and eventually inserted) out of order.
random.shuffle(cols)

# 1320 Keys * 1680 Columns (per key) == 2,217,600 data entries
# Generates a ~100MB data file.
target_data_file_path = sys.argv[1]
data_file = open(target_data_file_path, 'w')

for key in keys:
	for column in cols:
		data_map = {'key': key, 'column': column, 'value': generate_unique_value()}
		data_string = '%(key)s,%(column)s,%(value)s\n' % data_map
		data_file.write(data_string)

data_file.close()
