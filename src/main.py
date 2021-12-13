import logging
import pandas as pd
import numpy as np
import sys
import mysql.connector
import traceback
import os
from mysql.connector import errorcode

#TODO: implement ability to take in multiple xlsx files maybe
#TODO: logfile

def get_worksheets(file):


    sheets = {
        'bank' : pd.read_excel(file, 'bank'),
        'branch' : pd.read_excel(file, 'branch'),
        'applicant' : pd.read_excel(file, 'applicant'),
        'member' : pd.read_excel(file, 'member'),
        'account' : pd.read_excel(file, 'account'),
        'application' : pd.read_excel(file, 'application'),
        'merchant' : pd.read_excel(file, 'merchant'),
        'user': pd.read_excel(file, 'user'),
        'transaction' : pd.read_excel(file, 'transaction')
    }

    return sheets

#TODO: FIX FOREIGN KEY CONSTRAINT ISSUE WITH USERS TABLE
def populate_table(table_name, table, cursor) :

    print(f"Creating queries for {table_name} with items: \n {[col for col in table]} ")
    
    for i in table.index :
        items = table.iloc[i].array #List of items in current element.

        items = ["'" + item + "'"  if isinstance(item, str) else item for item in items] #adding '' to strings. 
        items = ["'" + str(item) + "'" if isinstance(item, pd._libs.tslibs.timestamps.Timestamp) else item for item in items] #adding '' to datetimes.
        items = [int(item) if isinstance(item, np.float64) else item for item in items] #changing any float values to integer values. 
        items = [str(item) for item in items] #converts all elements to string values for the String.join method.
        items = ['0' if item == 'nan' else item for item in items] #changing NAN values to 0 (assumes all NAN values are the auto increment values, may break later.)

        query = f"INSERT INTO {table_name} VALUES ({', '.join(items)})"

        print(query)

        try:
            cursor.execute(query)
        except:
            #TODO: LOG ERROR
            print(f"Error executing query : {query} ")
            traceback.print_exc()
            return -1
    
    return 0
    

if __name__ == '__main__' :

    cnx_info = {
        'user':'root',
        'password' : 'password',
        'host' : '127.0.0.1',
        'database': 'alinedb',
        'port' : '3307'}


    try:
        cnx = mysql.connector.connect(**cnx_info)
        cursor = cnx.cursor()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access denied. Please check your username and password.")
        else:
            print(err)
    
    
    print("running program .. ")

    logging.basicConfig(filename = "logfile.log", filemode='w', format='[%(asctime)s][%(levelname)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    logging.info("Program has started")

    if len(sys.argv) <= 1 : #no argument was given.
        logging.error("No CLA was given.")
        print("ERROR: Script is expecting at least one CL argument. ")
        logging.info("Shutting down.")
        quit()


    filename = os.path.dirname(__file__) + sys.argv[1]

    with open(filename) as cfile:

        xlsx = pd.ExcelFile(filename)

        sheets = get_worksheets(xlsx)

        err_code = 0

        for table_name in sheets.keys():
            err_code = err_code + populate_table(table_name, sheets[table_name], cursor)
        
        if err_code < 0 :
            print("sorry, there was an error with mysql. will not commit.")
        else:
            cnx.commit()

    cnx.close()


        

