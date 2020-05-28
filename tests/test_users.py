import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()


class TestCasesForRegistration:

    def test_for_username_email_password_all_details_given(self):
        ENDPOINT = 'register/'
        url = os.getenv('BASE_URL') + ENDPOINT
        data = {"username": "kartikeyparashar96", "email": "kartikeyparashar96@gmail.com",
                "password": "kartikeyparashar96"}
        headers = {'Content-Type': 'application/json'}
        response_ = requests.post(url, data=json.dumps(data), headers=headers)
        assert response_.status_code == 201

    def test_for_email_password_given_username_not_given(self):
        ENDPOINT = 'register/'
        url = os.getenv('BASE_URL') + ENDPOINT
        data = {"email": "kartikeyparashar96@gmail.com",
                "password": "kartikeyparashar96"}
        headers = {'Content-Type': 'application/json'}
        response_ = requests.post(url, data=json.dumps(data), headers=headers)
        assert response_.status_code == 400

    def test_for_username_password_given_email_not_given(self):
        ENDPOINT = 'register/'
        url = os.getenv('BASE_URL') + ENDPOINT
        data = {"username": "kartikeyparashar96", "password": "kartikeyparashar96"}
        headers = {'Content-Type': 'application/json'}
        response_ = requests.post(url, data=json.dumps(data), headers=headers)
        assert response_.status_code == 400

    def test_for_username_email_given_password_not_given(self):
        ENDPOINT = 'register/'
        url = os.getenv('BASE_URL') + ENDPOINT
        data = {"username": "kartikeyparashar96", "email": "kartikeyparashar96@gmail.com"}
        headers = {'Content-Type': 'application/json'}
        response_ = requests.post(url, data=json.dumps(data), headers=headers)
        assert response_.status_code == 400

    def test_for_username_given_email_password_not_given(self):
        ENDPOINT = 'register/'
        url = os.getenv('BASE_URL') + ENDPOINT
        data = {"username": "kartikeyparashar96"}
        headers = {'Content-Type': 'application/json'}
        response_ = requests.post(url, data=json.dumps(data), headers=headers)
        assert response_.status_code == 400

    def test_for_email_given_username_password_not_given(self):
        ENDPOINT = 'register/'
        url = os.getenv('BASE_URL') + ENDPOINT
        data = {"email": "kartikeyparashar96@gmail.com"}
        headers = {'Content-Type': 'application/json'}
        response_ = requests.post(url, data=json.dumps(data), headers=headers)
        assert response_.status_code == 400

    def test_for_password_given_username_email_not_given(self):
        ENDPOINT = 'register/'
        url = os.getenv('BASE_URL') + ENDPOINT
        data = {"password": "kartikeyparashar96"}
        headers = {'Content-Type': 'application/json'}
        response_ = requests.post(url, data=json.dumps(data), headers=headers)
        assert response_.status_code == 201


class TestCasesForLogin:

    def test_for_username_password_all_details_given(self):
        ENDPOINT = 'login/'
        url = os.getenv('BASE_URL') + ENDPOINT
        data = {"username": "kartikeyparashar96", "password": "kartikeyparashar96"}
        headers = {'Content-Type': 'application/json'}
        response_ = requests.post(url, data=json.dumps(data), headers=headers)
        assert response_.status_code == 202

    def test_username_not_given(self):
        ENDPOINT = 'login/'
        url = os.getenv('BASE_URL') + ENDPOINT
        data = {'password': 'kartikeyparashar96'}
        headers = {'Content-Type': 'application/json'}
        response_ = requests.post(url, data=json.dumps(data), headers=headers)
        assert response_.status_code == 400

    def test_password_not_given(self):
        ENDPOINT = '/login/'
        url = os.getenv('BASE_URL') + ENDPOINT
        data = {'username': 'Akshaya'}
        headers = {'Content-Type': 'application/json'}
        response_ = requests.post(url, data=json.dumps(data), headers=headers)
        assert response_.status_code == 404


class TestCasesForResetPassword:

    def test_Username_Email_ID_given(self):
        ENDPOINT = 'reset_password/'
        url = os.getenv('BASE_URL') + ENDPOINT
        data = {'username': 'kartikeyparashar96', 'email': 'kartikeyparashar96@gmail.com'}
        headers = {'Content-Type': 'application/json'}
        response_ = requests.post(url, data=json.dumps(data), headers=headers)
        assert response_.status_code == 200

    def test_Email_ID_not_given(self):
        ENDPOINT = 'reset_password/'
        url = os.getenv('BASE_URL') + ENDPOINT
        data = {'username': 'kartikeyparashar96'}
        headers = {'Content-Type': 'application/json'}
        response_ = requests.post(url, data=json.dumps(data), headers=headers)
        assert response_.status_code == 500

    def test_Username_not_given(self):
        ENDPOINT = 'reset_password/'
        url = os.getenv('BASE_URL') + ENDPOINT
        data = {'email': 'kartikeyparashar96@gmail.com'}
        headers = {'Content-Type': 'application/json'}
        response_ = requests.post(url, data=json.dumps(data), headers=headers)
        assert response_.status_code == 500


class TestCasesForFORGOTPassword:

    def test_password_confirm_password_given(self):
        ENDPOINT = 'forgot_password/parasharkartikey/'
        url = os.getenv('BASE_URL') + ENDPOINT
        data = {'password': 'parasharkartikey', 'confirm_password': 'parasharkartikey'}
        headers = {'Content-Type': 'application/json'}
        response_ = requests.post(url, data=json.dumps(data), headers=headers)
        assert response_.status_code == 200

    def test_password_not_given(self):
        ENDPOINT = 'forgot_password/parasharkartikey/'
        url = os.getenv('BASE_URL') + ENDPOINT
        data = {'confirm_password': 'parasharkartikey'}
        headers = {'Content-Type': 'application/json'}
        response_ = requests.post(url, data=json.dumps(data), headers=headers)
        assert response_.status_code == 400

    def test_confirm_password_not_given(self):
        ENDPOINT = 'forgot_password/parasharkartikey/'
        url = os.getenv('BASE_URL') + ENDPOINT
        data = {'password': 'parasharkartikey'}
        headers = {'Content-Type': 'application/json'}
        response_ = requests.post(url, data=json.dumps(data), headers=headers)
        assert response_.status_code == 400
