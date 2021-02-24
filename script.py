import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    print('made it to the server from JS')
    return "<h1>Hello World!</h1><p>From Python and Flask!</p>"


app.run()
