import boto3
from botocore import exceptions as aws_exceptions
import os
from http import HTTPStatus
import json
from decimal import Decimal
from src.services.users import UserService


def handler(event, context):
    print(event)
    user_data = json.loads(event['body'])
    first_name = user_data['first_name']
    last_name = user_data['last_name']
    email = user_data['email']
    password = user_data['password']

    try:
        sign_up_response = user_service.sign_up(
            first_name, last_name, email, password
        )
        print("User successfully registered with Cognito service")

        response = table.put_item(
            Item={
                "PK": email,
                "SK": "USER",
                "first_name": first_name,
                "last_name": last_name
            }
        )
        print("Successfully added user to Favorites table")
        body = {
            "response": response,
            "sign_up_response": sign_up_response.json()
        }
        http_response = {
            "statusCode": HTTPStatus.OK,
            "body": json.dumps(body, cls=DecimalEncoder)
        }     
        return http_response   
    except Exception as e:
        raise e
        print(e)
        return {
            "statusCode": HTTPStatus.BAD_REQUEST,
            "message": str(e)
        }



class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)    