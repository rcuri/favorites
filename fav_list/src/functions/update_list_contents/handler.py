import json
from .index import update_list_contents
from aws_lambda_powertools import Logger, Tracer

logger = Logger(service="update_list_contents")


@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    body = json.loads(event['body'])
    return update_list_contents(body['list_id'], body['data'])


