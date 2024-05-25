from locust import HttpUser, task, between, TaskSet
from requests.auth import HTTPBasicAuth


class UserBehavior(TaskSet):
    BASE_URL="api/v1/"
    def on_start(self):
        # Endpoint logowania
        login_url = f"{self.BASE_URL}users/login"
        # Dane logowania
        username = "Doe"
        password = "456"

        # Wysłanie żądania logowania z Basic Auth
        response = self.client.post(login_url, auth=HTTPBasicAuth(username, password))
        if response.status_code == 200:
            self.token = response.json().get("token")
        else:
            print("Login failed:", response.text)
            self.token = None

    @task(1)
    def users(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get(f"{self.BASE_URL}users", headers=headers)

    @task(1)
    def userInfo(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get(f"{self.BASE_URL}users/2", headers=headers)

    @task(1)
    def userCars(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get(f"{self.BASE_URL}users/2/cars", headers=headers)

    @task(1)
    def brands(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get(f"{self.BASE_URL}cars/brands", headers=headers)

    @task(1)
    def models(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get(f"{self.BASE_URL}cars/brands/models/3", headers=headers)

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)