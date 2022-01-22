from multiprocessing.connection import Client
from .test_setup import TestSetup
from rest_framework import status
from django.test import client
from ..models import CustomUser


'''
using import pdb pdb.set_trace() method creates a breaking point for you to inspect the data and know
what to test for. For instance if response.data is same to the data defined. useful tool to know 
the status code by just doing response.status_code

'''

class TestViews(TestSetup):

    def test_registration_with_no_data(self):
      res  = self.client.post(self.register)
      self.assertAlmostEqual(res.status_code, 400)


    def test_registration_with_data(self):
        res = self.client.post(self.register, self.user_data)
        self.assertEqual(res.data['email'], self.user_data['email'])
        self.assertEqual(res.data['username'], self.user_data['username'])
        self.assertEqual(res.status_code, 201)

    def test_login_with_unverified_email(self):
       res = self.client.post(self.login, self.user_data)
       self.assertEqual(res.status_code, 401)

    def test_login_with_verified_email(self):
       response = self.client.post(self.register, self.user_data, format='json')
       user = CustomUser.objects.get(email=response.data['email'])
       user.is_verified = True
       user.save()
       res = self.client.post(self.login, self.user_data, format="json")
       self.assertEqual(res.status_code, 200)
       
      
