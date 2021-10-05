import pymongo
from bson.objectid import ObjectId
import random
import string
import certifi
import re
from messagehandler import Errors

def singleton(class_):
	instances = {}
	def getinstance():
		if class_ not in instances:
			instances[class_] = class_()
		return instances[class_]
	return getinstance

class DbServiceError(Exception):
	pass

class StaticMethods:
	def __init__(self) -> None:
		pass
	
	@staticmethod
	def create_token(quantity:int) -> string:
		return ''.join(random.choices(string.ascii_uppercase + string.digits, k=quantity))

	@staticmethod
	def check_login(s:string) -> re:
		return re.search('^[a-zA-Z]([A-Za-z0-9_@$%&\.])*$', s)

	@staticmethod
	def check_password(s:string) -> re:
		return re.search('^[a-zA-Z0-9_@$^%&]([A-Za-z0-9_@$%&^])*$', s)
@singleton
class DbService(StaticMethods):
	def __init__(self) -> None:
		client = pymongo.MongoClient('mongodb+srv://root:root@cluster0.mlnhr.mongodb.net/test_api', tlsCAFile=certifi.where())
		db = client['test_api']
		self.__users = db['users']
		self.__items = db['items']

	def check_if_login(self, login:string) -> int:
		return 0 if len(list(self.__users.find({'_login':login}, {'_id':True}))) == 0 else 1

	def add_user(self, login:str, password:str) -> list:
		if type(password) is str and type(login) is str and super().check_login(login) != None and super().check_password(password) != None:
			if not self.check_if_login(login):
				self.__users.insert_one({'_id': str(ObjectId()), '_login': login, 'password': password})
				return
			else:
				raise DbServiceError(Errors.login_occupied())
		else:
			raise DbServiceError(Errors.wrong_login_pas())

	def get_user(self, login:str, password:str) -> list:
		if type(password) is str and type(login) is str:
			res = list(self.__users.find({'_login': login, 'password': password}, {'_id':True}))
			if len(res) > 0:
				return res[0]['_id']
			else:
				raise DbServiceError(Errors.wrong_login_pas())
		else:	
			raise DbServiceError(str(Errors('login', 'password')))

	def add_item(self, name: str, user_id: str) -> list:
		if type(user_id) is str and type(name) is str and len(name) > 0:
			if self.get_user_by_id(user_id) != None:
				id = str(ObjectId())
				self.__items.insert_one({'_id': id, 'name': name, 'user_id':user_id})
				return id
			else:
				raise DbServiceError(Errors.user_not_found())
		else:
			raise DbServiceError(str(Errors('user_id', 'name')))

	def delete_item(self, item_id: int, user_id: str) -> list:
		if type(item_id) is str and self.__items.find_one({'_id':item_id}) != None and type(user_id) is str:
			if self.get_user_by_id(user_id) != None:
				self.__items.delete_one({'_id': item_id, 'user_id':user_id})
				return
			else:
				raise DbServiceError(Errors.user_not_found())
		else:
			raise DbServiceError(str(Errors('item_id', 'user_id'))+' OR '+Errors.item_not_found())

	def get_items(self, user_id: str) -> list:
		if type(user_id) is str and self.__users.find_one({'_id':user_id}) != None:
			items = list(self.__items.find({'user_id':user_id}, {'_id':True, 'name':True}))
			if len(items) != 0:
				return items
			raise DbServiceError(Errors.item_not_found())
		else:
			raise DbServiceError(Errors.user_not_found())

	def send_item(self, item_id: int, login: str, user_id:int) -> list:
		if type(item_id) is str and type(login) is str and type(user_id) is str:
			if self.__users.find_one({'_login':login}, {'_id':True}) != None and self.__items.find_one({'_id':item_id, 'user_id':user_id}) != None and self.__users.find_one({'_id': user_id}) != None:
				key = super().create_token(6)
				self.__items.update_one({'_id':item_id}, {'$set': {'new_user_login': login, 'key':key}})
				return key
			raise DbServiceError(Errors.user_not_found()+' OR '+Errors.item_not_found())
		else: 
			raise DbServiceError(str(Errors('item_id', 'login', 'user_id')))

	def receive_item(self, user_id: str, key: str) -> list:
		if type(user_id) is str and type(key) is str:
			res = list(self.__users.find({'_id':user_id}, {'_id': False, '_login':True}))
			item_to_receive = []
			if len(res) > 0:
				login = res[0]['_login']
				res = list(self.__items.find({'new_user_login':login, 'key':key}, {'_id':True}))
				if len(res) > 0:
					item_to_receive = res[0]['_id']
				if type(item_to_receive) is not list:
					self.__items.update_one({'_id':item_to_receive}, {'$set': {'user_id':user_id}, '$unset': {'new_user_login':'', 'key':''}})
					return
			raise DbServiceError(Errors.nothing_to_receive())
		else:
			raise DbServiceError(str(Errors('user_id', 'key')))

	def get_user_id_by_login(self, login:string) -> list:
		return list(self.__users.find({'_login':login}, {'_id':True, '_login': False}))[0]['_id']

	def get_user_by_id(self, id:int):
		return self.__users.find_one({'_id':id}, {'_id':True})
