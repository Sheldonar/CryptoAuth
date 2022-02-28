from http import server
import random
import string


class LastRandom (object):
    N = None
    server_password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    s_key_N = 20
    I = 0
