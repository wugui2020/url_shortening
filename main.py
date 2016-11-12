import MySQLdb
from warnings import filterwarnings

BASE = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' # base62 alphabet
DATABASE_NAME = 'URL' # default database name
TABLE_NAME = 'URL_TABLE' # default table name
LENGTH_LIMIT = 1000 # url length limit
ID_SIZE = 10 # id int size
MAXIMUM_AGE_OF_URL = - 365 * 10 # maximum days for a url to live in database
PREFIX = "https://example.com/" # prefix for your short url

filterwarnings('ignore', category = MySQLdb.Warning) # To get rid of annoying warnings 

class Request():
    
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
        self._db_validate()
        self._clear_old_urls()
        self.result = self._handler(string, url)

    def _handler(self, string, url):
        if string != None:
            id = self.id_decoder(string)
            return self._db_retrieve(id)
        elif url != None:
            self._db_insert(url)
            return PREFIX + self.id_encoder(self.db.insert_id())
        else:
            raise

    def _clear_old_urls(self):
        """
        Remove expired entries.
        """
        self.cursor.execute(
                "\
                DELETE FROM {0} \
                WHERE Date < DATE_SUB(NOW(), INTERVAL {1} DAY) \
                ".format(TABLE_NAME, MAXIMUM_AGE_OF_URL))

    
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

    def _db_validate(self):
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
                        Date timestamp \
                        )".format(TABLE_NAME, str(ID_SIZE), str(LENGTH_LIMIT))
                )
        for query in queries:
            self.cursor.execute(query)
        return 

    
    def _db_insert(self, url):
        """
        Insert an entry into the database and return the id for shortening.
        Input: String
        Output: Int
        """
        s = "INSERT INTO {0} (url, date) VALUES ('{1}', NOW())".format(TABLE_NAME, url)
        self.cursor.execute(s)
        return self.db.insert_id()


    def _db_retrieve(self, id):
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
        return ret[0] if ret else "No Such Url"


if __name__== '__main__':
    print Request('wentaolu', url = "This is a test").result
    print Request('wentaolu', string = 'c').result

