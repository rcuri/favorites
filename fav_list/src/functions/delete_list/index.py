import boto3
import os
from src.models.list_entity import ListEntity
from src.models.list_metadata_entity import ListMetadataEntity

dynamodb = boto3.client('dynamodb')
table_name = os.environ['FAVORITES_TABLE_NAME']

def delete_list(list_uuid, username):
    list_size = int(os.environ['MAX_LIST_SIZE'])
    list_data = {
        "list_uuid": list_uuid,
        "list_size": list_size,
        "username": username
    }
    list_entity = ListEntity(list_data)
    delete_list_items = list_entity.generate_delete_list_items()
    delete_metadata_items = ListMetadataEntity.generate_delete_metadata_item(list_uuid, username)
    items = delete_list_items + delete_metadata_items
    try:
        db_response = dynamodb.transact_write_items(TransactItems=items)
        response = {
            "message": "Successfully deleted list",
            "list_id": list_uuid
        }
        return response
    except Exception as err:
        raise err