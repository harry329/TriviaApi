import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_All_Categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['categories']),6)

    def test_get_Questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 18)
        self.assertEqual(len(data['categories']), 6)

    def test_delete_Question(self):
        self.assertEqual(len(Question.query.all()),19)
        self.client().delete("/questions/23")
        self.assertEqual(len(Question.query.all()),18)

        
    def test_submit_question(self):
        res = self.client().post("/questions", json = {
            'question' : 'question',
            'answer' : 'answer',
            'category' : 1,
            'difficulty' : 1
        } )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)

    def test_search_questions(self):
        res = self.client().post("/questions/search", json = {
            'searchTerm' : 'auto'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['totalQuestions'], 1)

    def test_get_Question_For_Category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['totalQuestions'], 4)

    def test_404(self):
        res = self.client().get("/test")
        self.assertEqual(res.status_code, 404)
    
    def test_422(self):
        res = self.client().delete("/questions/123")
        self.assertEqual(res.status_code, 422)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
