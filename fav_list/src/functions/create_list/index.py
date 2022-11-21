import json
import boto3
import os
import uuid
from src.models.list_entity import ListEntity
from src.models.list_metadata_entity import ListMetadataEntity
from datetime import datetime
from pprint import pprint
import json

dynamodb = boto3.client('dynamodb')
table_name = os.environ['FAVORITES_TABLE_NAME']

def create_list(
        title, visibility, 
        description, notes, username):
    list_uuid = str(uuid.uuid4())
    list_size = int(os.environ['MAX_LIST_SIZE'])
    list_data = {
        "list_uuid": list_uuid,
        "username": username,
        "list_size": list_size
    }
    new_list = ListEntity(list_data)
    timestamp = datetime.now().isoformat(timespec='seconds')
    # Create the actual contents of the empty list and generate a DynamoDB put item
    list_items = new_list.generate_empty_list_put_items()
    #print(json.dumps(list_items, indent=4))
    #pprint(list_items, width=1)
    # Create Metadata object to generate a DynamoDB put item
    metadata_data = {
        "username": username,
        "list_uuid": list_uuid,
        "list_size": list_size,
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