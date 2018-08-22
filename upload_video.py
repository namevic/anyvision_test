import requests


def upload_file(path):
    files = {'file': open(path, 'rb')}

    requests.post('http://127.0.0.1:5000/', files=files)