import boto3
from botocore import exceptions as aws_exceptions
import os
from http import HTTPStatus
import json

def handler(event, context):
    cidp = boto3.client('cognito-idp')
    print(event)
    body = json.loads(event['body'])

    email = body['email']
    confirmation_code = body['confirmation_code']

    cognito_client_id = os.getenv('FAVORITES_USER_POOL_CLIENT_ID')
    try:
        print("Confirming user's email address")
        confirmed_response = cidp.confirm_sign_up(
            ClientId=cognito_client_id,
            Username=email,
            ConfirmationCode=confirmation_code,
        )
        print("Email address successfully confirmed")
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
            return response
        else:
            print("Other error")
            response = {
                "statusCode": HTTPStatus.BAD_REQUEST,
                "message": "An unexpected error has occurred"
            }
            return response
    user_pool_id = os.getenv('FAVORITES_USER_POOL_ID')
    confirmed_user_group = os.getenv('CONFIRMED_USER_GROUP_NAME')
    try:
        add_to_group_response = cidp.admin_add_user_to_group(
            UserPoolId=user_pool_id,
            Username=email,
            GroupName=confirmed_user_group
        )
    except Exception as e:
        print(e)
        return {
            "statusCode": HTTPStatus.BAD_REQUEST,
            "message": str(e)
        }
    print("User added to group")
    body = {
        "message": "Email address was successfully verified."
    }
    response = {
        "statusCode": HTTPStatus.OK,
        "body": json.dumps(body)
    }
    return response