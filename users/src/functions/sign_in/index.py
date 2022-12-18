import os
import boto3
from http import HTTPStatus
import json


def sign_in(email, password):
    cidp = boto3.client('cognito-idp')
    pool_client_id = os.getenv('FAVORITES_USER_POOL_CLIENT_ID')
    try:
        auth_rsp = cidp.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password
            },
            ClientId=pool_client_id
        )
        print("SUCCESSFULLY AUTHENTICATED USER")
        auth_results = {
            "id_token": auth_rsp['AuthenticationResult']['IdToken'],
            "refresh_token": auth_rsp['AuthenticationResult']['RefreshToken'],
            "token_type": auth_rsp['AuthenticationResult']['TokenType']
        }
        response = {
            "message": "User has been successfully authenticated",
            "auth_results": auth_results
        }     
    except cidp.exceptions.NotAuthorizedException as e:
        response = {
            "statusCode": HTTPStatus.BAD_REQUEST,
            "message": "The email or password provided are incorrect. Please try again"
        }
    except cidp.exceptions.UserNotFoundException as e:
        response = {
            "statusCode": HTTPStatus.BAD_REQUEST,
            "message": "The email or password provided are incorrect. Please try again"
        }
    except cidp.exceptions.UserNotConfirmedException as e:
        response = {
            "statusCode": HTTPStatus.BAD_REQUEST,
            "message": "Please verify your email address"            
        }
    except Exception as e:
        response = {
            "statusCode": HTTPStatus.BAD_REQUEST,
            "message": "An unexpected error has occurred"           
        }
    return response