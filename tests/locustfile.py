import json
import random

from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(0.01, 0.3)

    @task
    def hi(self):
        self.client.post("/api/v1/gateways/", data={"data": json.dumps({"test": str(random.randint(1, 100))})})

    @task
    def hello(self):
        self.client.post("/api/v1/gateways/", data={"data": json.dumps({"test": str(random.randint(1, 2))})})

    @task
    def chunk(self):
        for i in range(12):
            self.client.post("/api/v1/gateways/", data={"data": json.dumps({"test": str(i)})})
