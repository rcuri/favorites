class ListMetadataEntity:
    def __init__(self, item=None):
        if item is None:
            item = {}
        self.pk = item['PK']
        self.sk = item['SK']
        self.list_size = item['list_size']
        self.created_at = item['created_at']
        self.updated_at = item['updated_at']
        self.visibility = item['visibility']
        self.title = item['title']
        self.description = item['description']
        self.notes = item['notes']

    def generate_put_user_list_item(self, table_name):
        item = {
            "Put": {
                "Item": {
                    "PK": {
                        "S": self.pk
                    },
                    "SK": {
                        "S": self.sk
                    },
                    "list_size": {
                        "N": self.list_size
                    },
                    "created_at": {
                        "S": self.notes
                    },
                    "updated_at": {
                        "S": self.notes
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
                "TableName": table_name
            }
        }
        return item

    @classmethod
    def build_update_expression(data):
        pf = 'prefix'
        timestamp = int(time.time() * 1000)
        data['updatedAt'] = timestamp
        vals = {}
        exp = 'SET '
        attr_names = {}
        for key,value in data.items():
            vals[':{}'.format(key)] = value
            attr_names['#pf_{}'.format(key)] = key
            exp += '#pf_{} = :{},'.format(key, key)
        exp = exp.rstrip(",")
        return vals, exp, attr_names        

