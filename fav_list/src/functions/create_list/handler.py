import json
from .index import create_list
from aws_lambda_powertools import Logger, Tracer

logger = Logger(service="create_list")


@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    print(event)
    response = {
        "event": event
    }
    event = json.dumps(event)
    try:
        print(response)
        body = json.loads(event['body'])
    except Exception as e:
        print(e)
    # TODO add exception here    
    title = body['title']
    fav_list = body['fav_list']
    user = "rodrigocuriel95@gmail.com"
    return create_list(
        body['title'], body['fav_list'], 10, "PRIVATE",
        body['description'], body['notes'], body['comment']
    )
