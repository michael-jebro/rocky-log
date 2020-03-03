'''

Super Secure Session Library 0.1
* used to create temporary login session uids for storing them in the client's cookies

tested on Python3.8

'''

import hashlib
import string
import random

class SessionContainer:
    class Controller(object):
        def __new__(cls):
            if not hasattr(cls, '__instance'):
                cls.__instance = super(SessionContainer.Controller, cls).__new__(cls)
            return cls.__instance

        def get_random_data(self):
            ascii_chars = string.ascii_letters + string.digits + string.punctuation
            random_data = ''.join(
                [random.SystemRandom().choice(ascii_chars) for _ in range(0, 30)]
            )
            return random_data

        def produce_uid(self):
            random_data = self.get_random_data()
            md5_hash = hashlib.md5(random_data.encode('utf-32'))
            return md5_hash.hexdigest()


    def __init__(self):
        self.session_dict = dict()
        self.__secret_dict = dict()
        self.controller = SessionContainer.Controller()

    #TO DO
    def add_session_returning_uid(self, username):
        uid = None
        is_inside = True

        while is_inside:
            uid = self.controller.produce_uid()
            if uid not in self.session_dict.keys():
                is_inside = False
        self.session_dict.update({ uid: username })
        return uid

    def remove_session(self, uid):
        self.session_dict.pop(uid)

    def is_active(self, uid):
        is_inside = uid in self.session_dict.keys()
        return is_inside

    def clear(self):
        self.session_dict.clear()
