import pymysql

class Database:
    def __init__(self, host, user, password, database, charset='utf8'):
        self.db = pymysql.connect(host=host, user=user, password=password, database=database, charset=charset)
        self.cursor = self.db.cursor()
