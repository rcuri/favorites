import json
from src.functions.delete_list.index import delete_list
from aws_lambda_powertools import Logger

logger = Logger(service="delete_list")


@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    print(event)
    username = event['requestContext']['authorizer']['jwt']['claims']['sub']
    list_id = event['pathParameters']['list_id']
    return delete_list(list_id, username)
