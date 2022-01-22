from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker

class TestSetup(APITestCase):
    """
    Using Faker module to auto generate names
    """

    def setUp(self):
        self.register = reverse('register')
        self.login = reverse('login')
        self.fake = Faker()

        self.user_data = {
          "email": self.fake.email(),
          "username": self.fake.name(),
          "password": self.fake.email(),
        }
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()