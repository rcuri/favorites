import json
from .index import update_list_metadata
from aws_lambda_powertools import Logger, Tracer

logger = Logger(service="update_list_metadata")


@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    body = json.loads(event['body'])
    list_id = body['list_id']
    item_data = body['data']
    return update_list_metadata(list_id, item_data)
