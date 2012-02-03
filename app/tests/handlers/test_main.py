from env_setup import setup_tests; setup_tests()

from agar.test import BaseTest, WebTest

import main

class MainTest(BaseTest, WebTest):

    APPLICATION = main.application

    def test_hello_world(self):
        response = self.get("/")
        self.assertOK(response)
