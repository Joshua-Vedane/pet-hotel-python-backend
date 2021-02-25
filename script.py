import flask
import psycopg2
from flask import request, jsonify, make_response
from psycopg2.extras import RealDictCursor

app = flask.Flask(__name__)
app.config["DEBUG"] = True



# Get all Pets
@app.route('/dashboard', methods=['GET'])
def get_pets():
  connection = psycopg2.connect(user="travishuss",
                                host="127.0.0.1",
                                port="5432",
                                database="python_pets")
  print('made it to get pets')
  cursor = connection.cursor(cursor_factory=RealDictCursor)
  query_text= "SELECT * FROM pets"
  # execute query
  cursor.execute(query_text)
  # Selecting rows from mobile table using cursor.fetchall
  pets = cursor.fetchall()
  print(pets)
  # respond, status 200 is added for us
  return jsonify(pets)
  
## Add a pet 
@app.route('/dashboard', methods=['POST'])
def add_pet():
  user_id = request.form['owner']
  name = request.form['name']
  breed = request.form['breed']
  color = request.form['color']
  try: 
    connection = psycopg2.connect(user="travishuss",
                                host="127.0.0.1",
                                port="5432",
                                database="python_pets")
    # avoid array of arrays
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    print(f'adding {name} color: {color} breed: {breed} with user {user_id}')
    query_text = "INSERT INTO pets (user_id, name, breed, color) VALUES(%s,%s,%s,%s) "
    # execute the query
    cursor.execute(query_text, (user_id, name, breed, color))
    # really for sure commit the query
    connection.commit()
    count = cursor.rowcount
    print(count, "pet added")
    # respond nicely
    result = {'status': 'CREATED'}
    return make_response(jsonify(result), 201)
  except (Exception, psycopg2.Error) as error:
    # there was a problem
    if(connection):
        print("Failed to insert book", error)
        # respond with error
        result = {'status': 'ERROR'}
        return make_response(jsonify(result), 500)
  finally:
    # closing database connection.
    if(connection):
        # clean up our connections
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")


@app.route('/', methods=['GET'])
def tests():
    print('made it to the server from JS')
    return "<h1>Hello World!</h1><p>From Python and Flask!</p>"

@app.route('/owners', methods=['GET'])
def get_owners():
    # makes connection to postgresDB
    connection = psycopg2.connect(user="travishuss", host="127.0.0.1", port="5432", database="python_pets")

    cursor = connection.cursor(cursor_factory=RealDictCursor)

    query_text = "SELECT owners.id, owners.name, COUNT(pets.name) FROM owners LEFT JOIN pets on owners.id = pets.user_id GROUP BY owners.id"

    # execute query
    cursor.execute(query_text)
    # Selecting rows from mobile table using cursor.fetchall
    owners = cursor.fetchall()
    print(owners)
    # respond, status 200 is added for us
    return jsonify(owners)

@app.route('/owners', methods=['POST'])
def add_owner():
    # print(request.form)
    print('in ownerPost')
    name = request.form['name']
    try:
        # makes connection to postgresDB
        connection = psycopg2.connect(user="travishuss", host="127.0.0.1", port="5432", database="python_pets")
        # Avoid getting arrays of arrays!
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        print(name)
        insertQuery = "INSERT INTO owners (name) VALUES (%s)"
        # if only only one param, still needs to be a tuple --> cursor.execute(insertQuery, (title,)) <-- comma matters!
        cursor.execute(insertQuery, (name,))
        # really for sure commit the query
        connection.commit()
        count = cursor.rowcount
        print(count, "Owner inserted")
        # respond nicely
        result = {'status': 'CREATED'}
        return make_response(jsonify(result), 201)
    except (Exception, psycopg2.Error) as error:
        # there was a problem
        if(connection):
            print("Failed to create owner", error)
            # respond with error
            result = {'status': 'ERROR'}
            return make_response(jsonify(result), 500)
    finally:
        # closing database connection.
        if(connection):
            # clean up our connections
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

@app.route('/owners/<int:id>', methods=['DELETE'])
def delete_owner(id):
    print('in delete owner')
    print(id)
    try:
        connection = psycopg2.connect(user="travishuss", host="127.0.0.1", port="5432", database="python_pets")
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        query_text = "DELETE FROM owners where id = %s"
        cursor.execute(query_text, (id,))
        connection.commit()
        count = cursor.rowcount
        print(count, "Owner deleted")
        # respond nicely
        result = {'status': 'deleted'}
        return make_response(jsonify(result), 201)
    except (Exception, psycopg2.Error) as error:
        if(connection):
            print("Failed to delete owner", error)
            # respond with error
            result = {'status': 'ERROR'}
            return make_response(jsonify(result), 500)
    finally:
        # closing database connection.
        if(connection):
            # clean up our connections
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
app.run()
