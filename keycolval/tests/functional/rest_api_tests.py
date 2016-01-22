import unittest
import keycolval.api
from keycolval.api import app
import json
from datetime import datetime

class RestAPITests(unittest.TestCase):

	def setUp(self):
		app.testing = True
		app.config['DATA_STORE_FILE'] = '/tmp/rest-api-tests-data.%s' % datetime.now()
		self.client = app.test_client()

	def test_rest_api(self):
		self.client.post('/set/',
						 data={
						 	'key': 'a-key',
						 	'column': 'a-column',
						 	'value': 'my-value'
						 })
		self.client.post('/set/',
						 data={
						 	'key': 'a-key',
						 	'column': 'a2-column',
						 	'value': 'value2'
						 })
		self.client.post('/set/',
				 data={
				 	'key': 'b-key',
				 	'column': 'b-column',
				 	'value': 'valueb'
				 })

		response = self.client.get('/get/a-key/a-column/')
		data = json.loads(response.data)
		self.assertEqual(data, {'value': 'my-value'})

		response = self.client.get('/get/b-key/b-column/')
		data = json.loads(response.data)
		self.assertEqual(data, {'value': 'valueb'})

		response = self.client.get('/get/a-key/not-column/')
		data = json.loads(response.data)
		self.assertEqual(data, {'value': None})

		response = self.client.get('/get/not-key/not-column/')
		data = json.loads(response.data)
		self.assertEqual(data, {'value': None})
		
		response = self.client.get('/get-key/a-key/')
		data = json.loads(response.data)
		
		self.assertEqual(data, {
			'a-column': 'my-value',
			'a2-column': 'value2'
		})

		response = self.client.get('/get-key/not-key/')
		data = json.loads(response.data)
		
		self.assertEqual(data, {})


		response = self.client.get('/get-keys/')
		data = json.loads(response.data)
		self.assertEqual(data, {'keys': ['b-key', 'a-key']})


		self.client.post('/set/',
						 data={
						 	'key': 'a-key',
						 	'column': 'a2-column',
						 	'value': 'different-value'
						 })

		response = self.client.get('/get/a-key/a2-column/')
		data = json.loads(response.data)
		self.assertEqual(data, {'value': 'different-value'})

		self.client.post('/set/',
						 data={
						 	'key': 'a-key',
						 	'column': 'a5-column',
						 	'value': 'value5'
						 })
		self.client.post('/set/',
						 data={
						 	'key': 'a-key',
						 	'column': 'a3-column',
						 	'value': 'value3'
						 })
		self.client.post('/set/',
						 data={
						 	'key': 'a-key',
						 	'column': 'a4-column',
						 	'value': 'value4'
						 })


		response = self.client.get('/get-slice/a-key/a2-column/a4-column/')
		data = json.loads(response.data)
		self.assertEqual(data, {'a2-column': 'different-value',
								'a3-column': 'value3',
								'a4-column': 'value4'})
		
		response = self.client.get('/get-slice/a-key/none/a4-column/')
		data = json.loads(response.data)
		self.assertEqual(data, {'a-column': 'my-value',
								'a2-column': 'different-value',
								'a3-column': 'value3',	
								'a4-column': 'value4'})

		response = self.client.get('/get-slice/a-key/a2-column/none/')
		data = json.loads(response.data)
		self.assertEqual(data, {'a2-column': 'different-value',
								'a3-column': 'value3',
								'a4-column': 'value4',
								'a5-column': 'value5'})

		self.client.delete('/delete/a-key/a4-column/')
		
		response = self.client.get('/get/a-key/a4-column/')
		data = json.loads(response.data)
		self.assertEqual(data, {'value': None})


		self.client.delete('/delete-key/a-key/')
	
		response = self.client.get('/get/a-key/a1-column/')
		data = json.loads(response.data)
		self.assertEqual(data, {'value': None})


		response = self.client.get('/get-keys/')
		data = json.loads(response.data)
		self.assertEqual(data, {'keys': ['b-key']})

