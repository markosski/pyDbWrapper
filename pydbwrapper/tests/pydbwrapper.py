
import unittest
from pydbwrapper import pydbwrapper

db = pydbwrapper.PyDbWrapper({
	'user':'root', 
	'password':'martek123',
	'host':'localhost',
	'dbname':'test'
	})   

query = 'SELECT * FROM users'
users = db.fetchAll(query)
users = db.fetchFirst(query)

print users
print db.info

print 'done'

