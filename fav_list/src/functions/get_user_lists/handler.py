import json
import boto3
import os
import uuid
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from http import HTTPStatus
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['FAVORITES_TABLE_NAME'])


def handler(event, context):
    response = {
        "event": event
    }
    response = json.dumps(response)
    try:
        print(response)
        body = json.loads(event['body'])
    except Exception as e:
        print(e)
    return list_all_lists_per_user(body['username'])


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

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return jsonJSONEncoder.default(self, obj)