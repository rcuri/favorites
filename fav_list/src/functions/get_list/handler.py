import json
from .index import get_list_by_id
from aws_lambda_powertools import Logger, Tracer

logger = Logger(service="get_list_by_id")


@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    body = json.loads(event['body'])
    return get_list_by_id(body['list_id'])
