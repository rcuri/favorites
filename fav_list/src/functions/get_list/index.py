import json
import boto3
import os
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from http import HTTPStatus
from src.encoders import DecimalEncoder
from aws_lambda_powertools import Logger


logger = Logger(service="get_list_by_id")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['FAVORITES_TABLE_NAME'])


def get_list_by_id(list_id):
    logger.debug(f"Getting list: {list_id}")
    try:
        response = table.query(
            KeyConditionExpression=Key('PK').eq(list_id) & Key('SK').begins_with(f"{list_id}#ROW")
        )
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
