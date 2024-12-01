import sys
import os

# Add the project root directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from fastapi.testclient import TestClient
from api import app


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_ask_question(self):
        response = self.client.post(
            "/ask",
            json={"url": "https://help.zluri.com", "question": "What is Zluri?"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("answer", data)
        self.assertIn("confidence", data)


if __name__ == "__main__":
    unittest.main()
