import boto3
from botocore import exceptions as aws_exceptions
import os
from http import HTTPStatus
import json
from src.services.users import UserService
from aws_lambda_powertools import Logger


logger = Logger(service="sign_up")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['FAVORITES_TABLE_NAME'])

def sign_up_user(first_name, last_name, email, password):
    try:
        sign_up_response = user_service.sign_up(
            first_name, last_name, email, password
        )
        # User will be identified in table by their Cognito ID
        cognito_user_id = sign_up_response["cognito_user_id"]
        logger.info("User successfully registered with Cognito service")
        logger.debug("Cognito response is {}".format(sign_up_response))
        db_response = table.put_item(
            Item={
                "PK": cognito_user_id,
                "SK": "USER",
                "first_name": first_name,
                "last_name": last_name
            }
        )
        logger.info("Successfully added user to Favorites table")
        logger.debug("DynamoDB put_item response is {}".format(db_response))
        response = {
            "message": "User successfully signed up"
        }
        return response  
    except Exception as e:
        raise e
        print(e)
        return {
            "statusCode": HTTPStatus.BAD_REQUEST,
            "message": str(e)
        }
