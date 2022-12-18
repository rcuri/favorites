import json
from src.functions.sign_in.index import sign_in
from aws_lambda_powertools import Logger

logger = Logger(service="sign_in")


@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    body = json.loads(event['body']) 
    email = body['first_name']
    password = body['password']
    return sign_in(email, password)
