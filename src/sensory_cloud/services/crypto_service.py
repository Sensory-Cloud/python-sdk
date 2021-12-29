import secrets


class CryptoService:
    _allowable_characters: str = (
        "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    )

    def get_secure_random_string(self, length: int) -> str:
        return "".join(
            secrets.choice(self._allowable_characters) for i in range(length)
        )
