# test_integration.py
import unittest
from app import app, db, ToDo  # import your app, db, and models
from datetime import datetime


class ToDoIntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()  # Activar el contexto de la aplicación
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()  # Delete all 
        self.app_context.pop() 

    def add_sample_data(self):
        todo1 = ToDo(title='Test ToDo 1', description='', date_created=datetime(2024, 12, 5), is_completed=False)
        todo2 = ToDo(title='Test ToDo 2', description='', date_created=datetime(2024, 11, 6), is_completed=True)
        db.session.add(todo1)
        db.session.add(todo2)
        db.session.commit()


    def test_get_all_todos(self):
        self.add_sample_data()
        response = self.client.get('/todo')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test ToDo 1', response.data)
        self.assertIn(b'Test ToDo 2', response.data)

#    def test_complete_todo(self):
#        self.add_sample_data()
#        response = self.client.post('/todo/1/complete')
#        self.assertEqual(response.status_code, 200)
#        follow_response = self.client.get('/todo/1')
#        data = follow_response.get_json()
#        self.assertTrue(data['is_completed'])


    def test_delete_todo(self):
        self.add_sample_data()
        response = self.client.delete('/todo/1')
        self.assertEqual(response.status_code, 200)
        follow_response = self.client.get('/todo')
        self.assertNotIn(b'Test ToDo 1', follow_response.data)


# Add more integration tests as needed
