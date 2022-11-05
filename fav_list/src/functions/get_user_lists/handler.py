from aws_lambda_powertools import Logger
from src.functions.get_user_lists.index import list_all_lists_per_user


logger = Logger(service="get_user_lists")

# Change to admin route 
@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    user = event['pathParameters']['email']
    return list_all_lists_per_user(user)
