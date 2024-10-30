from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import os

class BlindSignatureHelper:
    def __init__(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()

    def blind_message(self, message):
        blinding_factor = os.urandom(32)
        blinded_message = int.from_bytes(message, byteorder='big') * int.from_bytes(blinding_factor, byteorder='big')
        blinded_message = blinded_message.to_bytes((blinded_message.bit_length() + 7) // 8, byteorder='big')
        return blinded_message, blinding_factor

    def sign_message(self, blinded_message):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(blinded_message)
        hash_value = digest.finalize()
        
        return self.private_key.sign(
            hash_value,
            padding.PKCS1v15(),
            hashes.SHA256()
        )

    def unblind_signature(self, blinded_signature, blinding_factor):
        signature_int = int.from_bytes(blinded_signature, byteorder='big')
        unblinded_signature = signature_int // int.from_bytes(blinding_factor, byteorder='big')
        return unblinded_signature.to_bytes((unblinded_signature.bit_length() + 7) // 8, byteorder='big')
