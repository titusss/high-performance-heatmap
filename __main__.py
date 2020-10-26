from pymongo import MongoClient
from flask import Flask, request
import os
from flask_cors import CORS

# client = MongoClient(os.environ.get("MONGO_CONNECTION_STRING"))
client = MongoClient()
db = client.main
heatmaps = db.heatmaps

DEBUG = True
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})  # enable CORS

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

@app.route('/upload', methods=['GET', 'POST'])
def upload_json():
  json = json.loads(request.form['form'])
  console.log(json)
  return 'moin'


client.close()