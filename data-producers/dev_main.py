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

#TODO: randomize income.
#TODO: modify income to randomize.
#TODO: wrap request api calls with try/except.
#TODO: logs


''' retrieves admin credentials and microservice hosts from environment.'''
def retrieve_environment_variables():
    logging.info(f"retrieving information from environment...")

    return {
        "admin_username":os.getenv('ALINE_ADMIN_USERNAME'),
        "admin_password":os.getenv('ALINE_ADMIN_PASSWORD'),
        "user_host":os.getenv('USER_HOST'),
        "underwriter_host":os.getenv('UNDERWRITER_HOST'),
        "transaction_host":os.getenv('TRANSACTION_HOST'),
        "bank_host":os.getenv('BANK_HOST')
    }

if __name__ == '__main__' :

    #logging
    logging.basicConfig(filename = "logfile.log", filemode='w', format='[%(asctime)s][%(levelname)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    
    #retrieve admin credentials, and microservice hosts.
    environment = retrieve_environment_variables()
    
    #login to application using admin username and password.
    bearer =  request.login(environment["username"], environment["password"], environment["user_host"]) 
    
    if not bearer :  #if failure, log and exit the program.
        logging.error("Was not able to acquire bearer token. Exiting process.")
        quit()

    
    #start with applicant -> user production

    for request_id in range(50) :

        applicant_json = generate.applicant()

        applicant = request.post_entity(applicant_json, bearer, environment['underwriter_host'], '/applicants') #applicant creation request


        if applicant.status_code > 210 :
            print(f"applicant status code: {applicant.status_code}\ncontent: {applicant.content}\nwith id: {applicant.json()['id']}\n\n\n")
        
        application_json = generate.application(applicant.json()['id']) #id extracted from previous response from microservice.

        application = request.post_entity(application_json, bearer, environment['underwriter_host'], '/applications') #application creation request

        if application.status_code > 210 :
            print(f"application status code: {application.status_code}\ncontent: {application.content}\n\n\n")

        user_json = generate.user({
            'first_name':applicant_json["firstName"],
            'last_name':applicant_json['lastName'],
            'email':applicant_json['email'],
            'phone':applicant_json['phone'],
            'membership_id':application.json()['createMembers'][0]['membershipId'],
            'ssn':application_json["socialSecurity"]
        })

        user = request.post_entity(user_json, bearer, environment['user_host'], '/users/registration')

        if user.status_code > 210 :
            print(f"user status code: {user.status_code}\ncontent: {user.content}\nwith json:{user_json}\n\n\n")

        for _ in range(1) :

            transaction_json = generate.transaction(application.json()['createdAccounts'][0]['accountNumber'])

            transaction = request.post_entity(transaction_json, bearer, environment['transaction_host'], '/transactions')

            if transaction.status_code > 210:
                print(f"transaction status code: {transaction.status_code}\ncontent: {transaction.content}\nwith json:{transaction_json}")


    #create banks and branches

    for _ in range(10):

        bank_json = generate.bank()

        bank = request.post_entity(bank_json, bearer, environment['bank_host'], '/banks')

        if bank.status_code > 210 :
            print(f"bank status code: {bank.status_code}\ncontent: {bank.content}\n\n\n")

        branch_json = generate.branch(bank_json)    

        branch = request.post_entity(branch_json, bearer, environment['bank_host'], '/branches')

        if branch.status_code > 210 :
            print(f"branch status code: {branch.status_code}\ncontent: {branch.content}\n\n\n")
    
    
    