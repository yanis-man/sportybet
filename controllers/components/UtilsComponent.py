import hashlib

class UtilsComponents:
    def __init__(self) -> None:
        self.HASH_SALT = b'b\xd0\xd9\x98&\xa2\x18E\xadv\x03d\x9e\xce\xe5\n\xb3N\xbbW\x95\xa7\xcbs>\xf1a\x10\xce\xdc\x83\x18'

    def hash_password(self, password):
        hashed_pswd = self.HASH_SALT + hashlib.pbkdf2_hmac(
        'sha256', # The hash digest algorithm for HMAC
        password.encode("utf-8"), # Convert the password to bytes
        self.HASH_SALT, # Provide the salt
        100000, # It is recommended to use at least 100,000 iterations of SHA-256 
        dklen=128
        )

        return str(hashed_pswd[32:])