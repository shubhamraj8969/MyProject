import mysql.connector
from configs import dbconfig

from mysql.connector.errors import Error


class  DBHelper(object):
	def __init__(self):
		self.db = dbconfig.DB['db']
		self.host = dbconfig.DB['host']
		self.port = dbconfig.DB['port']
		self.user = dbconfig.DB['user']
		self.password = dbconfig.DB['password']
		self.type = dbconfig.DB['type']
		self.connection = mysql.connector.connect(user = self.user, password = self.password, host = self.host, database = self.db)
		self.cursor = self.connection.cursor(dictionary = True)
		self.cursor.execute('set global max_allowed_packet=524288000')

	def Connection(self):
		return self.connection

	def query(self, queryStr, queryParams=None):
		try:
			if queryParams != None:
				self.cursor.execute(queryStr,queryParams)
			else:
				self.cursor.execute(queryStr)
			return self.cursor
		except Error as e:
			print(e)
			raise(e)

	def transact(self, queryStr, queryParams=()):
		try:
			self.cursor.execute(queryStr, queryParams)
			return self.cursor.lastrowid
		except Error as e:
			print(e)
			raise(e)

	def commit(self):
		try:
			self.connection.commit()

		except Error as e:
			print(e)
			raise(e)

	def __del__(self):
		self.commit()
		self.cursor.close()
		self.connection.close()
