from flask import Flask

# Using DoubleDictKeyColValStore as it performs much better for
# small / medium data load. 
from keycolval.stores.doubledictstore import DoubleDictKeyColValStore
from keycolval.stores.binarytreestore import BinaryTreeKeyColValStore

app = Flask(__name__)
app.config['DATA_STORE_FILE'] = '/tmp/keycolval-data'

@app.before_first_request
def initialize_data_store():
	"""
	Hook to initialize the data store on app start-up.
	"""
	app.data_store = DoubleDictKeyColValStore(
						path=app.config['DATA_STORE_FILE'])

# Import the views so they get registred.
import keycolval.api.rest
