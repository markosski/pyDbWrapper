import unittest
from sys import exit
from pydbwrapper import pydbwrapper

db = pydbwrapper.PyDbWrapper({
	'user'		:'root', 
	'password'	:'martek123',
	'host'		:'localhost',
	'dbname'	:'test'
	})   

# db.sql_no_cache = True


# Create temp table
query = """
CREATE TABLE IF NOT EXISTS `test`.`pydbwrapper_test` (
  `userID` int(11) NOT NULL AUTO_INCREMENT,
  `userName` varchar(50) NOT NULL,
  `userEmail` varchar(100) NOT NULL,
  PRIMARY KEY (`userID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;
"""
db.execute(query)

db.execute('TRUNCATE TABLE `test`.`pydbwrapper_test`;')

query = """
INSERT INTO `pydbwrapper_test`
	(`userName`, `userEmail`)
VALUES
	("Marcin", "marcin@gmail.com")
	,("Barbara", "barbara@gmail.net")
	,("Tomasz", "tomasz@gmail.com")
	,("Pawel", "pawel@gmail.com");
"""

db.execute(query)

query = "SELECT * FROM `pydbwrapper_test`"
users = db.fetchAll(query)

print '--- GET ALL ---'

for user in users:
	print 'Name: %s, email: %s' % (user['userName'], user['userEmail'])

user = db.fetchFirst(query)

print '--- GET ONE ---'
print 'Name: %s, email: %s' % (user['userName'], user['userEmail'])

print '--- PYDBWRAPPER INFO ---'
print db.info
