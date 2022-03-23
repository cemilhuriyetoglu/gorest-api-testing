from utils.http_requests import get, post, put, delete
import variables
import pytest
import allure
import time

# ENDPOINTS
GET_URL = '/public-api/users'
POST_URL = '/public-api/users'
PUT_URL = '/public-api/users'
DELETE_URL = '/public-api/users'


class Tests:

    @allure.feature("Get Users")
    @allure.story("User can see users information")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_get_users(self):
        response = get(GET_URL)
        response_json = response.json()
        assert response.status_code == 200
        assert response_json['code'] == 200
        limit = response_json['meta']['pagination']['limit']
        assert len(response_json['data']) == limit

    @allure.feature("Get Users with wrong endpoint")
    @allure.story("User can not see users information with wrong endpoint")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_get_users_wrong_endpoint(self):
        wrong_endpoint = "/public-api/customers"
        response = get(wrong_endpoint)
        assert response.status_code == 404

    @allure.feature("Create a User")
    @allure.story("Authorized user can add users information")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_new_user(self):
        payload = {
            "name": "Cemil",
            "gender": "male",
            "email": "cemil" + str(variables.email_iteration_number) + "@test.com",
            "status": "active"
        }
        email_iteration_number = variables.email_iteration_number + 1
        response = post(POST_URL, payload)
        response_json = response.json()
        print(response_json)
        assert response.status_code == 200
        assert response_json['code'] == 201
        assert response_json['data']['name'] == "Cemil"
        assert response_json['data']['gender'] == "male"
        assert response_json['data']['email'] == "cemil" + str(variables.email_iteration_number) + "@test.com"
        assert response_json['data']['status'] == 'active'
        user_id = response_json['data']['id']
        with open("./variables.py", "w") as f:
            f.write(f"user_id = {user_id}\n")
            f.write(f"email_iteration_number = {email_iteration_number}\n")

    @allure.feature("Create already exist User")
    @allure.story("Authorized user can not add existing users information")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_already_existing_user(self):
        time.sleep(3)
        payload = {
            "name": "Cemil",
            "gender": "male",
            "email": "cemil" + str(variables.email_iteration_number - 1) + "@test.com",
            "status": "active"
        }
        response = post(POST_URL, payload)
        response_json = response.json()
        assert response.status_code == 200
        assert response_json['code'] == 422
        expected_failure_output = [{'field': 'email', 'message': 'has already been taken'}]
        assert response_json['data'] == expected_failure_output

    @allure.feature("Get Users with non exist id")
    @allure.story("Authorized user can not see non exist users information")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_get_user_with_non_existing_id(self):
        endpoint = GET_URL + "/" + "123abc"
        response = get(endpoint)
        response_json = response.json()
        expected_failure_output = {'code': 404, 'meta': None, 'data': {'message': 'Resource not found'}}
        assert response.status_code == 200
        assert response_json == expected_failure_output

    @allure.feature("Get Users with id")
    @allure.story("Authorized user can see users information")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_get_users_with_existing_id(self):
        endpoint = GET_URL + "/" + str(variables.user_id)
        response = get(endpoint)
        response_json = response.json()
        assert response.status_code == 200
        assert response_json['code'] == 200

    @allure.feature("Update a non exist User")
    @allure.story("Authorized user can not update non exist users information")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_update_non_exist_user(self):
        payload = {
            "name": "Cemil",
            "email": "cemil" + str(variables.email_iteration_number - 1) + "@test.com",
            "status": "inactive"
        }
        wrong_endpoint = PUT_URL + "/" + "123abc"
        response = put(wrong_endpoint, payload)
        response_json = response.json()
        expected_failure_output = {'code': 404, 'meta': None, 'data': {'message': 'Resource not found'}}
        assert response.status_code == 200
        assert response_json == expected_failure_output

    @allure.feature("Update a User")
    @allure.story("Authorized user can update users information")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_update_existing_user(self):
        payload = {
            "name": "Cemil",
            "gender": "male",
            "email": "cemil" + str(variables.email_iteration_number - 1) + "@test.com",
            "status": "inactive"
        }
        endpoint = PUT_URL + "/" + str(variables.user_id)
        response = put(endpoint, payload)
        response_json = response.json()
        print(response_json)
        assert response_json['data']['name'] == "Cemil"
        assert response_json['data']['gender'] == "male"
        assert response_json['data']['email'] == "cemil" + str(variables.email_iteration_number - 1) + "@test.com"
        assert response_json['data']['status'] == 'inactive'

    @allure.feature("Delete a User")
    @allure.story("Authorized user can delete users information")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_delete_existing_users(self):
        endpoint = DELETE_URL + "/" + str(variables.user_id)
        response = delete(endpoint)
        response_json = response.json()
        assert response.status_code == 200
        assert response_json['code'] == 204

    @allure.feature("Delete a non exist  User")
    @allure.story("Authorized user can not delete users information")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_delete_non_existing_users(self):
        endpoint = DELETE_URL + "/" + str(variables.user_id)
        response = delete(endpoint)
        response_json = response.json()
        expected_failure_output = {'code': 404, 'meta': None, 'data': {'message': 'Resource not found'}}
        assert response.status_code == 200
        assert response_json == expected_failure_output
