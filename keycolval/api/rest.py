"""
Define the REST views for our application API.

Note: I have choosen URLs which include the function name
in order to make the resolution as simple as possible.
These URLs are not HATEOS RESTful as REST should just deal with
resources and use HTTP Methods to maniplulate them.
"""

from keycolval.api import app
from flask import jsonify
from flask import request

@app.route('/set/', methods=['POST'])
def set_keycolval():
	"""
	Set a key, column, value in the datastore.
	"""
	post_data = request.form

	app.data_store.set(post_data['key'],
					   post_data['column'],
					   post_data['value'])
	# Included posted data in HTTP response as confirmation.
	return jsonify(dict(post_data))

@app.route('/get/<key>/<col>/', methods=['GET'])
def get_keycol(key, col):
	"""
	Get a value at a key/column combintation.
	"""
	value = app.data_store.get(key, col)
	return jsonify({'value': value})

@app.route('/get-key/<key>/', methods=['GET'])
def get_key(key):
	"""
	Get all columns for a key.
	"""
	columns = app.data_store.get_key(key)
	return jsonify(columns)

@app.route('/get-keys/', methods=['GET'])
def get_keys():
	"""
	Get all the current keys.
	"""
	keys = app.data_store.get_keys()
	return jsonify({'keys': list(keys)})

@app.route('/delete/<key>/<col>/', methods=['DELETE'])
def delete_keycol(key, col):
	"""
	Delete a column/value pair within a key.
	"""
	app.data_store.delete(key, col)
	return jsonify({'key': key, 'column': col})

@app.route('/delete-key/<key>/', methods=['DELETE'])
def delete_key(key):
	"""
	Delete an entire key.
	"""
	app.data_store.delete_key(key)
	return jsonify({'key': key})

@app.route('/get-slice/<key>/<start>/<end>/', methods=['GET'])
def get_slice(key, start, end):
	"""
	Get a slice of columns in a key.
	'none' or 'null' may be used as start or end indices in
	order to specify an open slice.
	"""
	start_index = None if start.lower() in ['none', 'null'] else start
	end_index = None if end.lower() in ['none', 'null'] else end
	
	columns = app.data_store.get_slice(key, start_index, end_index)
	
	return jsonify(columns)	
