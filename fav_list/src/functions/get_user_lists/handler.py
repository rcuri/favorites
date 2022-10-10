from .index import list_all_lists_per_user
from aws_lambda_powertools import Logger, Tracer

logger = Logger(service="get_user_lists")


@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    print(response)
    body = json.loads(event['body'])
    return list_all_lists_per_user(body['username'])
