import json
from src.functions.get_list.index import get_list_by_id
from aws_lambda_powertools import Logger

logger = Logger(service="get_list_by_id")


@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    list_id = event['pathParameters']['list_id']    
    return get_list_by_id(list_id)
