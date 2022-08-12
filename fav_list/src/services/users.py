import os
import requests as r
import json


class UserService:
    def __init__(self, url=None):
        self.http_api_url = os.environ['USERS_HTTP_API_URL']
    
    def sign_up(self, first_name, last_name, email, password):
        body = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password
        }
        headers = {
            "content-type": "application/json"
        }
        url = self.http_api_url + "/sign_up"
        data = json.dumps(body)
        print("THIS is the HTTP API")
        response = r.post(url=url, data=data, headers=headers)
        return response
