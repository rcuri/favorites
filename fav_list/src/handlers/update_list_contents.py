import json
import boto3
import os
import uuid
from decimal import Decimal
from http import HTTPStatus

dynamodb = boto3.client('dynamodb')
table_name = os.environ['FAVORITES_TABLE_NAME']

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
    return update_list_contents(body['list_id'], body['data'])


def update_list_contents(list_id, fav_list):
    list_items = []
    for item in fav_list:
        list_item = {
            "Update": {
                "TableName": table_name,
                "Key": {
                    "PK": {
                        "S": list_id
                    },
                    "SK": {
                        "S": item['name']
                    }
                }
            }
        }
        vals, exp, attr_names = build_update_expression(item['data'])            
        print(vals)
        print(exp)
        print(attr_names)
        list_item['Update']['UpdateExpression'] = exp
        list_item['Update']['ExpressionAttributeNames'] = attr_names
        list_item['Update']['ExpressionAttributeValues'] = vals
        list_items.append(list_item)
    try:
        print("TRYING TO WRITE")
        response = dynamodb.transact_write_items(TransactItems=list_items)
        print("IT WORKS")
        print(response)
        body = {
            "response": response
        }
        http_response = {
            "statusCode": HTTPStatus.OK,
            "body": json.dumps(body, cls=DecimalEncoder)
        }
        return http_response
    except Exception as err:
        raise err


def build_update_expression(data):
    pf = 'prefix'
    vals = {}
    exp = 'SET '
    attr_names = {}
    for key,value in data.items():
        vals[':{}'.format(key)] = {"S": value}
        attr_names['#pf_{}'.format(key)] = key
        exp += '#pf_{} = :{},'.format(key, key)
    exp = exp.rstrip(",")
    return vals, exp, attr_names


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)    