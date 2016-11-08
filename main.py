import MySQLdb
BASE = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    

class Session():
    
    def __init__(self):
        """
        Session Initialization
        """
        user, passwd = self.getUserCredentials()
        self.db = MySQLdb.connect(user = user, passwd = passwd)

    
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

    def id_decoder(self, code, base = BASE):
        """
        Take an encoded string and reverse it back to the original number.
        Input: String
        Output: Int
        """

        ans = 0
        length = len(base)

        for i, char in enumerate(code):
            ans += base.index(char) * length ** i

        return ans


    


