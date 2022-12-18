import json
from src.functions.confirm_email.index import confirm_email
from aws_lambda_powertools import Logger

logger = Logger(service="confirm_email")


@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    body = json.loads(event['body']) 
    email = body['email']
    confirmation_code = body['confirmation_code']
    return confirm_email(email, confirmation_code)
