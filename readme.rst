====================================================
Flask Rest API serverless with lambda and dynamodb
====================================================

deploy::

    serverless deploy

Talking to REST API
====================

Export the base url for convience::

    export BASE_DOMAIN=https://6n6pw7uzjc.execute-api.eu-west-1.amazonaws.com/dev

Make a new user::

    curl \
        -H "Content-Type: application/json" \
        -X POST ${BASE_DOMAIN}/users \
        -d '{"userId": "pschwendenman", "name": "Paul Schwendenman"}'

Fetch new user::

    curl -H "Content-Type: application/json" -X GET ${BASE_DOMAIN}/users/pschwendenman




Source:

https://serverless.com/blog/flask-python-rest-api-serverless-lambda-dynamodb/