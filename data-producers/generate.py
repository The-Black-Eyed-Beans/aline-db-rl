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


'''[DEPRECATED] function to manually remove all symbols not accepted by the regex expression used by Aline. [DEPRECATED]'''
def password_cleaner(password):
    new_password = password.replace("+","").replace("(","").replace(")","").replace("+","")
    return new_password

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

'''generates application information and returns it in the proper json format for microservice. Requires applicant id'''
def application(applicant_id):

    application_json = {
        "applicationType": application_type[randint(0,2)],
        "noApplicants": True,
        "applicantIds": [applicant_id],
    }

    return application_json

'''generates user information and returns it in the proper json format for microservice.'''
'''
    applicant_info keys:
        first_name
        last_name
        email
        phone
        membership_id
        ssn
'''
def user(**applicant_info) :
    
    user_json = {
        "role":"member",
        "username": fake.profile(fields=['username'])['username'] + str(randint(10,99)),
        "password": password(),
        "firstName": applicant_info["first_name"],
        "lastName": applicant_info["last_name"],
        "email": applicant_info['email'],
        "phone": applicant_info["phone"],
        "membershipId": applicant_info['membership_id'],
        "lastFourOfSSN": str(applicant_info["ssn"])[7:11]
    }

    return user_json

'''generates transaction information and returns it in the proper json format for microservice. Requires account number'''
def transaction(account_number):

    transaction_json ={
        "type": transaction_type[randint(0,7)],
        "method": transaction_method[randint(0,4)],
        "amount": randint(1000, 5000),
        "merchantCode": 'hj1234',
        "merchantName": 'Hillcrest ATM',
        "description": 'High class merchant',
        "cardNumber": None,
        "accountNumber": account_number
    }

    return transaction_json

'''generates bank information and returns it in the proper json format for microservice.'''
def bank():

    bank_json  = {
        "routingNumber": "".join([str(randint(0,9)) for _ in range(9)]),
        "address": fake.street_address(),
        "city": fake.city(),
        "state": fake.state(),
        "zipcode": fake.zipcode()
    }

    return bank_json

'''generates branch information and returns it in the proper json format for microservice. requires bank json'''
def branch(bank_json):

    branch_json = {
        "name": fake.word() + "branch",
        "phone": phone_number,
        "address": bank_json["address"],
        "city": bank_json['city'],
        "state": bank_json['state'],
        "zipcode": bank_json['zipcode'],
        "bankID": bank.json()['id']
    }

    return branch_json
