import json
import boto3
import os
import uuid
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import time
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
    return update_list_metadata(body['list_id'])


def update_list_metadata(list_id, data):
    print(f"Getting list {list_id}")
    user = "rodrigocuriel95@gmail.com"

    try:
        vals, exp, attr_names = build_update_expression(data)
        response = table.update_item(
            Key={
                "PK": user,
                "SK": list_id 
            },
            ConditionExpression="attribute_exists(PK)",
            UpdateExpression=exp,
            ExpressionAttributeNames=attr_names,
            ExpressionAttributeValues=vals,
            ReturnValues="ALL_NEW"
        )
        body = {
            "response": response
        }
        http_response = {
            "statusCode": HTTPStatus.OK,
            "body": json.dumps(body, cls=DecimalEncoder)
        }
        return http_response        
        return response
    except ClientError as err:
        print("An error has occurred")
        print(err)
        raise err

def build_update_expression(data):
    pf = 'prefix'
    timestamp = int(time.time() * 1000)
    data['updatedAt'] = timestamp
    vals = {}
    exp = 'SET '
    attr_names = {}
    for key,value in data.items():
        vals[':{}'.format(key)] = value
        attr_names['#pf_{}'.format(key)] = key
        exp += '#pf_{} = :{},'.format(key, key)
    exp = exp.rstrip(",")
    return vals, exp, attr_names

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return jsonJSONEncoder.default(self, obj)    