import os
import boto3
from http import HTTPStatus
import json


def handler(event, context):
    print(event)
    cidp = boto3.client('cognito-idp')
    pool_client_id = os.getenv('FAVORITES_USER_POOL_CLIENT_ID')

    body = json.loads(event['body'])
    email = body['username']
    password = body['password']

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
        print(auth_rsp)
    except cidp.exceptions.NotAuthorizedException as e:
        raise e
        response = {
            "statusCode": HTTPStatus.BAD_REQUEST,
            "message": "The email or password provided are incorrect. Please try again"
        }
        return response
    except cidp.exceptions.UserNotFoundException as e:
        raise e
        response = {
            "statusCode": HTTPStatus.BAD_REQUEST,
            "message": "The email or password provided are incorrect. Please try again"
        }
        return response
    except cidp.exceptions.UserNotConfirmedException as e:
        raise e
        response = {
            "statusCode": HTTPStatus.BAD_REQUEST,
            "message": "Please verify your email address"            
        }
        return response
    except Exception as e:
        raise e
        response = {
            "statusCode": HTTPStatus.BAD_REQUEST,
            "message": "An unexpected error has occurred"           
        }
        return response

    auth_results = {
        "id_token": auth_rsp['AuthenticationResult']['IdToken'],
        "refresh_token": auth_rsp['AuthenticationResult']['RefreshToken'],
        "token_type": auth_rsp['AuthenticationResult']['TokenType']
    }
    body = {
        "message": "User has been successfully authenticated",
        "auth_results": auth_results
    }
    response = {
        "statusCode": HTTPStatus.OK,
        "body": json.dumps(body)
    }
    return response