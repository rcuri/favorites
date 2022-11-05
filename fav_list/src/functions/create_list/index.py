import json
import boto3
import os
import uuid
from src.models.list_entity import ListEntity
from datetime import datetime

dynamodb = boto3.client('dynamodb')
table_name = os.environ['FAVORITES_TABLE_NAME']

def create_list(
        title, fav_list, visibility, 
        description, notes, comment, user
):
    new_list = ListEntity()
    username = user
    list_items = []
    timestamp = datetime.now().isoformat(timespec='seconds')    
    user_item = {
        "Put": {
            "Item": {
                "PK": {
                    "S": username
                },
                "SK": {
                    "S": new_list.get_list_id()
                },
                "list_size": {
                    "N": str(new_list.get_list_size())
                },
                "created_at": {
                    "S": notes
                },
                "updated_at": {
                    "S": timestamp
                },
                "visibility": {
                    "S": visibility
                },
                "title": {
                    "S": title
                },
                "descripton": {
                    "S": description
                },
                "notes": {
                    "S": notes
                }
            },
            "TableName": table_name
        }
    }
    list_items.append(user_item)
    favorites_list_information = new_list.create_list_information_item(comment, timestamp)
    list_items.append(favorites_list_information)    
    list_items.extend(new_list.get_list_items())
    try:
        response = dynamodb.transact_write_items(TransactItems=list_items)
        return user_item
    except Exception as err:
        raise err