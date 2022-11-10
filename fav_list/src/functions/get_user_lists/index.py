import boto3
import os
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from http import HTTPStatus
from aws_lambda_powertools import Logger


logger = Logger(service="get_user_lists")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['FAVORITES_TABLE_NAME'])

def list_all_lists_per_user(username):
    logger.debug(f"Getting lists for user: {username}")
    try:
        response = table.query(
            KeyConditionExpression=Key('PK').eq(username) & Key('SK').begins_with(f"LIST#")
        )
        list_items = []
        for item in response['Items']:
            list_response = {
                "list_id": item['SK'].replace("LIST#", ""),
                "title": item['title'],
                "description": item.get('description', "")
            }
            list_items.append(list_response)
        logger.info("response is {}".format(response))
        return {
            "list_items": list_items
        }
    except ClientError as err:
        print("An error has occurred")
        print(err)
        raise err