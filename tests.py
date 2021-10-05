from dbservice import DbService, DbServiceError
from messagehandler import Errors

db = DbService()
def check_if_error(f, args):
	try:
		if type(args) != int and type(args) != str:
			f(*args)
		else:
			f(args)
		return 0
	except DbServiceError:
		return 1

if __name__ == '__main__':
	#Testing registration
	#logins
	assert check_if_error(db.add_user,('45asdasd', 'pas')) == 1
	assert check_if_error(db.add_user,('@asdasd', 'pas')) == 1
	assert check_if_error(db.add_user,(None, 'pas')) == 1
	assert check_if_error(db.add_user,('123', 'pas')) == 1
	assert check_if_error(db.add_user,(';;;;;', 'pas')) == 1
	assert check_if_error(db.add_user,('_asd', 'pas')) == 1
	assert check_if_error(db.add_user,('', 'pas')) == 1
	assert check_if_error(db.add_user,('ывфыв', 'pas')) == 1
	assert check_if_error(db.add_user,('kolasdasdasdin', 'pas')) == 1
	#passwords
	assert check_if_error(db.add_user,('log', '')) == 1
	assert check_if_error(db.add_user,('log', '"pas"')) == 1
	assert check_if_error(db.add_user,('log', None)) == 1
	assert check_if_error(db.add_user,('log', 'ф')) == 1
	assert check_if_error(db.add_user,('log', 'asd.asd')) == 1

	#Login tests
	#login
	assert check_if_error(db.get_user,('', 'admin')) == 1
	assert check_if_error(db.get_user,('ad', 'admin')) == 1
	assert check_if_error(db.get_user,('min', 'admin')) == 1
	assert check_if_error(db.get_user,('@asd', 'admin')) == 1
	assert check_if_error(db.get_user,(None, 'admin')) == 1
	#password
	assert check_if_error(db.get_user,('admin', 'min')) == 1
	assert check_if_error(db.get_user,('admin', '')) == 1
	assert check_if_error(db.get_user,('admin', 'admin1')) == 1
	assert check_if_error(db.get_user,('admin', ' admin')) == 1
	assert check_if_error(db.get_user,('admin', None)) == 1
	#success
	admin_id = db.get_user_id_by_login('kolasdasdasdin')
	assert check_if_error(db.get_user,('kolasdasdasdin', 'green')) == 0

	#Create item test
	#wrong data type
	assert check_if_error(db.add_item,(None, 0)) == 1
	assert check_if_error(db.add_item,(None, None)) == 1
	assert check_if_error(db.add_item,(0, None)) == 1
	assert check_if_error(db.add_item,(123, 0)) == 1
	#wrong user_id
	assert check_if_error(db.add_item,('None', 666)) == 1

	#Delete item
	#wrong types
	assert check_if_error(db.delete_item,(None, 0)) == 1
	assert check_if_error(db.delete_item,(None, None)) == 1
	assert check_if_error(db.delete_item,(0, None)) == 1
	assert check_if_error(db.delete_item,('123', 0)) == 1
	assert check_if_error(db.delete_item,('123', '0')) == 1
	#wrong item id
	assert check_if_error(db.delete_item,(123, 0)) == 1
	#wrong user id
	assert check_if_error(db.delete_item,(0, 123)) == 1

	#Get items list
	#wrong types
	assert check_if_error(db.get_items,'asd') == 1
	#wrong user id
	assert check_if_error(db.get_items,321) == 1
	#not a users' items
	assert check_if_error(db.get_items,2) == 1

	#Send item to user login
	#wrong types
	assert check_if_error(db.send_item,('0', 'ad', 0)) == 1
	assert check_if_error(db.send_item,(0, None, 0)) == 1
	assert check_if_error(db.send_item,(0, 'ad', '0')) == 1
	assert check_if_error(db.send_item,(None, None, None)) == 1
	#wrong user id 
	assert check_if_error(db.send_item,(2, 'ad', 666)) == 1
	#wrong login
	assert check_if_error(db.send_item,(2, 'adasd', 0)) == 1
	#wrong item id
	assert check_if_error(db.send_item,(666, 'ad', 0)) == 1

	key = '1GGN6F'
	#wrong types
	assert check_if_error(db.receive_item,('1',key)) == 1
	assert check_if_error(db.receive_item,(1,123)) == 1
	#wrong user id
	assert check_if_error(db.receive_item,(666,key)) == 1
	#wrong key
	assert check_if_error(db.receive_item,(1,'ASDASD')) == 1
	
	print('Test successfully passed')






	
