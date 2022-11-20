from src.models.list_metadata_entity import ListMetadataEntity
import pytest


def test_correct_metadata_entity_creation(valid_metadata):
    valid_metadata_entity = ListMetadataEntity(valid_metadata)
    assert isinstance(valid_metadata_entity, ListMetadataEntity)
    assert hasattr(valid_metadata_entity, 'username')
    assert hasattr(valid_metadata_entity, 'list_uuid')
    assert hasattr(valid_metadata_entity, 'list_size')
    assert hasattr(valid_metadata_entity, 'created_at')
    assert hasattr(valid_metadata_entity, 'visibility')
    assert hasattr(valid_metadata_entity, 'title')
    assert hasattr(valid_metadata_entity, 'description') 
    assert hasattr(valid_metadata_entity, 'notes')                        


def test_missing_required_field_creation(invalid_metadata):
    with pytest.raises(KeyError):
        invalid_metadata_entity = ListMetadataEntity(invalid_metadata)

def test_metadata_entity_dynamodb_put_item_generation(valid_metadata, valid_dynamodb_put_item):
    valid_metadata_entity = ListMetadataEntity(valid_metadata)
    metadata_put_item = valid_metadata_entity.generate_put_metadata_list_item()
    assert isinstance(metadata_put_item, dict)
    assert metadata_put_item == valid_dynamodb_put_item

def test_metadata_entity_dynamodb_delete_item_generation(valid_metadata, valid_dynamodb_delete_metadata_item):
    metadata_delete_item = ListMetadataEntity.generate_delete_metadata_item("test_uuid", "testuser")
    assert len(metadata_delete_item) == 1
    assert isinstance(metadata_delete_item[0], dict)
    assert metadata_delete_item[0] == valid_dynamodb_delete_metadata_item

def test_metadata_id_generation(valid_metadata):
    valid_metadata_entity = ListMetadataEntity(valid_metadata)
    metadata_id = valid_metadata_entity.metadata_id
    # TODO change this to regex
    id_type = metadata_id.split("#")[0] 
    assert len(metadata_id.split("#")) == 2
    assert id_type == "LIST_METADATA"


@pytest.fixture
def valid_metadata():
    item = {
        "username": "testuser",
        "list_uuid": "test_uuid",
        "list_size": 20,
        "created_at": "2022-11-09T00:18:25",
        "visibility": "PRIVATE",
        "title": "Test List",
        "description": "This is a valid list for pytest.",
        "notes": "Keep on testing"
    }
    return item


@pytest.fixture
def invalid_metadata():
    # Missing the username and list_uuid fields
    item = {
        "list_uuid": "test_uuid",
        "list_size": 20,
        "created_at": "2022-11-09T00:18:25",
        "visibility": "PRIVATE",
        "title": "Test List",
        "description": "This is the invalid metadata for pytest.",
        "notes": "Keep on testing"
    }    
    return item

@pytest.fixture
def valid_dynamodb_put_item():
        item = {
            "Put": {
                "Item": {
                    "PK": {
                        "S": "testuser"
                    },
                    "SK": {
                        "S": "LIST_METADATA#test_uuid"
                    },
                    "list_size": {
                        "N": "20"
                    },
                    "created_at": {
                        "S": "2022-11-09T00:18:25"
                    },
                    "visibility": {
                        "S": "PRIVATE"
                    },
                    "title": {
                        "S": "Test List"
                    },
                    "description": {
                        "S": "This is a valid list for pytest."
                    },
                    "notes": {
                        "S": "Keep on testing"
                    }
                },
                "TableName": "test-table"
            }
        }
        return item

@pytest.fixture
def valid_dynamodb_delete_metadata_item():
        item = {
            "Delete": {
                "TableName": "test-table",
                "Key": {
                    "PK": {
                        "S": "testuser"
                    },
                    "SK": {
                        "S": "LIST_METADATA#test_uuid"
                    }
                }
            }
        }
        return item        