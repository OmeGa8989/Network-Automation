import requests
import json

class ApiClient:
    def __init__(self, base_url, timeout=10):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.token = None
        self.session = requests.Session()

    def register(self, endpoint, username, password):
        url = f"{self.base_url}{endpoint}"
        payload = {"username": username, "password": password}
        try:
            response = self.session.post(url, json=payload, timeout=self.timeout)
            # 200 or 201 are acceptable for registration
            if response.status_code in [200, 201]:
                print(f"Registration successful for user: {username}")
                return True
            else:
                print(f"Registration failed: {response.text}")
                return False
        except requests.RequestException as e:
            print(f"Registration error: {e}")
            return False

    def login(self, endpoint, username, password):
        url = f"{self.base_url}{endpoint}"
        # Task specified Basic Auth for login, but let's check payload format in task description
        # "Auth Type: Basic Auth (use your registered username/password)"
        # But payload example shows just token response. 
        # Usually Basic auth is header.
        try:
            response = self.session.post(url, auth=(username, password), timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("token")
                if self.token:
                    print("Login successful. Token received.")
                    self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                    return True
            print(f"Login failed at {url}: {response.status_code} {response.text}")
            return False
        except requests.RequestException as e:
            print(f"Login error at {url}: {e}")
            return False

    def get(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"GET Request failed: {e}")
            return None

    def put(self, endpoint, payload):
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.put(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"PUT Request failed: {e}")
            return None
