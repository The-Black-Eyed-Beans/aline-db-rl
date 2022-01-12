import requests
import re

from faker import Faker
from faker.providers import internet, ssn, person, date_time
from random import randint, randrange
from datetime import date
import time

#TODO: implement way of handing in address to microservice API from user input.
#TODO: determine whether we should create applications. 
#TODO: implement way of taking in admin username and password from args
#TODO: modify income to randomize.
#TODO: wrap request api calls with try/except.

def password_cleaner(password):
    new_password = password.replace("+","").replace("(","").replace(")","").replace("+","")
    return new_password

if __name__ == '__main__' :

    #login

    login_json = {
        "username":"admin1" ,
        "password":"Password1!"
    } 

    login = requests.post('http://127.0.0.1:8070/login' , json=login_json)

    print(f"{login.status_code}")

    #extract bearer token

    bearer = {'authorization':login.headers['Authorization'] }

    print(f"Authorization : {bearer}\n\n\n")

    fake = Faker()

    application_type = ["CHECKING", "SAVINGS", "CHECKING_AND_SAVINGS", "CREDIT_CARD", "LOAN"]
    transaction_type = ["DEPOSIT","WITHDRAWAL","PURCHASE","PAYMENT","REFUND","VOID", "TRANSFER_IN","TRANSFER_OUT"]
    transaction_method = ["ACH","ATM","CREDIT_CARD","DEBIT_CARD","APP"]
    
    #start with applicant -> user production

    for _ in range(50) :

        phone_number = [str(randint(0, 9)) for _ in range(10)]
        phone_number.insert(3, '-')
        phone_number.insert(7, '-')
        phone_number = ''.join(phone_number)

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
            "phone": phone_number,
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

        applicant = requests.post("http://127.0.0.1:8071/applicants", json=applicant_json, headers=bearer) #applicant creation request


        if applicant.status_code > 210 :
            print(f"applicant status code: {applicant.status_code}\ncontent: {applicant.content}\nwith id: {applicant.json()['id']}\n\n\n")
        
        application_json = {
            "applicationType": application_type[randint(0,2)],
            "noApplicants": True,
            "applicantIds": [applicant.json()['id']],
        }

        application = requests.post("http://127.0.0.1:8071/applications", json=application_json, headers=bearer) #application creation request

        if application.status_code > 210 :
            print(f"application status code: {application.status_code}\ncontent: {application.content}\n\n\n")

        password = ''

        password_regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$"

        while not re.match(password_regex, password) : #regex check to make sure password provided by faker is valid. 
            password = fake.password(length=10)


        user_json = {
            "role":"member",
            "username": fake.profile(fields=['username'])['username'] + str(randint(10,99)),
            "password": password,
            "firstName": applicant_json["firstName"],
            "lastName": applicant_json["lastName"],
            "email": applicant_json['email'],
            "phone": applicant_json["phone"],
            "membershipId": application.json()['createdMembers'][0]['membershipId'],
            "lastFourOfSSN": str(applicant_json["socialSecurity"])[7:11]
        }

        user = requests.post("http://127.0.0.1:8070/users/registration", json=user_json, headers=bearer)

        if user.status_code > 210 :
            print(f"user status code: {user.status_code}\ncontent: {user.content}\nwith json:{user_json}\n\n\n")

        for _ in range(1) :


            transaction_json ={
                "type": transaction_type[randint(0,7)],
                "method": transaction_method[randint(0,4)],
                "amount": randint(1000, 5000),
                "merchantCode": 'hj1234',
                "merchantName": 'Hillcrest ATM',
                "description": 'High class merchant',
                "cardNumber": None,
                "accountNumber": application.json()['createdAccounts'][0]['accountNumber']
            }

            transaction = requests.post("http://127.0.0.1:8073/transactions", json=transaction_json, headers=bearer)

            if transaction.status_code > 210:
                print(f"transaction status code: {transaction.status_code}\ncontent: {transaction.content}\nwith json:{transaction_json}")


    #create banks and branches

    for _ in range(50): #TODO: modify this value to ensure more data population

        phone_number = [str(randint(0, 9)) for _ in range(10)]
        phone_number.insert(3, '-')
        phone_number.insert(7, '-')
        phone_number = ''.join(phone_number)
        
        bank_json  = {
            "routingNumber": "".join([str(randint(0,9)) for _ in range(9)]),
            "address": fake.street_address(),
            "city": fake.city(),
            "state": fake.state(),
            "zipcode": fake.zipcode()
        }

        bank = requests.post("http://127.0.0.1:8083/banks", json=bank_json, headers=bearer)


        if bank.status_code > 210 :
            print(f"bank status code: {bank.status_code}\ncontent: {bank.content}\n\n\n")

        branch_json = {
            "name": fake.word() + "branch",
            "phone": phone_number,
            "address": bank_json["address"],
            "city": bank_json['city'],
            "state": bank_json['state'],
            "zipcode": bank_json['zipcode'],
            "bankID": bank.json()['id']
        }

        branch = requests.post("http://127.0.0.1:8083/branches", json=branch_json, headers=bearer)

        if branch.status_code > 210 :
            print(f"branch status code: {branch.status_code}\ncontent: {branch.content}\n\n\n")
    
    
    