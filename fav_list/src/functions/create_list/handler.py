import json
from src.functions.create_list.index import create_list
from aws_lambda_powertools import Logger, Tracer

logger = Logger(service="create_list")


@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    print(event)
    user = event['requestContext']['authorizer']['jwt']['claims']['email']
    body = json.loads(event['body']) 
    title = body['title']
    fav_list = body['fav_list']
    return create_list(
        body['title'], body['fav_list'], "PRIVATE",
        body['description'], body['notes'], body['comment'], user
    )
