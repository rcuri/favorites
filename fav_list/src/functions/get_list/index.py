import json
import boto3
import os
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from http import HTTPStatus
from src.encoders import DecimalEncoder
from aws_lambda_powertools import Logger
from collections import defaultdict


logger = Logger(service="get_list_by_id")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['FAVORITES_TABLE_NAME'])


def get_list_by_id(list_uuid):
    list_id = f"LIST#{list_uuid}"
    logger.debug(f"Getting list: {list_id}")
    try:
        db_response = table.query(
            KeyConditionExpression=Key('PK').eq(list_id) & Key('SK').begins_with(f"{list_id}#ROW")
        )
        response = {
            "list_id": list_uuid,
            "items": defaultdict()
        }
        for item in db_response['Items']:
            # Get row number from sort key
            row_no = item['SK'].split("#")[-1]
            response['items'][row_no] = {
                "content": item['content']
            }
        return response
    except ClientError as err:
        print("An error has occurred")
        print(err)
        raise err
