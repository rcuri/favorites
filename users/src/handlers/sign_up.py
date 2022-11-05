import boto3
from botocore import exceptions as aws_exceptions
import os
from http import HTTPStatus
import json
from decimal import Decimal
import base64

def handler(event, context):
    cidp = boto3.client('cognito-idp')
    print(event)
    user_data = json.loads(event['body'])
    first_name = user_data['first_name']
    last_name = user_data['last_name']
    email = user_data['email']
    password = user_data['password']

    user_attributes = [
        {
            "Name": "custom:first_name", 
            "Value": first_name
        },
        {
            "Name": "custom:last_name",
            "Value": last_name
        }
    ]
    print("Signing user up")
    cognito_client_id = os.getenv('FAVORITES_USER_POOL_CLIENT_ID')
    try:
        sign_up_rsp = cidp.sign_up(
            ClientId=cognito_client_id,
            Username=email,
            Password=password,
            UserAttributes=user_attributes
        )
        print(sign_up_rsp)
        print("User signed up successfully")
    except aws_exceptions.ClientError as client_error:
        print("Client error occurred")
        print(client_error)
        if client_error.response['Error']['Code'] == 'UsernameExistsException':
            print("Username exists exception")
            body = {
                "message": "Email address has already been used."
            }   
            response = {
                "statusCode": HTTPStatus.BAD_REQUEST,
                "body": json.dumps(body)
            }  
            raise client_error          
            return response
        else:
            print("Other error")
            response = {
                "statusCode": HTTPStatus.BAD_REQUEST,
                "message": "An unexpected error has occurred"
            }
            return response
    print("User signed up")
    user_pool_id = os.getenv('FAVORITES_USER_POOL_ID')
    verification_required_grp = os.getenv('AWAITING_VERIFICATION_GROUP_NAME')
    try:
        add_to_group_rsp = cidp.admin_add_user_to_group(
            UserPoolId=user_pool_id,
            Username=email,
            GroupName=verification_required_grp
        )
        print("Successfully added user to group")
        body = {
            "response": add_to_group_rsp
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
    print("User added to group")
    body = {
        "message": "User successfully signed up."
    }
    response = {
        "statusCode": HTTPStatus.OK,
        "body": json.dumps(body)
    }
    return response


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)    