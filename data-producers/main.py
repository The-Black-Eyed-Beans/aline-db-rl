import os
import sys
import logging

import request
import produce

#TODO: wrap request api calls with try/except.

if __name__ == '__main__' :

    #logging
    logging.basicConfig(stream = sys.stdout, filemode='w', format='[%(asctime)s][%(levelname)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
    
    response = request.login(os.getenv('ALINE_ADMIN_USERNAME'), os.getenv('ALINE_ADMIN_PASSWORD'), os.getenv('USER_HOST')) 
    
    if not response :  #if failure, log and exit the program.
        logging.error("Was not able to acquire bearer token. Exiting process.")
        quit()
    else: #if success, retrieve bearer token.
        bearer = {'authorization':response.headers['Authorization'] }

    produce.applications_to_users(50, 10, bearer)

    produce.banks_and_branches(10, bearer)