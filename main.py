from flask import (
    Flask, 
    render_template, 
    request, 
    redirect, 
    jsonify, 
    abort
)
import pymongo
from uuid import uuid4
import os

DB_URL = os.environ.get('DB_URL')
assert DB_URL is not None, "DB_URL is required"

# mongo collection
col = pymongo.MongoClient(DB_URL, serverSelectionTimeoutMS=5000)['app']['links']
app = Flask(__name__, template_folder="templates")


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sub")
def sub():
    target = request.args.get("url")
    id = uuid4().hex[:5]
    col.insert_one({'id': id, 'url': target})
    return jsonify({
        'url': target,
        'id': id
    })

@app.route("/<id>")
def redirect_route(id = None):
    result = col.find_one({
        'id': id
    })
    if not result:
        return abort(404)
    url = result['url']
    return redirect(url)
    

app.run(host="0.0.0.0", port=8080)