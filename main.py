import MySQLdb
from warnings import filterwarnings
from datetime import date

BASE = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
DATABASE_NAME = 'URL'
TABLE_NAME = 'URL_TABLE'
LENGTH_LIMIT = 1000
ID_SIZE = 10

filterwarnings('ignore', category = MySQLdb.Warning) # To get rid of annoying warnings 

class Session():
    
    def __init__(self, user, passwd = None, string = None, url = None):
        """
        Session Initialization
        """
        if passwd:
            self.db = MySQLdb.connect(user = user, passwd = passwd)
        else:
            self.db = MySQLdb.connect(user = user)

        self.cursor = self.db.cursor()
        self.db.autocommit(True)
        self.db_validate()
        self.date = date.today()
        print self.handler(string, url)

    def handler(self, string, url):
        if string != None:
            id = self.id_decoder(string)
            return self.db_retrieve(id)
        elif url != None:
            self.db_insert(url)
            return self.id_encoder(self.db.insert_id())
        else:
            raise

    
    def id_encoder(self, num, base = BASE):
        """
        Take an number and return an shortened string representation.
        Input: Int
        Output: String
        """

        if not num:
            return BASE[0]

        ans = []
        length = len(base)

        while num:
            ans += base[num % length],
            num /= length

        return "".join(ans)

    def id_decoder(self, string, base = BASE):
        """
        Take an encoded string and reverse it back to the original number.
        Input: String
        Output: Int
        """

        ans = 0
        length = len(base)

        for i, char in enumerate(string):
            ans += base.index(char) * length ** i

        return ans

    def db_validate(self):
        """
        Create database url if it does not exist.
        Create table url_table if it does not exist.
        return Nothing
        """
        queries = (
                "CREATE DATABASE IF NOT EXISTS {0};".format(DATABASE_NAME),
                "USE {0}".format(DATABASE_NAME),
                "CREATE TABLE IF NOT EXISTS {0} \
                        ( \
                        id INT({1}) UNSIGNED AUTO_INCREMENT PRIMARY KEY, \
                        Url varchar({2}), \
                        Date date \
                        )".format(TABLE_NAME, str(ID_SIZE), str(LENGTH_LIMIT))
                )
        for query in queries:
            self.cursor.execute(query)
            self.db.commit()
        return 

    
    def db_insert(self, url):
        """
        Insert an entry into the database and return the id for shortening.
        Input: String
        Output: Int
        """
        s = "INSERT INTO {0} (url, date) VALUES ('{1}', '{2}')".format(TABLE_NAME, url, self.date.isoformat())
        self.cursor.execute(s)
        return self.db.insert_id()


    def db_retrieve(self, id):
        """
        Get the original url from the database with id.
        Input: Int
        Output: String
        """
        self.cursor.execute(
                " \
                SELECT url \
                FROM {0} \
                WHERE id = {1} \
                ".format(TABLE_NAME , str(id))
                )
        ret = self.cursor.fetchone()
        return ret[0] if ret else -1


if __name__== '__main__':
    Session('wentaolu', url = "This is a test")
    Session('wentaolu', string = 'c')

