import json
import boto3
import os
from http import HTTPStatus
from src.encoders import DecimalEncoder
from src.models.list_entity import ListEntity

dynamodb = boto3.client('dynamodb')
table_name = os.environ['FAVORITES_TABLE_NAME']

def update_list_contents(list_id, fav_list):
    item_data = {
        "list_id": list_id,
        "data": fav_list
    }
    list_contents = ListEntity(item_data)
    updated_items = list_contents.update_list_item(table_name)
    """
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
    """
    try:
        print("TRYING TO WRITE")
        response = dynamodb.transact_write_items(TransactItems=updated_items)
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