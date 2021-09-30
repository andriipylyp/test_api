from db_service import db_service
from message_handler import errors

db = db_service()
if __name__ == '__main__':
	#Testing registration
	#logins
	assert db.add_user('45asdasd', 'pas') == [0, str(errors('login', 'password'))+' OR '+errors.wrong_login_pas()]
	assert db.add_user('@asdasd', 'pas') == [0, str(errors('login', 'password'))+' OR '+errors.wrong_login_pas()]
	assert db.add_user(None, 'pas') == [0, str(errors('login', 'password'))+' OR '+errors.wrong_login_pas()]
	assert db.add_user('123', 'pas') == [0, str(errors('login', 'password'))+' OR '+errors.wrong_login_pas()]
	assert db.add_user(';;;;;', 'pas') == [0, str(errors('login', 'password'))+' OR '+errors.wrong_login_pas()]
	assert db.add_user('_asd', 'pas') == [0, str(errors('login', 'password'))+' OR '+errors.wrong_login_pas()]
	assert db.add_user('', 'pas') == [0, str(errors('login', 'password'))+' OR '+errors.wrong_login_pas()]
	assert db.add_user('ывфыв', 'pas') == [0, str(errors('login', 'password'))+' OR '+errors.wrong_login_pas()]
	assert db.add_user('admin', 'pas') == [0, errors.login_occupied()]
	#passwords
	assert db.add_user('log', '') == [0, str(errors('login', 'password'))+' OR '+errors.wrong_login_pas()]
	assert db.add_user('log', '"pas"') == [0, str(errors('login', 'password'))+' OR '+errors.wrong_login_pas()]
	assert db.add_user('log', None) == [0, str(errors('login', 'password'))+' OR '+errors.wrong_login_pas()]
	assert db.add_user('log', 'ф') == [0, str(errors('login', 'password'))+' OR '+errors.wrong_login_pas()]
	assert db.add_user('log', 'asd.asd') == [0, str(errors('login', 'password'))+' OR '+errors.wrong_login_pas()]

	#Login tests
	#login
	assert db.get_user('', 'admin') == [0, errors.wrong_login_pas()]
	assert db.get_user('ad', 'admin') == [0, errors.wrong_login_pas()]
	assert db.get_user('min', 'admin') == [0, errors.wrong_login_pas()]
	assert db.get_user('@asd', 'admin') == [0, errors.wrong_login_pas()]
	assert db.get_user(None, 'admin') == [0, str(errors('login', 'password'))]
	#password
	assert db.get_user('admin', 'min') == [0, errors.wrong_login_pas()]
	assert db.get_user('admin', '') == [0, errors.wrong_login_pas()]
	assert db.get_user('admin', 'admin1') == [0, errors.wrong_login_pas()]
	assert db.get_user('admin', ' admin') == [0, errors.wrong_login_pas()]
	assert db.get_user('admin', None) == [0, str(errors('login', 'password'))]
	#success
	admin_id = db.get_user_id_by_login('admin')
	assert db.get_user('admin', 'admin') == [1, admin_id]

	#Create item test
	#wrong data type
	assert db.add_item(None, 0) == [0, str(errors('user_id', 'name'))]
	assert db.add_item(None, None) == [0, str(errors('user_id', 'name'))]
	assert db.add_item(0, None) == [0, str(errors('user_id', 'name'))]
	assert db.add_item(123, 0) == [0, str(errors('user_id', 'name'))]
	#wrong user_id
	assert db.add_item('None', 666) == [0, errors.user_not_found()]

	#Delete item
	#wrong types
	assert db.delete_item(None, 0) == [0, str(errors('item_id', 'user_id'))+' OR '+errors.item_not_found()]
	assert db.delete_item(None, None) == [0, str(errors('item_id', 'user_id'))+' OR '+errors.item_not_found()]
	assert db.delete_item(0, None) == [0, str(errors('item_id', 'user_id'))+' OR '+errors.item_not_found()]
	assert db.delete_item('123', 0) == [0, str(errors('item_id', 'user_id'))+' OR '+errors.item_not_found()]
	assert db.delete_item('123', '0') == [0, str(errors('item_id', 'user_id'))+' OR '+errors.item_not_found()]
	#wrong item id
	assert db.delete_item(123, 0) == [0, str(errors('item_id', 'user_id'))+' OR '+errors.item_not_found()]
	#wrong user id
	assert db.delete_item(0, 123) == [0, errors.user_not_found()]

	#Get items list
	#wrong types
	assert db.get_items('asd') == [0, str(errors('user_id'))+' OR '+errors.user_not_found()]
	#wrong user id
	assert db.get_items(321) == [0, str(errors('user_id'))+' OR '+errors.user_not_found()]
	#not a users' items
	assert db.get_items(2) == [1,errors.item_not_found()]

	#Send item to user login
	#wrong types
	assert db.send_item('0', 'ad', 0) == [0, str(errors('item_id', 'login', 'user_id'))]
	assert db.send_item(0, None, 0) == [0, str(errors('item_id', 'login', 'user_id'))]
	assert db.send_item(0, 'ad', '0') == [0, str(errors('item_id', 'login', 'user_id'))]
	assert db.send_item(None, None, None) == [0, str(errors('item_id', 'login', 'user_id'))]
	#wrong user id 
	assert db.send_item(2, 'ad', 666) == [0, errors.user_not_found()+' OR '+errors.item_not_found()]
	#wrong login
	assert db.send_item(2, 'adasd', 0) == [0, errors.user_not_found()+' OR '+errors.item_not_found()]
	#wrong item id
	assert db.send_item(666, 'ad', 0) == [0, errors.user_not_found()+' OR '+errors.item_not_found()]

	#Receiving test with full link: localhost:5000/get/1GGN6F
	key = '1GGN6F'
	user_id = 1
	#wrong types
	assert db.receive_item('1',key) == [0, str(errors('user_id', 'key'))]
	assert db.receive_item(1,123) == [0, str(errors('user_id', 'key'))]
	#wrong user id
	assert db.receive_item(666,key) == [0, errors.nothing_to_receive()]
	#wrong key
	assert db.receive_item(1,'ASDASD') == [0, errors.nothing_to_receive()]
	






	
