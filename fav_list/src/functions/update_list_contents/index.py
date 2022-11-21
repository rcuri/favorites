import json
import boto3
import os
from http import HTTPStatus
from src.models.list_entity import ListEntity

dynamodb = boto3.client('dynamodb')
table_name = os.environ['FAVORITES_TABLE_NAME']

def update_list_contents(list_uuid, fav_list, username):
    list_size = int(os.environ['MAX_LIST_SIZE'])
    list_data = {
        "list_uuid": list_uuid,
        "list_size": list_size,
        "username": username
    }    
    list_entity = ListEntity(list_data)
    updated_items = ListEntity.update_list_item(fav_list)
    try:
        db_response = dynamodb.transact_write_items(TransactItems=updated_items)
        response = {
            "message": "List has been successfully updated"
        }
        return response
    except Exception as err:
        raise err
