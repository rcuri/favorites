import json
import boto3
import os
from http import HTTPStatus
from src.models.list_entity import ListEntity

dynamodb = boto3.client('dynamodb')
table_name = os.environ['FAVORITES_TABLE_NAME']

def update_list_contents(list_uuid, fav_list):
    list_id = f"LIST#{list_uuid}"
    updated_items = ListEntity.update_list_item(list_id, fav_list, table_name)
    try:
        db_response = dynamodb.transact_write_items(TransactItems=updated_items)
        response = {
            "message": "List has been successfully updated"
        }
        return response
    except Exception as err:
        raise err
