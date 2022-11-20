import json
import boto3
import os
from src.models.list_entity import ListEntity
from src.models.list_metadata_entity import ListMetadataEntity
from datetime import datetime

dynamodb = boto3.client('dynamodb')
table_name = os.environ['FAVORITES_TABLE_NAME']

def create_list(
        title, visibility, 
        description, notes, comment, username
):
    print("table_name:", table_name)
    print("Available tables:", dynamodb.list_tables(), sep='\n')
    new_list = ListEntity()
    list_uuid = new_list.get_list_uuid()
    timestamp = datetime.now().isoformat(timespec='seconds')
    # Create the actual contents of the empty list and generate a DynamoDB put item
    list_items = new_list.generate_empty_list_put_item(username)

    # Create Metadata object to generate a DynamoDB put item
    metadata_data = {
        "username": username,
        "list_uuid": list_uuid,
        "list_size": new_list.get_list_size(),
        "created_at": timestamp,
        "visibility": visibility,
        "title": title,
        "description": description,
        "notes": notes
    }
    metadata_entity = ListMetadataEntity(metadata_data)
    list_items.append(metadata_entity.generate_put_metadata_list_item())
    try:
        db_response = dynamodb.transact_write_items(TransactItems=list_items)
        response = {
            "message": "Successfully created list",
            "list_id": list_uuid
        }
        return response
    except Exception as err:
        raise err