from server import app
from unittest import TestCase
import unittest
from model import connect_to_db, db, User, ProfilePage, Image, Note, Vote, Question, Comment

class CampBuddyTest(unittest.TestCase):
    """Tests for the routes"""
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        # Connect to the database
        connect_to_db(app)


    def test_home_page(self):
        '''Checking the root route'''
        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)

    def test_login(self):
        """Check user login"""
        result = self.client.get('/login',
                            data={"email":"cutekitty@gmail.com", "password":"123"},
                            follow_redirects=True)
        self.assertIn("Email", result.data)





    if __name__ == "__main__":
    unittest.main()