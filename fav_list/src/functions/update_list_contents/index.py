import json
import boto3
import os
from http import HTTPStatus
from src.encoders import DecimalEncoder
from src.models.list_entity import ListEntity

dynamodb = boto3.client('dynamodb')
table_name = os.environ['FAVORITES_TABLE_NAME']

def update_list_contents(list_uuid, fav_list):
    list_id = f"LIST#{list_uuid}"
    updated_items = ListEntity.update_list_item(list_id, fav_list, table_name)
    try:
        response = dynamodb.transact_write_items(TransactItems=updated_items)
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