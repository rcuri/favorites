import json
import boto3
import os
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from http import HTTPStatus
from src.encoders import DecimalEncoder
from aws_lambda_powertools import Logger


logger = Logger(service="get_user_lists")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['FAVORITES_TABLE_NAME'])

def list_all_lists_per_user(username):
    logger.debug(f"Getting lists for user: {username}")
    try:
        response = table.query(
            KeyConditionExpression=Key('PK').eq(username) & Key('SK').begins_with(f"LIST#")
        )
        logger.info("response is {}".format(response))
        body = {
            "response": response
        }
        http_response = {
            "statusCode": HTTPStatus.OK,
            "body": json.dumps(body, cls=DecimalEncoder)
        }
        return http_response
    except ClientError as err:
        print("An error has occurred")
        print(err)
        raise err