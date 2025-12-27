import requests

class APIClient:
    session = requests.Session()
    BASE_URL = "http://localhost:8000"

    @classmethod
    def get(cls, path):
        return cls.session.get(cls.BASE_URL + path)

    @classmethod
    def post(cls, path, json=None):
        return cls.session.post(cls.BASE_URL + path, json=json)

    @classmethod
    def put(cls, path, json=None):
        return cls.session.put(cls.BASE_URL + path, json=json)

    @classmethod
    def delete(cls, path):
        return cls.session.delete(cls.BASE_URL + path)
