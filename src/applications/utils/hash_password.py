import bcrypt
class PasswordUtils:
    @staticmethod
    def hash_password(p:str) -> str:
        return bcrypt.hashpw(p.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def check_password(p:str, hashed:str) -> bool:
        return bcrypt.checkpw(p.encode('utf-8'), hashed.encode('utf-8'))
