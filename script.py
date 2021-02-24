import flask
import psycopg2
from flask import request, jsonify, make_response
from psycopg2.extras import RealDictCursor

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# makes connection to postgresDB
connection = psycopg2.connect(user="dave",
                                host="127.0.0.1",
                                port="5432",
                                database="python_pets")


@app.route('/', methods=['GET'])
def tests():
    print('made it to the server from JS')
    return "<h1>Hello World!</h1><p>From Python and Flask!</p>"

@app.route('/owners', methods=['GET'])
def get_owners():
    cursor = connection.cursor()
    query_text = "
                    SELECT "owners".id, "owners".name, COUNT("pets".name) FROM "owners"
                    JOIN "pets" on "owners".id = "pets".user_id
                    GROUP BY "owners".id;
                    "
    # execute query
    cursor.execute(query_text)
    # Selecting rows from mobile table using cursor.fetchall
    owners = cursor.fetchall()
    print(owners)
    # respond, status 200 is added for us
    return jsonify(owners)


app.run()
