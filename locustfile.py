from locust import HttpUser, task, between

class MyLocustTesting(HttpUser):
    wait_time = between(0.5, 1)
    
    def on_start(self):
        return super().on_start()
    def on_stop(self):
        return super().on_stop()
    @task(1)
    def hello_world(self):
        url = "http://localhost:5000/"
        self.client.get(url + "extractbeacon"+ "?staff_id=1&start_time=0&end_time=999999999")
    @task(1)
    def hello_world2(self):
        url = "http://localhost:5000/"
        self.client.get(url)
        
