from src.util import build_update_expression
import uuid
import os


class ListEntity:
    table_name = os.environ['FAVORITES_TABLE_NAME']

    def __init__(self, item):
        self.username = item['username']
        self.list_uuid = item['list_uuid']     
        self.list_id = self.generate_list_id()
        self.list_size = item['list_size']
    
    def generate_list_id(self):
        prefix = "LIST#"
        return prefix + self.list_uuid

    def update_list_item(self, list_data):
        items = []
        for item in list_data:
            list_item = {
                "Update": {
                    "TableName": ListEntity.table_name,
                    "Key": {
                        "PK": {
                            "S": self.username
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

    def generate_delete_list_items(self):
        items = []
        # 21 since max list size is 20.
        # TODO pass in list_size as parameter
        for row_no in range(1, self.list_size+1):
            row_name = f"LIST#{self.list_uuid}#ROW_{row_no}"
            list_item = {
                "Delete": {
                    "TableName": ListEntity.table_name,
                    "Key": {
                        "PK": {
                            "S": self.username
                        },
                        "SK": {
                            "S": row_name
                        }
                    }
                }
            }
            items.append(list_item)            
        return items        

    def generate_empty_list_put_items(self):
        items = []
        # Information about the list
        # The contents of the list
        for row_no in range(1, self.list_size+1):
            item = {
                "Put": {
                    "Item": {
                        "PK": {
                            "S": self.username
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