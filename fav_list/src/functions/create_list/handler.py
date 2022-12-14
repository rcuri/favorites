import json
from src.functions.create_list.index import create_list
from aws_lambda_powertools import Logger

logger = Logger(service="create_list")


@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    print(event)
    username = event['requestContext']['authorizer']['jwt']['claims']['sub']
    body = json.loads(event['body']) 
    return create_list(
        body['title'], "PRIVATE",
        body['description'], body['notes'], username
    )
