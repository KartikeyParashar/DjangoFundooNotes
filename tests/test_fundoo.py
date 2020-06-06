import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()

# ****************************************TEST CASES FOR NOTE*******************************************************


class TestCasesForCreateNote:

    def test__title_note_given(self):
        ENDPOINT = 'note/create/'
        url = os.getenv('BASE_URL') + ENDPOINT
        data = {"title": "Test Case for Create Note",
                "note": "pytest has support for running Python unittest.py style tests"}
        headers = {'Content-Type': 'application/json'}
        response_ = requests.post(url, data=json.dumps(data), headers=headers)
        assert response_.status_code == 201

    def test__note_not_given(self):
        ENDPOINT = 'note/create/'
        url = os.getenv('BASE_URL') + ENDPOINT
        data = {"title": "Test Case for Create Note"}
        headers = {'Content-Type': 'application/json'}
        response_ = requests.post(url, data=json.dumps(data), headers=headers)
        assert response_.status_code == 201


class TestCaseForGetNote:

    def test_for_get_note(self):
        ENDPOINT = 'note/get/'
        url = os.getenv('BASE_URL') + ENDPOINT
        headers = {'Content-Type': 'application/json'}
        response_ = requests.get(url, headers=headers)
        assert response_.status_code == 200


class TestCaseForGetNoteWithID:

    def test_for_get_note_with_id(self):
        ENDPOINT = 'note/get/1/'
        url = os.getenv('BASE_URL') + ENDPOINT
        headers = {'Content-Type': 'application/json'}
        response_ = requests.get(url, headers=headers)
        assert response_.status_code == 200


class TestCaseForUpdateNoteWithID:

    # def test_for_update_note_with_id(self):
    #     ENDPOINT = 'note/update/50/'
    #     url = os.getenv('BASE_URL') + ENDPOINT
    #     data = {"title": "How prepared is India to tackle a possible COVID-19 outbreak?",
    #             "note": "The Indian government has set up coronavirus screening at airports "
    #                     "as soon as the news of the outbreak in China came out. And people "
    #                     "from China or who have travel history with China were banned from "
    #                     "entering into India. In some cases, they were sent back. "
    #                     "And Indians were stopped from going to China. If anyone has symptoms, "
    #                     "they were quarantined and were treated in isolation. In this way, "
    #                     "India could effectively prevent the COVID-19 for a much longer time "
    #                     "than most of the developed countries."}
    #     headers = {'Content-Type': 'application/json'}
    #     response_ = requests.put(url, data=json.dumps(data), headers=headers)
    #     assert response_.status_code == 202

    def test_for_update_note_with_id_note_not_given(self):
        ENDPOINT = 'note/update/3/'
        url = os.getenv('BASE_URL') + ENDPOINT
        data = {"title": "How prepared is India to tackle a possible COVID-19 outbreak?"}
        headers = {'Content-Type': 'application/json'}
        response_ = requests.put(url, data=json.dumps(data), headers=headers)
        assert response_.status_code == 400


# class TestCaseForDeleteNoteWithID:
#
    # def test_for_delete_note_with_id(self):
    #     ENDPOINT = 'note/delete/47/'
    #     url = os.getenv('BASE_URL') + ENDPOINT
    #     headers = {'Content-Type': 'application/json'}
    #     response_ = requests.delete(url, headers=headers)
    #     assert response_.status_code == 204

# *********************************************TEST CASES FOR LABELS************************************************


# class TestCasesForCreateLabel:
#
    # def test__name_given(self):
    #     ENDPOINT = 'label/create/'
    #     url = os.getenv('BASE_URL') + ENDPOINT
    #     data = {"name": "Test Case for Create Label"}
    #     headers = {'Content-Type': 'application/json'}
    #     response_ = requests.post(url, data=json.dumps(data), headers=headers)
    #     assert response_.status_code == 201


class TestCaseForGetLabel:

    def test_for_get_label(self):
        ENDPOINT = 'label/get/'
        url = os.getenv('BASE_URL') + ENDPOINT
        headers = {'Content-Type': 'application/json'}
        response_ = requests.get(url, headers=headers)
        assert response_.status_code == 200


class TestCaseForGetLabelWithID:

    def test_for_get_label_with_id(self):
        ENDPOINT = 'label/get/1/'
        url = os.getenv('BASE_URL') + ENDPOINT
        headers = {'Content-Type': 'application/json'}
        response_ = requests.get(url, headers=headers)
        assert response_.status_code == 200


# class TestCaseForUpdateLabelWithID:
#
    # def test_for_update_label_with_id(self):
    #     ENDPOINT = 'label/update/12/'
    #     url = os.getenv('BASE_URL') + ENDPOINT
    #     data = {"name": "Sports in INDIA"}
    #     headers = {'Content-Type': 'application/json'}
    #     response_ = requests.put(url, data=json.dumps(data), headers=headers)
    #     assert response_.status_code == 202


# class TestCaseForDeleteLabelWithID:
#
    # def test_for_delete_label_with_id(self):
    #     ENDPOINT = 'label/delete/15/'
    #     url = os.getenv('BASE_URL') + ENDPOINT
    #     headers = {'Content-Type': 'application/json'}
    #     response_ = requests.delete(url, headers=headers)
    #     assert response_.status_code == 204
