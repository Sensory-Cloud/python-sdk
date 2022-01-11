import secrets


class CryptoService:
    """
    Class that handles cryptographic operations
    """

    _allowable_characters: str = (
        "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    )

    def get_secure_random_string(self, length: int) -> str:
        """
        Method that generates a cryptographically-random string

        Arguments:
            length: Integer denoting the length of the string that is returned

        Returns:
            A cryptographically-random string
        """

        return "".join(
            secrets.choice(self._allowable_characters) for i in range(length)
        )
