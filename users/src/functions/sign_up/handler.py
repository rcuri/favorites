import json
from src.functions.sign_up.index import sign_up
from aws_lambda_powertools import Logger

logger = Logger(service="sign_up")


@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    body = json.loads(event['body']) 
    first_name = body['first_name']
    last_name = body['last_name']
    email = body['email']
    password = body['password']
    return sign_up(first_name, last_name, email, password)
