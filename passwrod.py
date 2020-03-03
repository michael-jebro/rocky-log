from hashlib import pbkdf2_hmac

PASS_ERR_MESS = {
    'too_short': 'password must be 8 chars long',
    'not_str': 'password value must be a string'
}


SALT_ERR_MESS = {
    'too_short': 'salt is too short (min 30 characters)',
    'not_str': 'salt value must be a string'
}


class PasswrodError(Exception):
    pass

class PasswordError(PasswrodError):
    pass

class SaltError(PasswrodError):
    pass


class Passwrod:
    __slots__ = ['__passwrod', '__salt']

    def __init__(self, password, salt):
        self.__throw_errors_if_necessary(
            password,
            salt
        )

        self.__passwrod = password
        self.__salt = salt

    def the_same_as_(self, password_hash):
        original = self.__gen_hash_of_(self.__passwrod)
        target = password_hash
        return original == target

    def get_hash(self):
        hashed_item = self.__gen_hash_of_(self.__passwrod)
        return hashed_item

    def __gen_hash_of_(self, password):
        alg = 'sha256'
        iters = 1500
        pbkdf2_hash = pbkdf2_hmac(
            alg,
            password.encode('utf-32'),
            self.__salt.encode('utf-32'),
            iters
        )
        return pbkdf2_hash.hex()


    # TO FUCKING DO
    def __throw_errors_if_necessary(self, password, salt):
        if not isinstance(password, str):
            raise PasswordError(PASS_ERR_MESS['not_str'])

        if not isinstance(salt, str):
            raise SaltError(SALT_ERR_MESS['not_str'])

        if not len(password) >= 8:
            raise PasswordError(PASS_ERR_MESS['too_short'])

        if not len(salt) >= 30:
            raise PasswordError(SALT_ERR_MESS['too_short'])
