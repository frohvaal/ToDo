# test_integration.py
import unittest
from app import app, db, ToDo  # import your app, db, and models

class ToDoIntegrationTestCase(unittest.TestCase):
    def setUp(self):
        # Set up the test client and database
        app.config.from_object('config.TestingConfig')
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Tear down the database
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def add_sample_data(self):
        # Add sample data to the database for testing
        todo1 = ToDo(title='Test ToDo 1', completed=False)
        todo2 = ToDo(title='Test ToDo 2', completed=True)
        db.session.add(todo1)
        db.session.add(todo2)
        db.session.commit()

    def test_get_all_todos(self):
        self.add_sample_data()
        response = self.client.get('/todo')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test ToDo 1', response.data)
        self.assertIn(b'Test ToDo 2', response.data)

    def test_complete_todo(self):
        self.add_sample_data()
        response = self.client.post('/todo/1/complete')
        self.assertEqual(response.status_code, 302)
        follow_response = self.client.get('/todo/1')
        self.assertIn(b'completed', follow_response.data)

    def test_delete_todo(self):
        self.add_sample_data()
        response = self.client.delete('/todo/1/delete')
        self.assertEqual(response.status_code, 200)
        follow_response = self.client.get('/todo')
        self.assertNotIn(b'Test ToDo 1', follow_response.data)

    def test_todo_lifecycle(self):
        # Create a new To-Do
        response = self.client.post('/todos', data={'title': 'New To-Do'})
        self.assertEqual(response.status_code, 302)
        
        # Check if it was added
        response = self.client.get('/todos')
        self.assertIn(b'New To-Do', response.data)

        # Mark the To-Do as complete
        response = self.client.post('/todo/1/complete')
        self.assertEqual(response.status_code, 302)
        follow_response = self.client.get('/todo/1')
        self.assertIn(b'completed', follow_response.data)

        # Delete the To-Do
        response = self.client.delete('/todo/1/delete')
        self.assertEqual(response.status_code, 200)
        follow_response = self.client.get('/todo')
        self.assertNotIn(b'New To-Do', follow_response.data)

# Add more integration tests as needed
