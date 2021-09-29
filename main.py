from flask import Flask, request, json, session, Response
from db_service import db_service
db = db_service()

app = Flask(__name__)
app.secret_key = 'super secret key'

def response_f(response, status, token=None):
	return Response(
			response=json.dumps(response),
			status=status,
			mimetype='application/json'
			)

@app.route('/registration', methods=['POST'])
def registration():
	login, password = [request.form['login'], request.form['password']]
	if login and password:
		status, res = db.add_user(login, password)
		if status == 1:
			return response_f({'Message':'Operation was successful.'}, 200)
		else:
			return response_f({'Message':res}, 409)
	else:
		return response_f({'Message':'Login or password was not provided.'}, 204)

@app.route('/login', methods=['POST'])
def login():
	login, password = [request.form['login'], request.form['password']]
	if login and password:
		status, res = db.get_user(login, password)
		if status == 1:
			session['login'] = login
			session['user_id'] = res
			return response_f({'Message':'Successfuly logged.'}, 200)
		else:
			return response_f({'Message':'Wrong login or password.'}, 403)
	else:
		return response_f({'Message':'Login or password was not provided.'}, 204)

@app.route('/items/new', methods=['POST'])
def new_item():
	name = request.form['name']
	if name and session['user_id']:
		status, res = db.add_item(name,session['user_id'])
		if status == 1:
			return response_f({'Message':'Item successfuly created', 'Id':res, 'Name':name},200)
		else:
			return response_f({'Message':res},500)
	else:
		return response_f({'Message':'Name was not provided or you are not logged.'},204)

@app.route('/items/<id>', methods=['DELETE'])
def delete_item(id):
	item_id = int(id)
	status, res = db.delete_item(item_id, session['user_id'])
	if status == 1:
		return response_f({'Message':'Item was deleted.'},200)
	else:
		return response_f({'Message':res},500)

@app.route('/items', methods=['GET'])
def get_items_from_db():
	status, res = db.get_items(session['user_id'])
	if status == 1:
		return response_f(res,200)
	return response_f({'Message':res},204)

@app.route('/send', methods=['POST'])
def generate_link():
	item_id, user_login = [int(request.form['id']), request.form['login']]
	if item_id and user_login and session['user_id']:
		status, res = db.send_item(item_id, user_login, session['user_id'])
		if status == 1:
			return response_f({'Link':f'localhost:5000/get/{res}'},200)
		else:
			return response_f({'Message':res}, 406)
	else:
		return response_f({'Message':'Item id or user login was not provided or you are not logged.'},204)

@app.route('/get/<key>', methods=['GET'])
def get_item(key):
	status, res = db.receive_item(session['user_id'], key)
	if status == 1:
		return response_f({'Message':'Item successfuly transfered'}, 200)
	else:
		return response_f({'Message':res}, 406)

if __name__ == '__main__':
   app.run(debug=True)