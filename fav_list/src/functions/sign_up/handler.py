from .index import sign_up_user
from aws_lambda_powertools import Logger, Tracer

logger = Logger(service="sign_up")


@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    user_data = json.loads(event['body'])
    first_name = user_data['first_name']
    last_name = user_data['last_name']
    email = user_data['email']
    password = user_data['password']

    return sign_up_user(first_name, last_name, email, password)