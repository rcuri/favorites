from src.util import build_update_expression
import uuid
import os


class ListEntity:
    table_name = os.environ['FAVORITES_TABLE_NAME']

    def __init__(self):
        self.list_uuid = self.generate_list_uuid()        
        self.list_id = self.generate_list_id()
        self.list_size = 20

    @classmethod
    def update_list_item(cls, list_id, list_data, username):
        items = []
        for item in list_data:
            list_item = {
                "Update": {
                    "TableName": ListEntity.table_name,
                    "Key": {
                        "PK": {
                            "S": username
                        },
                        "SK": {
                            "S": item['name']
                        }
                    }
                }
            }
            vals, exp, attr_names = build_update_expression(item['data'])            
            list_item['Update']['UpdateExpression'] = exp
            list_item['Update']['ExpressionAttributeNames'] = attr_names
            list_item['Update']['ExpressionAttributeValues'] = vals
            items.append(list_item)            
        return items

    @classmethod
    def generate_delete_list_items(cls, list_uuid, username):
        items = []
        # 21 since max list size is 20.
        # TODO pass in list_size as parameter
        for row_no in range(1, 21):
            row_name = f"LIST#{list_uuid}#ROW_{row_no}"
            list_item = {
                "Delete": {
                    "TableName": ListEntity.table_name,
                    "Key": {
                        "PK": {
                            "S": username
                        },
                        "SK": {
                            "S": row_name
                        }
                    }
                }
            }
            items.append(list_item)            
        return items        

    def get_list_size(self):
        return self.list_size

    def get_list_uuid(self):
        return self.list_uuid

    def generate_list_uuid(self):
        list_uuid = str(uuid.uuid4())
        return list_uuid

    def generate_list_id(self):
        prefix = "LIST#"
        return prefix + self.list_uuid


    def generate_empty_list_put_item(self, username):
        items = []
        # Information about the list
        # The contents of the list
        for row_no in range(1, self.list_size+1):
            item = {
                "Put": {
                    "Item": {
                        "PK": {
                            "S": username
                        },
                        "SK": {
                            "S": f"{self.list_id}#ROW_{row_no}"
                        },
                        "content": {
                            "S": ""
                        }
                    },
                    "TableName": ListEntity.table_name
                }
            }
            items.append(item)
        return items        