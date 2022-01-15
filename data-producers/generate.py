import requests
import request
import re
import os
import logging
from faker import Faker
from faker.providers import internet, ssn, person, date_time
from random import randint, randrange
from datetime import date
import time

fake = Faker()
password_regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$"

application_type = ["CHECKING", "SAVINGS", "CHECKING_AND_SAVINGS", "CREDIT_CARD", "LOAN"]
transaction_type = ["DEPOSIT","WITHDRAWAL","PURCHASE","PAYMENT","REFUND","VOID", "TRANSFER_IN","TRANSFER_OUT"]
transaction_method = ["ACH","ATM","CREDIT_CARD","DEBIT_CARD","APP"]


'''generates a random phone number in the proper format.'''
def phone_number():

    phone_number = [str(randint(0, 9)) for _ in range(10)]
    phone_number.insert(3, '-')
    phone_number.insert(7, '-')
    phone_number = ''.join(phone_number)

    return phone_number

'''generates a random password, validated by the password regex used in the application.'''
def password():

    password = ''

    while not re.match(password_regex, password) : #regex check to make sure password provided by faker is valid. 
        password = fake.password(length=10)
    
    return password


'''generates applicant information and returns it in the proper json format for microservice.'''
def applicant():

    reused_data = {
    "address": fake.street_address(),
    "city": fake.city(),
    "state": fake.state(),
    "zipcode": fake.zipcode(),
    }

    applicant_json = {
        "firstName": fake.first_name(),
        "middleName": fake.first_name(),
        "lastName": fake.last_name(),
        "dateOfBirth": str(fake.date_between(date(1970, 1, 1), date(2002, 12, 1))),
        "gender": "UNSPECIFIED",
        "email": fake.email(),
        "phone": phone_number(),
        "socialSecurity": fake.ssn(),
        "driversLicense": "DL" + str(randrange(100000, 999999)),
        "income": 1500001,
        "address": reused_data['address'],
        "city": reused_data['city'],
        "state": reused_data['state'],
        "zipcode": reused_data['zipcode'],
        "mailingAddress": reused_data['address'],
        "mailingCity": reused_data['city'],
        "mailingState": reused_data['state'],
        "mailingZipcode": reused_data['zipcode']
    }

    return applicant_json

'''generates application information and returns it in the proper json format for microservice.'''
def application(applicant_id):

    application_json = {
        "applicationType": application_type[randint(0,2)],
        "noApplicants": True,
        "applicantIds": [applicant_id],
    }

    return application_json

'''generates user information adn returns it in the proper json format for microservice.'''
def user(**applicant_info) :
    
