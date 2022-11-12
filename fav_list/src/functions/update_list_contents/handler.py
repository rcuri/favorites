import json
from src.functions.update_list_contents.index import update_list_contents
from aws_lambda_powertools import Logger

logger = Logger(service="update_list_contents")


@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    list_id = event['pathParameters']['list_id']
    username = event['requestContext']['authorizer']['jwt']['claims']['sub']    
    body = json.loads(event['body'])
    return update_list_contents(username, list_id, body['data'])


