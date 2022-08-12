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
    print(event)
    print(context)
    response = {
        "event": event
    }
    response = json.dumps(response)
    try:
        print(response)
        body = json.loads(event['body'])
    except Exception as e:
        print(e)
    return get_list_by_id(body['list_id'])


def get_list_by_id(list_id):
    print(f"Getting list {list_id}")
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


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return jsonJSONEncoder.default(self, obj)