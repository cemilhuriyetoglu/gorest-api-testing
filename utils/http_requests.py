import requests
import config

BASE_URL = config.BASE_URL
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Bearer ' + config.auth_token
}


def get(endpoint):
    response = requests.get(BASE_URL + endpoint, headers=headers)
    return response


def post(endpoint, reqBody):
    response = requests.post(BASE_URL + endpoint, json=reqBody, headers=headers)
    return response


def put(endpoint, reqBody):
    response = requests.put(BASE_URL + endpoint, json=reqBody, headers=headers)
    return response


def delete(endpoint):
    response = requests.delete(BASE_URL + endpoint, headers=headers)
    return response
