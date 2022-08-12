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
