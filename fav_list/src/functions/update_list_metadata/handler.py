import json
from src.functions.update_list_metadata.index import update_list_metadata
from aws_lambda_powertools import Logger

logger = Logger(service="update_list_metadata")


@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    list_id = event['pathParameters']['list_id']
    user = event['requestContext']['authorizer']['jwt']['claims']['email']
    body = json.loads(event['body'])
    item_data = body['data']
    return update_list_metadata(list_id, item_data, user)
