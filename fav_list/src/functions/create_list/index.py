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
    new_list = ListEntity()
    list_id = new_list.get_list_id()
    timestamp = datetime.now().isoformat(timespec='seconds')

    # Create the actual contents of the empty list and generate a DynamoDB put item
    list_items = new_list.generate_empty_list_put_item()

    # Create Metadata object to generate a DynamoDB put item
    metadata_data = {
        "username": username,
        "list_id": list_id,
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
            "list_id": list_id.replace("LIST#", "")
        }
        return response
    except Exception as err:
        raise err