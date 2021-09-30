import pymongo
import random
import string
import certifi
import re

class db_service:
	is_instance = 0
	def __init__(self):
		if db_service.check_if_instance():
			db_service.is_instance = 1
			client = pymongo.MongoClient('mongodb+srv://root:root@cluster0.mlnhr.mongodb.net/test_api', tlsCAFile=certifi.where())
			db = client['test_api']
			self.__users = db['users']
			self.__items = db['items']
		else:
			raise RuntimeError('Only one instance of db_service can exist.')

	@classmethod
	def check_if_instance(cls):
		return 1 if cls.is_instance == 0 else 0

	@staticmethod
	def get_last_id(obj):
		ID = list(obj.find({}, {'_id': True}).sort('_id', pymongo.DESCENDING).limit(1))
		return ID[0]['_id'] if len(ID) > 0 else -1

	@staticmethod
	def create_token(quantity):
		return ''.join(random.choices(string.ascii_uppercase + string.digits, k=quantity))

	@staticmethod
	def check_login(s):
		return re.search('^[a-zA-Z]([A-Za-z0-9_@$%&\.])*$', s)

	@staticmethod
	def check_password(s):
		return re.search('^[a-zA-Z0-9_@$^%&]([A-Za-z0-9_@$%&^])*$', s)

	def check_if_login(self, login):
		return 0 if len(list(self.__users.find({'_login':login}, {'_id':True}))) == 0 else 1

	def add_user(self, login:str, password:str) -> list:
		if type(password) is str and type(login) is str and db_service.check_login(login) != None and db_service.check_password(password) != None:
			try:
				if not self.check_if_login(login):
					self.__users.insert_one({'_id': db_service.get_last_id(self.__users)+1, '_login': login, 'password': password})
					return [1, '']
				else:
					return [0, 'Login occupied.']
			except pymongo.errors.PyMongoError as e:
				return [0, e]
		else:
			return [0, 'login or password has wrong type OR login or password has incorrect characters.']

	def get_user(self, login:str, password:str) -> list:
		if type(password) is str and type(login) is str:
			try:
				res = list(self.__users.find({'_login': login, 'password': password}, {'_id':True}))
				print(res)
				if len(res) > 0:
					return [1, res[0]['_id']]
				else:
					return [0, 'wrong login or password.']
			except pymongo.errors.PyMongoError as e:
				return [0, e]
		else:	
			return [0, 'wrong login, password types.']

	def add_item(self, name: str, user_id: int) -> list:
		if type(user_id) is int and type(name) is str:
			try:
				if self.get_user_by_id(user_id) != None:
					self.__items.insert_one({'_id': db_service.get_last_id(self.__items)+1, 'name': name, 'user_id':user_id})
					return [1, db_service.get_last_id(self.__items)]
				else:
					return [0, 'user not found.']
			except pymongo.errors.PyMongoError as e:
				return [0, e]
		else:
			return [0, 'name must be str and user_id must be int.']

	def delete_item(self, item_id: int, user_id: int) -> list:
		if type(item_id) is int and self.__items.find_one({'_id':item_id}) != None and type(user_id) is int:
			if self.get_user_by_id(user_id) != None:
				self.__items.delete_one({'_id': item_id, 'user_id':user_id})
				return [1, '']
			else:
				return [0, 'user not found.']
		else:
			return [0, 'item_id, user_id must be integers or item does not exist.']

	def get_items(self, user_id: int) -> list:
		if type(user_id) is int and self.__users.find_one({'_id':user_id}) != None:
			items = self.__items.find({'user_id':user_id})
			return [1,list(items)] if len(list(items)) > 0 else [1,'no items']
		else:
			return [0, 'user user_id must be integer or user does not exist.']

	def send_item(self, item_id: int, login: str, user_id:int) -> list:
		if type(item_id) is int and type(login) is str and type(user_id) is int:
			if self.__users.find_one({'_login':login}, {'_id':True}) != None and self.__items.find_one({'_id':item_id, 'user_id':user_id}) != None and self.__users.find_one({'_id': user_id}) != None:
				key = db_service.create_token(6)
				self.__items.update_one({'_id':item_id}, {'$set': {'new_user_login': login, 'key':key}})
				return [1, key]
			return [0, 'item or user does not exist.']
		else:
			return [0, 'wrong item_id(must be int) or login(must be string) or user_id(must be int).']

	def receive_item(self, user_id: int, key: str) -> list:
		if type(user_id) is int and type(key) is str:
			res = list(self.__users.find({'_id':user_id}, {'_id': False, '_login':True}))
			item_to_receive = []
			if len(res) > 0:
				login = res[0]['_login']
				res = list(self.__items.find({'new_user_login':login, 'key':key}, {'_id':True}))
				if len(res) > 0:
					item_to_receive = res[0]['_id']
			return [1, self.__items.update_one({'_id':item_to_receive}, {'$set': {'user_id':user_id}, '$unset': {'new_user_login':'', 'key':''}})] if len(item_to_receive) > 0 else [0, 'Nothing to receive']
		else:
			return [0, 'wrong user_id, key type.']

	def get_last_user(self):
		return list(self.__users.find({'_id':db_service.get_last_id(self.__users)}))

	def get_user_id_by_login(self, login):
		return list(self.__users.find({'_login':login}, {'_id':True, '_login': False}))[0]['_id']

	def get_user_by_id(self, id):
		return self.__users.find_one({'_id':id}, {'_id':True})

