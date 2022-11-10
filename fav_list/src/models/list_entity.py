from src.util import build_update_expression
import uuid
import os


class ListEntity:
    table_name = os.environ['FAVORITES_TABLE_NAME']

    def __init__(self):
        self.list_id = self.generate_list_id()
        self.list_size = 20
        self.favorites_list = []


    @classmethod
    def update_list_item(cls, list_id, list_data, table_name):
        items = []
        for item in list_data:
            list_item = {
                "Update": {
                    "TableName": ListEntity.table_name,
                    "Key": {
                        "PK": {
                            "S": list_id
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

    def get_list_size(self):
        return self.list_size

    def get_list_id(self):
        return self.list_id

    def get_list_items(self):
        return self.favorites_list

    def generate_list_id(self, prefix=None):
        if not prefix:
            prefix = "LIST#"
        list_uuid = str(uuid.uuid4())
        return prefix + list_uuid


    def generate_empty_list_put_item(self):
        items = []
        # Information about the list
        # The contents of the list
        for row_no in range(1, self.list_size+1):
            item = {
                "Put": {
                    "Item": {
                        "PK": {
                            "S": self.list_id
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