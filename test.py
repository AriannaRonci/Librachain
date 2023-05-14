import unittest

from faker import Faker
from dal.user_repository import UserRepository

class testLibra (unittest.TestCase):
    faker = Faker()

    def test_private_key_encryption(self):
        user_repo = UserRepository()
        username = self.faker.user_name()
        password = self.faker.password()
        public_key = "clear_public_key"
        private_key = "clear_private_key"
        user_repo.register_user(
            username,
            password,
            public_key,
            private_key
        )
        user = user_repo.get_user_by_username(username)
        self.assertIsNotNone(user)
        if user is not None:
            encrypted_private_key = user.get_private_key()
            decrypted_private_key = user_repo.decrypt_private_key(encrypted_private_key, password)
            self.assertEqual(private_key, decrypted_private_key)
        else:
            print("Error: user not registered")

if __name__ == '__main__':
    unittest.main()
