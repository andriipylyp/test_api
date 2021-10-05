from flask import Flask, request, json, session, Response
from dbservice import DbService, DbServiceError
from messagehandler import Api
db = DbService()

app = Flask(__name__)
app.secret_key = 'super secret key'

def response_f(response, status):
	return Response(
			response=json.dumps(response),
			status=status,
			mimetype='application/json'
			)

@app.route('/registration', methods=['POST'])
def registration():
	json_body = request.get_json()
	try:
		login, password = [json_body['login'], json_body['password']]
		db.add_user(login, password)
		return response_f({'Message':Api.operation_success('Operation')}, 200)
	except KeyError:
		return response_f({'Message':Api.not_provided('Login', 'Password')}, 400)
	except DbServiceError as e:
		return response_f({'Message':str(e)}, 400)

@app.route('/login', methods=['POST'])
def login():
	json_body = request.get_json()
	try:
		login, password = [json_body['login'], json_body['password']]
		id = db.get_user(login, password)
		session['login'] = login
		session['user_id'] = id
		return response_f({'Message':Api.operation_success('Login')}, 200)
	except KeyError:
		return response_f({'Message':Api.not_provided('Login', 'Password')}, 400)
	except DbServiceError as e:
		return response_f({'Message':str(e)}, 400)
	

@app.route('/items/new', methods=['POST'])
def new_item():
	json_body = request.get_json()
	try:
		name = json_body['name']
	except KeyError:
		return response_f({'Message':Api.not_provided('Item name')},400)
	try:
		id = db.add_item(name,session['user_id'])
		return response_f({'Message':Api.operation_success('Item creation'), 'Id':id, 'Name':name},200)
	except KeyError:
		return response_f({'Message':Api.not_logged()},401)
	except DbServiceError as e:
		return response_f({'Message':str(e)},403)

@app.route('/items/<id>', methods=['DELETE'])
def delete_item(id):
	try:
		db.delete_item(id, session['user_id'])
		return response_f({'Message':Api.operation_success('Detete')},200)
	except KeyError:
		return response_f({'Message':Api.not_logged()},401)
	except DbServiceError as e:
		return response_f({'Message':str(e)},403)

@app.route('/items', methods=['GET'])
def get_items_from_db():
	try:
		items = db.get_items(session['user_id'])
		return response_f(items,200)
	except KeyError:
		return response_f({'Message':Api.not_logged()},401)
	except DbServiceError as e:
		return response_f({'Message':str(e)},403)

@app.route('/send', methods=['POST'])
def generate_link():
	json_body = request.get_json()
	try:
		item_id, user_login = [json_body['id'], json_body['login']]
	except KeyError:
		return response_f({'Message':Api.not_provided('id', 'login')+' OR '+Api.not_logged()},400)
	try:
		key = db.send_item(item_id, user_login, session['user_id'])
		return response_f({'Link':f'localhost:5000/get/{key}'},200)
	except KeyError:
		return response_f({'Message':Api.not_logged()},401)
	except DbServiceError as e:
		return response_f({'Message':str(e)},403)

@app.route('/get/<key>', methods=['GET'])
def get_item(key):
	try:
		db.receive_item(session['user_id'], key)
		return response_f({'Message':Api.operation_success('Transfer')}, 200)
	except KeyError:
		return response_f({'Message':Api.not_logged()},401)
	except DbServiceError as e:
		print(str(e))
		return response_f({'Message':str(e)}, 403)

if __name__ == '__main__':
   app.run(debug=True)