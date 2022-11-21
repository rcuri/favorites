import pytest
from moto import mock_dynamodb
import boto3
import os


def test_successful_list_creation_response_body(valid_create_list_parameters, dynamodb_client):
    from src.functions.create_list.index import create_list
    create_list_response = create_list(
        valid_create_list_parameters['title'],
        valid_create_list_parameters['visibility'],
        valid_create_list_parameters['description'],
        valid_create_list_parameters['notes'],
        valid_create_list_parameters['username']
    )
    assert isinstance(create_list_response, dict)
    assert len(create_list_response.keys()) == 2
    assert "list_id" in create_list_response
    assert isinstance(create_list_response['list_id'], str)
    assert "message" in create_list_response
    assert isinstance(create_list_response['message'], str)
    assert create_list_response['message'] == "Successfully created list"


def test_successful_entities_created(valid_create_list_parameters, dynamodb_client):
    from src.functions.create_list.index import create_list
    # metadata entity and list entity should be created upon list creation
    create_list_response = create_list(
        valid_create_list_parameters['title'],
        valid_create_list_parameters['visibility'],
        valid_create_list_parameters['description'],
        valid_create_list_parameters['notes'],
        valid_create_list_parameters['username']
    )
    username = valid_create_list_parameters['username']
    list_uuid = create_list_response['list_id']
    list_row_prefix = f"LIST#{list_uuid}#ROW_"
    metadata_id = f"LIST_METADATA#{list_uuid}"
    # There should be 20 items since the default list size is 20
    list_items = dynamodb_client.query(
        TableName="test-table",
        ExpressionAttributeValues={
            ":username": {
                "S": username
            },
            ":list_row": {
                "S": list_row_prefix
            }
        },
        ExpressionAttributeNames={
            "#PK": "PK",
            "#SK": "SK"
        },
        KeyConditionExpression="#PK = :username and begins_with(#SK, :list_row)"
    )
    # Metadata item should be created upon successful list creation
    metadata_item = dynamodb_client.get_item(
        Key={
            "PK": {
                "S": username
            },
            "SK": {
                "S": metadata_id
            }
        },
        TableName="test-table"
    )
    assert "Items" in list_items
    assert len(list_items['Items']) > 0
    assert "Item" in metadata_item


def test_successful_entity_uuid_matches(valid_create_list_parameters, dynamodb_client):
    from src.functions.create_list.index import create_list
    # metadata entity and list entity should be created upon list creation
    create_list_response = create_list(
        valid_create_list_parameters['title'],
        valid_create_list_parameters['visibility'],
        valid_create_list_parameters['description'],
        valid_create_list_parameters['notes'],
        valid_create_list_parameters['username']
    )
    username = valid_create_list_parameters['username']
    list_uuid = create_list_response['list_id']
    list_row_prefix = f"LIST#{list_uuid}#ROW_"
    metadata_id = f"LIST_METADATA#{list_uuid}"
    # There should be 20 items since the default list size is 20
    list_items = dynamodb_client.query(
        TableName="test-table",
        ExpressionAttributeValues={
            ":username": {
                "S": username
            },
            ":list_row": {
                "S": list_row_prefix
            }
        },
        ExpressionAttributeNames={
            "#PK": "PK",
            "#SK": "SK"
        },
        KeyConditionExpression="#PK = :username and begins_with(#SK, :list_row)"
    )
    # Metadata item should be created upon successful list creation
    metadata_item = dynamodb_client.get_item(
        Key={
            "PK": {
                "S": username
            },
            "SK": {
                "S": metadata_id
            }
        },
        TableName="test-table"
    )
    # all 20 row items in list must have same list_uuid as metadata item
    row_list_uuids = set()
    for row in list_items['Items']:
        parsed_list_id = row['SK']['S'].split("#")[1]
        row_list_uuids.add(parsed_list_id)
    # metadata entity should have one item with the same list_uuid as rows
    metadata_list_uuid = {metadata_item['Item']['SK']['S'].split("#")[1]}
    assert len(row_list_uuids) == 1
    assert row_list_uuids == metadata_list_uuid


def test_valid_list_structure(valid_create_list_parameters, dynamodb_client):
    from src.functions.create_list.index import create_list
    # metadata entity and list entity should be created upon list creation
    create_list_response = create_list(
        valid_create_list_parameters['title'],
        valid_create_list_parameters['visibility'],
        valid_create_list_parameters['description'],
        valid_create_list_parameters['notes'],
        valid_create_list_parameters['username']
    )
    username = valid_create_list_parameters['username']
    list_uuid = create_list_response['list_id']
    list_row_prefix = f"LIST#{list_uuid}#ROW_"
    # There should be 20 items since the default list size is 20
    list_items = dynamodb_client.query(
        TableName="test-table",
        ExpressionAttributeValues={
            ":username": {
                "S": username
            },
            ":list_row": {
                "S": list_row_prefix
            }
        },
        ExpressionAttributeNames={
            "#PK": "PK",
            "#SK": "SK"
        },
        KeyConditionExpression="#PK = :username and begins_with(#SK, :list_row)"
    )
    assert len(list_items['Items']) == 20

def test_metadata_contains_all_attributes(
            valid_create_list_parameters, required_metadata_attributes_set, dynamodb_client
        ):
    from src.functions.create_list.index import create_list
    # metadata entity and list entity should be created upon list creation
    create_list_response = create_list(
        valid_create_list_parameters['title'],
        valid_create_list_parameters['visibility'],
        valid_create_list_parameters['description'],
        valid_create_list_parameters['notes'],
        valid_create_list_parameters['username']
    )
    username = valid_create_list_parameters['username']
    list_uuid = create_list_response['list_id']
    metadata_id = f"LIST_METADATA#{list_uuid}"
    metadata_item = dynamodb_client.get_item(
        Key={
            "PK": {
                "S": username
            },
            "SK": {
                "S": metadata_id
            }
        },
        TableName="test-table"
    )
    metadata_attributes = {attr for attr in metadata_item['Item'].keys()}
    assert metadata_attributes == required_metadata_attributes_set


# TODO add to conftest.py
@pytest.fixture(scope='function')
def dynamodb_table():
    with mock_dynamodb():
        dynamodb = boto3.resource('dynamodb', 'us-east-1')
        table_name = "test-table"
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "PK", "KeyType": "HASH"},
                {"AttributeName": "SK", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "PK", "AttributeType": "S"},
                {"AttributeName": "SK", "AttributeType": "S"},
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }        
        )
        yield table


# TODO add to conftest.py
@pytest.fixture(scope='function')
def dynamodb_client():
    with mock_dynamodb():
        client = boto3.client('dynamodb', 'us-east-1')
        table_name = "test-table"
        table = client.create_table(
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "PK", "KeyType": "HASH"},
                {"AttributeName": "SK", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "PK", "AttributeType": "S"},
                {"AttributeName": "SK", "AttributeType": "S"},
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }        
        )
        yield client

@pytest.fixture
def valid_create_list_parameters():
    item = {
        "title": "Test List",
        "visibility": "PRIVATE",
        "description": "This is a valid list for pytest.",
        "notes": "Keep on testing",
        "username": "testuser"
    }
    return item


@pytest.fixture
def required_metadata_attributes_set():
    metadata_attributes = {
        "PK", "SK", "list_size", "created_at",
        "visibility", "title", "description", "notes"
    }
    return metadata_attributes