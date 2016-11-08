BASE = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def id_encoder(num, base = BASE):

    if not num:
        return BASE[0]

    ans = []
    length = len(base)

    while num:
        ans += base[num % length],
        num /= length

    return "".join(ans)

def id_decoder(code, base = BASE):

    ans = 0
    length = len(base)

    for i, char in enumerate(code):
        ans += base.index(char) * length ** i

    return ans
    



