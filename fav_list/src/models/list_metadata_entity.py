import os

class ListMetadataEntity:
    table_name = os.environ['FAVORITES_TABLE_NAME']        

    def __init__(self, item):
        self.username = item['username']
        self.list_uuid = item['list_uuid']
        self.metadata_id = self.generate_metadata_id()
        self.list_size = item['list_size']
        self.created_at = item['created_at']
        self.visibility = item['visibility']
        self.title = item['title']
        self.description = item['description']
        self.notes = item['notes']

    def generate_metadata_id(self):
        prefix = "LIST_METADATA#"
        return prefix + self.list_uuid

    def generate_put_metadata_list_item(self):
        item = {
            "Put": {
                "Item": {
                    "PK": {
                        "S": self.username
                    },
                    "SK": {
                        "S": self.metadata_id
                    },
                    "list_size": {
                        "N": str(self.list_size)
                    },
                    "created_at": {
                        "S": self.created_at
                    },
                    "visibility": {
                        "S": self.visibility
                    },
                    "title": {
                        "S": self.title
                    },
                    "descripton": {
                        "S": self.description
                    },
                    "notes": {
                        "S": self.notes
                    }
                },
                "TableName": ListMetadataEntity.table_name
            }
        }
        return item

    @classmethod
    def generate_delete_metadata_item(cls, list_uuid, username):
        metadata_id = f"LIST_METADATA#{list_uuid}"
        item = {
            "Delete": {
                "TableName": ListMetadataEntity.table_name,
                "Key": {
                    "PK": {
                        "S": username
                    },
                    "SK": {
                        "S": metadata_id
                    }
                }
            }
        }
        return [item]            

    @classmethod
    def build_update_expression(cls, data):
        pf = 'prefix'
        vals = {}
        exp = 'SET '
        attr_names = {}
        for key,value in data.items():
            vals[':{}'.format(key)] = value
            attr_names['#pf_{}'.format(key)] = key
            exp += '#pf_{} = :{},'.format(key, key)
        exp = exp.rstrip(",")
        return vals, exp, attr_names        

