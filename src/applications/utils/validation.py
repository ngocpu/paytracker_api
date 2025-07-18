import random
class VerificationUtlils:
    @staticmethod
    def generate_verification_code():
        return random.randint(100000, 999999)