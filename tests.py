from db_service import db_service
db = db_service()
if __name__ == '__main__':
	#Testing registration
	#logins
	assert db.add_user('45asdasd', 'pas') == [0, 'login or password has wrong type OR login or password has incorrect characters.']
	assert db.add_user('@asdasd', 'pas') == [0, 'login or password has wrong type OR login or password has incorrect characters.']
	assert db.add_user(None, 'pas') == [0, 'login or password has wrong type OR login or password has incorrect characters.']
	assert db.add_user('123', 'pas') == [0, 'login or password has wrong type OR login or password has incorrect characters.']
	assert db.add_user(';;;;;', 'pas') == [0, 'login or password has wrong type OR login or password has incorrect characters.']
	assert db.add_user('_asd', 'pas') == [0, 'login or password has wrong type OR login or password has incorrect characters.']
	assert db.add_user('', 'pas') == [0, 'login or password has wrong type OR login or password has incorrect characters.']
	assert db.add_user('ывфыв', 'pas') == [0, 'login or password has wrong type OR login or password has incorrect characters.']
	assert db.add_user('admin', 'pas') == [0, 'Login occupied.']
	#passwords
	assert db.add_user('log', '') == [0, 'login or password has wrong type OR login or password has incorrect characters.']
	assert db.add_user('log', '"pas"') == [0, 'login or password has wrong type OR login or password has incorrect characters.']
	assert db.add_user('log', None) == [0, 'login or password has wrong type OR login or password has incorrect characters.']
	assert db.add_user('log', 'ф') == [0, 'login or password has wrong type OR login or password has incorrect characters.']
	assert db.add_user('log', 'asd.asd') == [0, 'login or password has wrong type OR login or password has incorrect characters.']

	#Login tests
	#login
	assert db.get_user('', 'admin') == [0, 'wrong login or password.']
	assert db.get_user('ad', 'admin') == [0, 'wrong login or password.']
	assert db.get_user('min', 'admin') == [0, 'wrong login or password.']
	assert db.get_user('@asd', 'admin') == [0, 'wrong login or password.']
	assert db.get_user(None, 'admin') == [0, 'wrong login, password types.']
	#password
	assert db.get_user('admin', 'min') == [0, 'wrong login or password.']
	assert db.get_user('admin', '') == [0, 'wrong login or password.']
	assert db.get_user('admin', 'admin1') == [0, 'wrong login or password.']
	assert db.get_user('admin', ' admin') == [0, 'wrong login or password.']
	assert db.get_user('admin', None) == [0, 'wrong login, password types.']
	#success
	admin_id = db.get_user_id_by_login('admin')
	assert db.get_user('admin', 'admin') == [1, admin_id]

	#Create item test
	#wrong data type
	assert db.add_item(None, 0) == [0, 'name must be str and user_id must be int.']
	assert db.add_item(None, None) == [0, 'name must be str and user_id must be int.']
	assert db.add_item(0, None) == [0, 'name must be str and user_id must be int.']
	assert db.add_item(123, 0) == [0, 'name must be str and user_id must be int.']
	#wrong user_id
	assert db.add_item('None', 666) == [0, 'user not found.']

	#Delete item
	#wrong types
	assert db.delete_item(None, 0) == [0, 'item_id, user_id must be integers or item does not exist.']
	assert db.delete_item(None, None) == [0, 'item_id, user_id must be integers or item does not exist.']
	assert db.delete_item(0, None) == [0, 'item_id, user_id must be integers or item does not exist.']
	assert db.delete_item('123', 0) == [0, 'item_id, user_id must be integers or item does not exist.']
	assert db.delete_item('123', '0') == [0, 'item_id, user_id must be integers or item does not exist.']
	#wrong item id
	assert db.delete_item(123, 0) == [0, 'item_id, user_id must be integers or item does not exist.']
	#wrong user id
	assert db.delete_item(0, 123) == [0, 'user not found.']

	#Get items list
	#wrong types
	assert db.get_items('asd') == [0, 'user user_id must be integer or user does not exist.']
	#wrong user id
	assert db.get_items(321) == [0, 'user user_id must be integer or user does not exist.']
	#no users' items
	assert db.get_items(1) == [1,'no items']

	#Send item to user login
	#wrong types
	assert db.send_item('0', 'ad', 0) == [0, 'wrong item_id(must be int) or login(must be string) or user_id(must be int).']
	assert db.send_item(0, None, 0) == [0, 'wrong item_id(must be int) or login(must be string) or user_id(must be int).']
	assert db.send_item(0, 'ad', '0') == [0, 'wrong item_id(must be int) or login(must be string) or user_id(must be int).']
	assert db.send_item(None, None, None) == [0, 'wrong item_id(must be int) or login(must be string) or user_id(must be int).']
	#wrong user id 
	assert db.send_item(2, 'ad', 666) == [0, 'item or user does not exist.']
	#wrong login
	assert db.send_item(2, 'adasd', 0) == [0, 'item or user does not exist.']
	#wrong item id
	assert db.send_item(666, 'ad', 0) == [0, 'item or user does not exist.']

	#Receiving test with full link: localhost:5000/get/1GGN6F
	key = '1GGN6F'
	user_id = 1
	#wrong types
	assert db.receive_item('1',key) == [0, 'wrong user_id, key type.']
	assert db.receive_item(1,123) == [0, 'wrong user_id, key type.']
	#wrong user id
	assert db.receive_item(666,key) == [0, 'Nothing to receive']
	#wrong key
	assert db.receive_item(1,'ASDASD') == [0, 'Nothing to receive']
	






	
