from src.util import build_update_expression
import uuid


class ListEntity:
    def __init__(self, item=None):
        if item is None:
            item = {}
        self.list_id = item['PK']
        self.name = item['SK']
        self.list_data = item['data']
        self.list_size = 20


    def update_list_item(self, table_name):
        items = []
        for item in self.list_data:
            list_item = {
                "Update": {
                    "TableName": table_name,
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

    def generate_list_id(self, prefix=None):
        if not prefix:
            prefix = ""
        prefix = "LIST#"
        list_uuid = str(uuid.uuid4())
        return prefix + list_uuid

    def create_list_item(self, table_name):
        items = []
        for row_no in range(1, self.list_size+1):
            item = {
                "Put": {
                    "Item": {
                        "PK": {
                            "S": self.list_id
                        },
                        "SK": {
                            "S": f"LIST#{self.list_id}#ROW_{row_no}"
                        },
                        "content": {
                            "S": self.fav_list[row_no]['content']
                        }
                    },
                    "TableName": table_name
                }
            }
            items.append(item)
        return items