import json
import boto3
import os
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from http import HTTPStatus
from src.encoders import DecimalEncoder
from src.util import build_update_expression
from aws_lambda_powertools import Logger

logger = Logger(service="update_list_metadata")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['FAVORITES_TABLE_NAME'])


def update_list_metadata(list_uuid, data, user):
    list_id = f"LIST#{list_id}"
    user = user
    logger.info(f"Updating list: {list_id}")
    logger.info("submitted data {}".format(data))

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
