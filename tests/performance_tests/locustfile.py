from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    def home(self):
        self.client.get("/")

    @task
    def login(self):
        self.client.post('/showSummary', data={"email": "admin@irontemple.com"})

    @task
    def get_in_competition(self):
        self.client.get('book/Spring Festival 2022/Iron Temple')

    @task
    def purchase_places(self):
        self.client.post('/purchasePlaces', data={"club": "Iron Temple", "competition": "Spring Festival 2022",
                                                  "places": 1})

    @task
    def logout(self):
        self.client.get('/logout')

