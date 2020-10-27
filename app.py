from pymongo import MongoClient
from flask import Flask, request, Response
import os
from flask_cors import CORS
from bson.json_util import loads, dumps, ObjectId
import pandas as pd
from io import BytesIO

client = MongoClient(os.environ.get("MONGO_CONNECTION_STRING"))
# client = MongoClient() # For offline testing.
db = client.test
visualizations = db.visualizations

DEBUG = True
app = Flask(__name__)
CORS(app)

@app.route('/status', methods=['GET'])
def status():
  return 'alive'

@app.route('/config', methods=['GET', 'POST'])
def respond_config():
  if request.form['url'] != 'undefined':
    db_entry_id = ObjectId(loads(request.form['url']))
    db_entry = db.visualizations.find_one({"_id": db_entry_id})
    try:
      data = pd.read_parquet(BytesIO(db_entry['filtered_dataframe']))
      data.set_index(list(data)[0], inplace=True).to_json(orient='index')
    except:
      if type(db_entry['transformed_dataframe']) == bytes: # The mockup db_entry stores the empty transformed_dataframe as a list, so don't convert that one.
        data = pd.read_parquet(BytesIO(db_entry['transformed_dataframe']))
        data.set_index(list(data)[0], inplace=True).to_json(orient='index')
      else:
        data = db_entry['transformed_dataframe']
  return Response(data, mimetype="application/json")

client.close()