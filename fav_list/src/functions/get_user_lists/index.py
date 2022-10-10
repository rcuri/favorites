import json
import boto3
import os
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from http import HTTPStatus
from src.encoders import DecimalEncoder

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['FAVORITES_TABLE_NAME'])


def list_all_lists_per_user(username):
    print(f"Getting lists for user {username}")
    try:
        response = table.query(
            KeyConditionExpression=Key('PK').eq(username) & Key('SK').begins_with(f"LIST#")
        )
        print(response)
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