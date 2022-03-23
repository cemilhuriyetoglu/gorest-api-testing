# gorest-api-testing

Test Stack : Python3, Pytest, Requests Library, Allure Report

Test Cases Path: test_cases/test_cases.py

Allure Results Path: test-cases/allure-results. To create the allure report you should run the "allure serve ./test_cases/allure-results" command.

For creation unique email, the "email_iteration_number" stored under variables.py and the value of "email_iteration_number" is incremented by one each time a new user is created.

The id of the new user created is stored in variables.py
