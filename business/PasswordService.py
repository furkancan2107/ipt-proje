import hashlib

class PasswordService:
    @staticmethod
    def hash_password(password):
        hashed_bytes = hashlib.sha256(password.encode()).digest()
        hashed_password = hashed_bytes.hex()
        return hashed_password

    @staticmethod
    def verify_password(password, hashed_password):
        input_hashed_password = PasswordService.hash_password(password)
        return input_hashed_password == hashed_password