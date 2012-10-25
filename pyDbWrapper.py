#!/usr/bin/python

import os
import re
import sys
import pdb
import time
import MySQLdb
import ConfigParser

__version__ = '0.1'

"""PyDbWrapper

0.1 - 2012-10-01
    Fixed empty opts dictionary in execute method
    Added lastInsertId class property
    Added charset property, set to utf8 by default
"""


class PyDbWrapper:
    def __init__(self, dbName, **opts):
        optsDefaults = {
            'config': os.path.dirname(os.path.abspath(__file__)) + '/pyDbWrapperConnections.ini'
        }

        opts = dict(optsDefaults, **opts)

        self.conn = None
        self.dbName = None
        self.connections = None
        self.cur = None
        self.query = None
        self.sqlCacheOn = True
        self.info = {
            'executed': [],
            'connStats': None,
            'lastInsertId': None,
            'totalExecutionTime': None
        }
        self.lastInsertId = None
        self.charset = 'utf8'

        # Load config file with defined connections
        if opts['config'] and os.path.exists(opts['config']):
            self.configPath = opts['config']
        # Otherwise throw exception
        else:
            raise Exception('Path to config not specified in object constructor or path does not exist')

        self.connections = ConfigParser.ConfigParser()
        self.connections.read(self.configPath)

        if dbName != None:
            self.dbName = dbName
        else:
            raise Exception('Expected constructor parameter to be connection name.')

    def connection(self):

        if self.conn != None:
            return

        try:
            self.conn = MySQLdb.connect(
                host = self.connections.get(self.dbName, 'host'),
                port = self.connections.getint(self.dbName, 'port'),
                user = self.connections.get(self.dbName, 'user'),
                passwd = self.connections.get(self.dbName, 'password'),
                db = self.connections.get(self.dbName, 'dbname'),
                charset = self.charset
            )
        except MySQLdb.Error, e:
            raise Exception('There was a problem with connection to the database: ' + str(e))

    def fetchFirst(self, query, **opts):       
        # Check/create the connection
        self.connection()

        # Default options
        optsDefaults = {
            'returnDict': True
        }

        opts = dict(optsDefaults.items() + opts.items())

        if opts['returnDict'] == True:
            cur = self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        else:
            cur = self.conn.cursor()

        t0 = time.time()
        cur.execute(query)
        t1 = time.time() - t0

        self.setInfo(cur, time=t1)

        row = cur.fetchone()

        cur.close()

        return row

    def fetchAll(self, query, **opts):

        # Check/create the connection
        self.connection()

        # Default options
        optsDefaults = {
            'returnDict': True
        }
        opts = dict(optsDefaults.items() + opts.items())

        if opts['returnDict'] == True:
            cur = self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        else:
            cur = self.conn.cursor()

        t0 = time.time()
        cur.execute(query)
        t1 = time.time() - t0

        self.setInfo(cur, time=t1)

        rows = cur.fetchall()

        cur.close()

        return rows

    def execute(self, query, data=None, opts=None):

        # Default options
        optsDefaults = {
            'returnSQL': False
        }

        if opts:
            opts = dict(optsDefaults.items() + opts.items())
        else:
            opts = optsDefaults

        # Check/create the connection
        self.connection()
        cur = self.conn.cursor()

        if data and query:

            replaceData = []

            # Find columns to fillout in SQL statement
            p = re.compile('\[(.+?)\]')
            cols = p.findall(query)

            for col in cols:

                try:
                    val = data[col]
                except KeyError, e:
                    raise Exception('Missing data for referenced column "' + col + '"')

                query = query.replace('[' + col + ']', '`' + col + '` = %s')

                replaceData.append(val)
            #            pdb.set_trace()
            # Execute SQL
            if opts['returnSQL'] == True:
                return query % tuple(replaceData)
            else:
                t0 = time.time()
                cur.execute(query, tuple(replaceData))
                t1 = time.time() - t0

                self.setInfo(cur, time=t1)
        elif query:
            # Execute passed raw SQL
            if opts['returnSQL'] == True:
                return query
            else:
                t0 = time.time()
                cur.execute(query)

                t1 = time.time() - t0

                self.setInfo(cur, time=t1)

            cur.close()

        else:
            raise Exception('Expecting 1st parameter to be SQL query.')

    def setInfo(self, cur, **opts):

        self.lastInsertId = cur.lastrowid
        self.info['executed'].append(
            {
                'query': cur._last_executed,
                'lastInsertId': cur.lastrowid,
                'warnings': cur._warnings,
                'executionTime': opts['time']
            }
        )
        self.info['connStats'] = self.conn.stat()
        self.info['lastInsertId'] = cur.lastrowid

        totalTime = 0
        for executed in self.info['executed']:
            totalTime += executed['executionTime']

        self.info['totalExecutionTime'] = totalTime
        
    def __del__(self):
        pass
        #self.close()
