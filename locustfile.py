import json

from django.urls import reverse
from locust import HttpUser, TaskSet, task


class UserBehavior(TaskSet):

    def on_start(self):
        self.login()

    def login(self):
        self.client.post("/user/login/", {"username": "parasharkartikey", "password": "parasharkartikey"})

    @task(2)
    def home(self):
        self.client.get("/")

    @task(1)
    def note_create(self):
        self.client.post("/note/create/", json.dumps({"title": "Locust", "note": "A note on Locust"}),
                         headers={"Content-Type": "application/json"})


class MyLocust(HttpUser):
    host = r"http://127.0.0.1:8000"
    tasks = [UserBehavior]
    min_wait = 5000
    max_wait = 15000
