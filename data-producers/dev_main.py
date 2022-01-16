import os
import logging

import request
import produce

#TODO: modify income to randomize.
#TODO: wrap request api calls with try/except.

if __name__ == '__main__' :

    #logging
    logging.basicConfig(filename = "logfile.log", filemode='w', format='[%(asctime)s][%(levelname)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
    
    bearer = request.login(os.getenv('ALINE_ADMIN_USERNAME'), os.getenv('ALINE_ADMIN_PASSWORD'), os.getenv('USER_HOST')) 
    
    if not bearer :  #if failure, log and exit the program.
        logging.error("Was not able to acquire bearer token. Exiting process.")
        quit()

    produce.applications_to_users(50, 1, bearer)

    produce.banks_and_branches(10, bearer)
    
    
    