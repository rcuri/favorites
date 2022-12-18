import boto3
from botocore import exceptions as aws_exceptions
import os
from http import HTTPStatus
import json


def confirm_email(email, confirmation_code):
    cidp = boto3.client('cognito-idp')
    cognito_client_id = os.getenv('FAVORITES_USER_POOL_CLIENT_ID')
    try:
        print("Confirming user's email address")
        confirmed_response = cidp.confirm_sign_up(
            ClientId=cognito_client_id,
            Username=email,
            ConfirmationCode=confirmation_code,
        )
        print("Email address successfully confirmed")
        response = {
            "message": "Email address was successfully verified."
        }      
    except aws_exceptions.ClientError as client_error:
        print("Client error occurred")
        print(client_error)
        if client_error.response['Error']['Code'] == 'UsernameExistsException':
            print("Username exists exception")
            response = {
                "statusCode": HTTPStatus.BAD_REQUEST,
                "message": "Email address has already been used."
            }            
        else:
            print("Other error")
            response = {
                "statusCode": HTTPStatus.BAD_REQUEST,
                "message": "An unexpected error has occurred"
            }
    return response