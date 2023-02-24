import unittest
from src.routes import app


class TestDepositCalculation(unittest.TestCase):
    def setUp(self) -> None:
        self.app = app.test_client()

    def test_methods_post(self):
        data = {"date": "31.01.2021",
                "periods": 7,
                "amount": 10000,
                "rate": 6}
        true_response = {
            "28.02.2021": 10100.25,
            "30.04.2021": 10201.5,
            "30.06.2021": 10303.77,
            "31.01.2021": 10050,
            "31.03.2021": 10150.75,
            "31.05.2021": 10252.51,
            "31.07.2021": 10355.29
        }
        response = self.app.post('/', json=data)
        status_code = response.status_code
        response = response.get_json()

        self.assertEqual(200, status_code)
        self.assertEqual(true_response, response)

    def test_methods_get(self):
        true_response = {"error": "No data"}
        response = self.app.get('/')
        status_code = response.status_code
        response = response.get_json()

        self.assertEqual(400, status_code)
        self.assertEqual(true_response, response)

    def test_error_date_and_rate(self):
        data = {"date": "31012021",
                "periods": 7,
                "amount": 10000,
                "rate": 0}
        true_response = {"error": "The following data contains errors:" \
                                  "\n\"Date\" must has format: dd.mm.yyyy" \
                                  "\n\"Rate\" must be between 1 and 8"}
        response = self.app.post('/', json=data)
        status_code = response.status_code
        response = response.get_json()

        self.assertEqual(400, status_code)
        self.assertEqual(true_response, response)

    def test_error_all_parametrs(self):
        data = {"date": "31012021",
                "periods": 70,
                "amount": 1000,
                "rate": 0}
        true_response = {"error": "The following data contains errors:" \
                                  "\n\"Date\" must has format: dd.mm.yyyy" \
                                  "\n\"Periods\" must be between 1 and 60" \
                                  "\n\"Amount\" must be between 10 000 and 3 000 000" \
                                  "\n\"Rate\" must be between 1 and 8"}
        response = self.app.post('/', json=data)
        status_code = response.status_code
        response = response.get_json()

        self.assertEqual(400, status_code)
        self.assertEqual(true_response, response)

    def test_empty_dict(self):
        data = {}
        true_response = {"error": "No following data:\nNo data"}

        response = self.app.post('/', json=data)
        status_code = response.status_code
        response = response.get_json()

        self.assertEqual(400, status_code)
        self.assertEqual(true_response, response)

    def test_no_date_and_amount(self):
        data = {"periods": 7,
                "rate": 6}
        true_response = {"error": "No following data:\ndate\namount"}

        response = self.app.post('/', json=data)
        status_code = response.status_code
        response = response.get_json()

        self.assertEqual(400, status_code)
        self.assertEqual(true_response, response)

    def test_not_correct_type(self):
        data = {"date": "Hello world",
                "periods": "Hello world",
                "amount": "Hello world",
                "rate": "Hello world"}
        true_response = {"error": "The following data contains errors:" \
                                  "\n\"Date\" must has format: dd.mm.yyyy" \
                                  "\n\"Periods\" must has type Integer and must be between 1 and 60" \
                                  "\n\"Amount\" must has type Integer and must be between 10 000 and 3 000 000" \
                                  "\n\"Rate\" must has type Float and must be between 1 and 8"}

        response = self.app.post('/', json=data)
        status_code = response.status_code
        response = response.get_json()

        self.assertEqual(400, status_code)
        self.assertEqual(true_response, response)
