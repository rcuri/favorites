import boto3
import os
from src.models.list_entity import ListEntity
from src.models.list_metadata_entity import ListMetadataEntity

dynamodb = boto3.client('dynamodb')
table_name = os.environ['FAVORITES_TABLE_NAME']

def delete_list(list_uuid, username):
    delete_list_items = ListEntity.generate_delete_list_items(list_uuid, username)
    delete_metadata_items = ListMetadataEntity.generate_delete_metadata_item(list_uuid, username)
    items = delete_list_items + delete_metadata_items
    try:
        db_response = dynamodb.transact_write_items(TransactItems=items)
        print(db_response)
        response = {
            "message": "Successfully deleted list",
            "list_id": list_uuid
        }
        return response
    except Exception as err:
        raise err