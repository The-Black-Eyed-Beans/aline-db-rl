import requests
import request
import generate
import re
import os
import logging
from faker import Faker
from faker.providers import internet, ssn, person, date_time
from random import randint, randrange
from datetime import date
import time
from dotenv import load_dotenv


def applications_to_users(user_amount, transaction_amount, bearer):
    
    for request_id in range(user_amount) :

        applicant_json = generate.applicant()

        applicant = request.post_entity(applicant_json, bearer, os.getenv('UNDERWRITER_HOST'), '/applicants') #applicant creation request

        if not applicant: #applicant could not be created.
            logging.error(f"Applicant request block {request_id} has failed.")
            continue

        
        application_json = generate.application(applicant.json()['id']) #id extracted from previous response from microservice.

        application = request.post_entity(application_json, bearer, os.getenv('UNDERWRITER_HOST'), '/applications') #application creation request

        try:
            user_json = generate.user(
                first_name=applicant_json["firstName"],
                last_name=applicant_json['lastName'],
                email=applicant_json['email'],
                phone=applicant_json['phone'],
                membership_id=application.json()['createdMembers'][0]['membershipId'],
                ssn=applicant_json["socialSecurity"]
            )
        except:
            print(f"application status code: {application.status_code}\ncontent: {application.content}\n\n\n")
            exit()

        user = request.post_entity(user_json, bearer, os.getenv('USER_HOST'), '/users/registration')

        for _ in range(transaction_amount) :

            transaction_json = generate.transaction(application.json()['createdAccounts'][0]['accountNumber'])

            transaction = request.post_entity(transaction_json, bearer, os.getenv('TRANSACTION_HOST'), '/transactions')
    
    return

def banks_and_branches(amount, bearer):

    for _ in range(amount):

        bank_json = generate.bank()

        bank = request.post_entity(bank_json, bearer, os.getenv('BANK_HOST'), '/banks')

        branch_json = generate.branch(bank_json, bank.json()['id'])    

        branch = request.post_entity(branch_json, bearer, os.getenv('BANK_HOST'), '/branches')

    return

