import unittest
import typing

from sensory_cloud.services.crypto_service import CryptoService


class CryptoServiceTest(unittest.TestCase):
    def test_get_secure_random_string(self):
        test_num: int = 100
        random_strings: typing.List[str] = []

        for i in range(test_num):
            random_string: str = CryptoService().get_secure_random_string(
                length=test_num + 1
            )
            self.assertEqual(len(random_string), test_num + 1)
            random_strings.append(random_string)

        self.assertEqual(len(random_strings), test_num)


if __name__ == "__main__":
    unittest.main()
