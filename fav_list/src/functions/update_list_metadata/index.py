import json
import boto3
import os
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import time
from http import HTTPStatus
from src.encoders import DecimalEncoder
from src.util import build_update_expression

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['FAVORITES_TABLE_NAME'])


def update_list_metadata(list_id, data):
    print(f"Getting list {list_id}")
    user = "rodrigocuriel95@gmail.com"

    try:
        vals, exp, attr_names = build_update_expression(data)
        response = table.update_item(
            Key={
                "PK": user,
                "SK": list_id 
            },
            ConditionExpression="attribute_exists(PK)",
            UpdateExpression=exp,
            ExpressionAttributeNames=attr_names,
            ExpressionAttributeValues=vals,
            ReturnValues="ALL_NEW"
        )
        body = {
            "response": response
        }
        http_response = {
            "statusCode": HTTPStatus.OK,
            "body": json.dumps(body, cls=DecimalEncoder)
        }
        return http_response        
    except ClientError as err:
        print("An error has occurred")
        print(err)
        raise err
