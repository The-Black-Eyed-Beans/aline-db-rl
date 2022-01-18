#Data Producer
## Ricky Lopez

## Required Environment Variables

$ALINE_ADMIN_USERNAME - Username used when logging into Aline Financial.
$ALINE_ADMIN_PASSWORD - Password used when logging into ALine Financial.
$USER_HOST - Host of the user microservice.
$UNDERWRITER_HOST - Host of the underwriter microservice.
$TRANSACTION_HOST - Host of the transaction microservice.
$BANK_HOST - Host of the bank microservice.

## Checks before Running

- Ensure that the database has an admin user already created
- Ensure that database has account_sequence table instantiated with one value (101)
- Ensure that all microservices are running properly, and connected to the database.
