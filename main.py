import MySQLdb
BASE = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    

class Session():
    
    def __init__(self, user, passwd = None, mode = 'Read', id = None, url = None):
        """
        Session Initialization
        """
        if passwd:
            self.db = MySQLdb.connect(user = user, passwd = passwd)
        else:
            self.db = MySQLdb.connect(user = user)

        self.cursor = self.db.cursor()
        self.db_validate()
    
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
        return self.cursor.execute(
                "CREATE DATABASE IF NOT EXISTS URL;"
                )

    
    def db_insert(self, url):
        """
        Insert an entry into the database and return the id for shortening.
        Input: String
        Output: Int
        """
        return 


    def db_retrieve(self, id):
        """
        Get the original url from the database with id.
        Input: Int
        Output: String
        """
        return


if __name__== '__main__':
    Session('wentaolu')
