import boto3
from botocore import exceptions as aws_exceptions
import os
from http import HTTPStatus


def sign_up(first_name, last_name, email, password):
    cidp = boto3.client('cognito-idp')
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
        print("User signed up successfully")
        response = {
            "message": "User successfully signed up.",
            "cognito_user_id": sign_up_rsp['UserSub']
        }        
    except aws_exceptions.ClientError as client_error:
        print("Client error occurred")
        if client_error.response['Error']['Code'] == 'UsernameExistsException':  
            response = {
                "statusCode": HTTPStatus.BAD_REQUEST,
                "message": "Email address has already been used."
            }  
        else:
            response = {
                "statusCode": HTTPStatus.BAD_REQUEST,
                "message": "An unexpected error has occurred"
            }
    return response