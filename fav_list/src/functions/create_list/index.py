import json
import boto3
import os
import uuid


dynamodb = boto3.client('dynamodb')
table_name = os.environ['FAVORITES_TABLE_NAME']

def create_list(
        title, fav_list, list_size, visibility, 
        description, notes, comment
):
    list_id = str(uuid.uuid4())
    username = "rodrigocuriel95@gmail.com"
    list_items = []    
    user_item = {
        "Put": {
            "Item": {
                "PK": {
                    "S": username
                },
                "SK": {
                    "S": f"LIST#{list_id}"
                },
                "list_size": {
                    "N": str(list_size)
                },
                "created_at": {
                    "S": notes
                },
                "updated_at": {
                    "S": notes
                },
                "visibility": {
                    "S": visibility
                },
                "title": {
                    "S": title
                },
                "descripton": {
                    "S": description
                },
                "notes": {
                    "S": notes
                }
            },
            "TableName": table_name
        }
    }
    list_items.append(user_item)
    for row_no in range(0, list_size+1):
        item = {
            "Put": {
                "TableName": table_name
            }
        }
        if row_no == 0:
            item['Put']['Item']= {
                "PK": {
                    "S": f"LIST#{list_id}"
                },
                "SK": {
                    "S": "LIST"
                },
                "comment": {
                    "S": comment
                },
                "updated_at": {
                    "S": notes
                }
            }
        else:
            item['Put']['Item']= {
                "PK": {
                    "S": f"LIST#{list_id}"
                },
                "SK": {
                    "S": f"LIST#{list_id}#ROW_{row_no}"
                },
                "content": {
                    "S": fav_list[row_no-1]['content'] if fav_list else ""
                }
            }
        list_items.append(item)

    try:
        print("TRYING TO WRITE")
        response = dynamodb.transact_write_items(TransactItems=list_items)
        print("IT WORKS")
        print(response)
        return user_item
    except Exception as err:
        raise err