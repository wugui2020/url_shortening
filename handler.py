import MySQLdb
from flask import redirect, request
from flask_restful import Resource
from warnings import filterwarnings
from hashlib import sha1

INITIAL_LENGTH = 5
MAX_ID_LENGTH = 7
BASE = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' # base62 alphabet
DATABASE_NAME = 'URL' # default database name
TABLE_NAME = 'URL_TABLE' # default table name
LENGTH_LIMIT = 1000 # url length limit
MAXIMUM_AGE_OF_URL = 365 * 10 # maximum days for a url to live in database
PREFIX = "https://example.com/" # prefix for your short url

filterwarnings('ignore', category = MySQLdb.Warning) # To get rid of annoying warnings 

class Handler(Resource):
    
    def __init__(self, string = None, url = None):
        """
        Session Initialization
        """
        with open('credentials.conf', 'r') as f:
            user = f.readline().strip()
            passwd = f.readline().strip()
        if passwd:
            self.db = MySQLdb.connect(user = user, passwd = passwd)
        else:
            self.db = MySQLdb.connect(user = user)

        self.cursor = self.db.cursor()
        self.db.autocommit(True)
        self._db_validate()

    def get(self, short_url):
        self._clear_old_urls()
        url = self._db_retrieve(short_url)
        return redirect(url) if url else None

    def post(self, short_url = None):
        url = request.form['data']
        self._clear_old_urls()
        if short_url and self.get(short_url) != data:
            return {'error':'The short_url has already been taken.'}
        elif not short_url:
            h = self.url_encode(int(sha1(url).hexdigest(), 16))
            short_url = h[:INITIAL_LENGTH]
            print short_url
            tmp_len = INITIAL_LENGTH
            while not self._db_insert(url, short_url):
                tmp_len += 1
                short_url = h[:tmp_len]
        return {'short_url': PREFIX + short_url,
                'data': url}

    def _clear_old_urls(self):
        """
        Remove expired entries.
        """
        self.cursor.execute(
                "\
                DELETE FROM {0} \
                WHERE Date < DATE_SUB(NOW(), INTERVAL {1} DAY) \
                ".format(TABLE_NAME, MAXIMUM_AGE_OF_URL))

    
    def url_encode(self, num, base = BASE):
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

    def url_decode(self, string, base = BASE): # outdated
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
                        id varchar({1}) UNIQUE, \
                        Url varchar({2}) UNIQUE, \
                        Date timestamp \
                        )".format(TABLE_NAME, MAX_ID_LENGTH, str(LENGTH_LIMIT))
                )
        for query in queries:
            self.cursor.execute(query)
        return 

    
    def _db_insert(self, url, short_url):
        """
        Insert an entry into the database and return the id for shortening.
        Input: String
        Output: Int
        """
        check = "SELECT id, url FROM {0} WHERE id = '{1}' OR url = '{2}'".format(TABLE_NAME, short_url, url)
        self.cursor.execute(check)
        ret = self.cursor.fetchone()
        if ret and ret[1] == url:
            return True
        else:
            try:
                s = "INSERT INTO {0} (id, url, date) VALUES ('{1}', '{2}', NOW())".format(TABLE_NAME, short_url, url)
                self.cursor.execute(s)
            except MySQLdb.IntegrityError as e:
                print e
                return False
        return True


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
                WHERE id = '{1}' \
                ".format(TABLE_NAME , str(id))
                )
        ret = self.cursor.fetchone()
        return ret[0] if ret else None

