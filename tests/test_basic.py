import unittest
from flask import cuttent_app
from app import create+app,db


class BasicsTestCase(unittest.TestCase):
    def setup(self):
        self.app=create_app('testing')
        self.app_context=self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def testappExists(self):
        self.assertFalse(current_app is None)

    def testapp_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])


class UserModelTestCase(unittest.TestCase):
    def test_password(self):
        u=User(password='zhulunchen111')
        self.asserTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u=User(password='zhulunchen111')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u=User(password='zhulunchen111')
        self.assertTrue(u.verify_password('zhulunchen111'))
        self.assertFalse(u.verify_password('fuck'))

    def test_password_salts_are_random(self):
        u=User(password='zhulunchen111')
        u2=User(password='zhulunchen111')
        self.assertTrue(u.password_hash!=u2.password_hash)




