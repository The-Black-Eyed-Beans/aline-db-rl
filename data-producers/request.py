import requests
import re
import os
import logging
from faker import Faker
from faker.providers import internet, ssn, person, date_time
from random import randint, randrange
from datetime import date
import time
from dotenv import load_dotenv

'''
    Uses login credentials to send login request to user microservice. If successful, returns bearer token in the form of a formatted dictionary defined
    by the 'requests' python module. 
'''
def login(username, password, user_host):
    logging.info(f"attempting login to application using admin credentials.. ")

    if username is None:
        logging.warning(f"username not found. Please check environment.")
        return 0
    if password is None:
        logging.warning(f"password not found. Please check environment.")
        return 0
    if user_host is None:
        logging.warning(f"user host not found. Please check environment.")
        return 0
    
    login_json = {
        "username":username ,
        "password":password
    } 

    logging.debug(f"Sending request to server...")
    login = requests.post(user_host , json=login_json)

    if login.status_code in range(200, 300):
        logging.info("Login successful.")
        logging.info(f"STATUS CODE: {login.status_code} ({login.reason})")
    elif login.status_code in range(300, 400):
        logging.warning("Login unsuccessful.")
        logging.error(f"CLIENT ERROR CODE {login.status_code} ({login.reason})")
        return 0
    elif login.status_code in range(400, 500):
        logging.warning("Login unsuccessful.")
        logging.error(f"SERVER ERROR CODE {login.status_code} ({login.reason})")
        return 0
    else:
        logging.info(f"STATUS CODE: {login.status_code} ({login.reason})")
    
    return login

'''Sends POST request to respective microservice with entity json to populate database.'''
def post_entity(json, headers, host, route):
    logging.debug(f"attempting to send POST request to {host+route}...")

    if not host:
        logging.warning("host was not found. Please check environment.")
        return 0
    
    logging.debug("Sending request to server...")

    response = requests.post(host+route, json=json, headers=headers)

    if response.status_code in range(200, 300):
        logging.debug(f"STATUS CODE: {response.status_code} ({response.reason})")
    elif response.status_code in range(300, 400):
        logging.error(f"CLIENT ERROR CODE {response.status_code} ({response.reason})")
        return 0
    elif response.status_code in range(400, 500):
        logging.error(f"SERVER ERROR CODE {response.status_code} ({response.reason})")
        return 0
    else:
        logging.info(f"STATUS CODE: {response.status_code} ({response.reason})")

    return response

''' Sends request to underwriter microservice with applicant json to create a new applicant.'''
def add_applicant(applicant_json, bearer, underwriter_host):
    logging.debug(f"attempting to send applicant request..")

    if underwriter_host is None:
        logging.warning(f"underwriter host was not found. Please check environment.")
        return 0
    
    logging.debug("Sending request to server...")

    response = requests.post(underwriter_host, json=applicant_json, headers=bearer)

    if response.status_code in range(200, 300):
        logging.debug(f"STATUS CODE: {response.status_code} ({response.reason})")
    elif response.status_code in range(300, 400):
        logging.error(f"CLIENT ERROR CODE {response.status_code} ({response.reason})")
        return 0
    elif response.status_code in range(400, 500):
        logging.error(f"SERVER ERROR CODE {response.status_code} ({response.reason})")
        return 0
    else:
        logging.info(f"STATUS CODE: {response.status_code} ({response.reason})")

    return 1

    
''' Sends request to user microservice with user json to create a new user.'''
def add_user(user_json, bearer, user_host):
    logging.debug("attempting to send user request...")

    if user_host is None:
        logging.warning(f"user host was not found. Please check environment.")
        return 0
    
    logging.debug("Sending request to server...")

    response = requests.post(user_host, json=user_json, headers=bearer)

    if response.status_code in range(200, 300):
        logging.debug(f"STATUS CODE: {response.status_code} ({response.reason})")
    elif response.status_code in range(300, 400):
        logging.error(f"CLIENT ERROR CODE {response.status_code} ({response.reason})")
        return 0
    elif response.status_code in range(400, 500):
        logging.error(f"SERVER ERROR CODE {response.status_code} ({response.reason})")
        return 0
    else:
        logging.info(f"STATUS CODE: {response.status_code} ({response.reason})")

    return 1

''' Sends request to transaction microservice with transaction json to create a new transaction.'''
def add_transaction(transaction_json, bearer, transaction_host):
    logging.debug("attempting to send transaction request...")

    if transaction_host is None:
        logging.warning(f"transaction host was not found. Plesae check environment.")
        return 0
    
    logging.debug("Sending request to server...")

    response = requests.post(transaction_host, json=transaction_json, headers=bearer)

    if response.status_code in range(200, 300):
        logging.debug(f"STATUS CODE: {response.status_code} ({response.reason})")
    elif response.status_code in range(300, 400):
        logging.error(f"CLIENT ERROR CODE {response.status_code} ({response.reason})")
        return 0
    elif response.status_code in range(400, 500):
        logging.error(f"SERVER ERROR CODE {response.status_code} ({response.reason})")
        return 0
    else:
        logging.info(f"STATUS CODE: {response.status_code} ({response.reason})")

    return 1

'''Sends request to bank microservice with bank json to create a new bank.'''
def add_bank():
    pass
