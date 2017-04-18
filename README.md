
Baby Pool API
==========
This is the API back-end for the baby pool app. It allows submissions and changes to existing entries

## Endpoint
All functions use the common endpoint https://api.eric-ely.com

## Update
/baby_pool/

### GET
Get all current entries

### POST
Post a new entry

#### Arguments

The following arguments must be passed in the data body:
- email: (String) Email address for the entrant
- weight: (String) Weight
- date: (String) Date
- sex: (String) 'M' or 'F'
- comment: (String) Comment with the entrant

#### Response:
Code | Description 
--- | --- 
200| Success

