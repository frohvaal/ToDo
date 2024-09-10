# test_app.py
import unittest
from app import app  # import your Flask app here

class ToDoTestCase(unittest.TestCase):
    def setUp(self):
        # Set up a test client
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_get_all_todos(self):
        response = self.client.get('/todo')
        self.assertEqual(response.status_code, 200)
        # additional assertions to verify the response content

#    def test_get_todo_by_id(self):
#        response = self.client.get('/todo/1')
#        self.assertEqual(response.status_code, 200)
#        data = response.get_json()
#        self.assertIn('id', data)
#        self.assertIn('title', data)
#        self.assertIn('description', data)
#        self.assertIn('date_created', data)
#        self.assertIn('is_completed', data)


#    def test_complete_todo(self):
#        response = self.client.post('/todo/1/complete')
#        self.assertEqual(response.status_code, 200)
#        follow_response = self.client.get('/todo/1')
#        data = follow_response.get_json()
#        self.assertTrue(data['is_completed'])



    def test_404_for_invalid_todo_id(self):
        response = self.client.get('/todo/9999')
        self.assertEqual(response.status_code, 404)

# add more tests for other routes and functionalities as needed
