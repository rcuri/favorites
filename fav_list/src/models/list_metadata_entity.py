from src.util import build_update_expression

class ListMetadataEntity:
    def __init__(self, item=None):
        if item is None:
            item = {}
        self.list_id = item['PK']
        self.name = item['SK']
        self.list_data = item['data']


    def update_list_item (self, data, table_name):
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