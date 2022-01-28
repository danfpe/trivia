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
        self.database_name = "triviadb_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            "caryn1", "student",'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {"question": "who is the funniest person",
                            "answer": "hello world","difficulty": 3,
                            "category": 4}

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

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])
    
    def test_404_categories(self):
        res = self.client().get("/categories/100")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not found")
        self.assertEqual(data["error"], 404)

    def test_delete_question(self):
        res = self.client().delete("/questions/4")
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
    
    def test_422_if_question_does_not_exist(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
    
    def test_add_questions(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_422_add_question(self):
        bad_question = {"question": "hello wold", "answer": "hello world",
                        "difficulty": 10, "category": 19}
        res = self.client().post("/questions", json=bad_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["message"], "unprocessable")
        self.assertEqual(data["error"], 422)
        self.assertEqual(data["success"], False)
    
    def test_search_question_with_result(self):
        search_term = {"searchTerm": "Who invented Peanut Butter?"}
        res = self.client().post("/questions/search", json=search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["total_questions"], 1)
        self.assertTrue(data["questions"])
    
    def test_search_question_without_result(self):
        search_term = {"searchTerm": "10000m"}
        res = self.client().post("/questions/search", json=search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['total_questions'], 0)
        self.assertFalse(data['questions'])
    
    def test_get_question_from_category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(data["success"], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"])

    def test_404_get_question_from_category(self):
        res = self.client().get("/categories/20/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Not found")
        self.assertEqual(data["error"], 404)

    def test_quizzes(self):
        next_question = {'quiz_category': {"type": "Science", "id": 1},
                         "previous_questions":["1"]}
        res = self.client().post("/quizzes", json=next_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["question"])
    
    def test_422_test_quizze(self):
        question = {'quiz_category': {"type": "Science", "id": 'plus'},
                         "previous_questions": ['1']}
        res = self.client().post("/quizzes", json=question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["message"], "unprocessable")
        self.assertEqual(data["error"], 422)
        self.assertFalse(data["success"])
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()