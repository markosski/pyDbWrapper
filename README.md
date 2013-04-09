===========
pydbwrapper
==========

PyDbWrapper is a simple wrapper around MySQL-python library.


USAGE
=====

Creating object instance:

	from pydbwrapper import PyDbWrapper
	
	db = PyDbWrapper({
		'user'		:'root', 
		'password'	:'somepass',
		'host'		:'localhost',
		'dbname'	:'test'
	}) 

To execute INSERT, UPDATE query just pass it to execute() method:

	db.execute('INSERT INTO `test` SET `name` = "something"')

To retrieve records:

	data = db.fetchAll('SELECT * FROM `test`')
or
	data = db.fetchFirst('SELECT * FROM `test`')

OBJECT SETTINGS
---------------

* get info about executed queries
	print db.info

* get last insert autoincrement ID
	db.lastInsertId

* cache on/off
	db.sql_no_cache = bool (False)

* autocommit on/off
	db.autocommit = bool (True)

* charset
	db.charset = str (utf8)