from src.models.list_entity import ListEntity
import pytest


def test_correct_list_entity_creation(valid_list_data):
    valid_list_entity = ListEntity(valid_list_data)
    assert isinstance(valid_list_entity, ListEntity)
    assert hasattr(valid_list_entity, 'list_uuid')
    assert hasattr(valid_list_entity, 'list_id')    
    assert hasattr(valid_list_entity, 'list_size')  
    assert hasattr(valid_list_entity, 'username')                    


def test_missing_required_field_creation(invalid_list_data):
    with pytest.raises(KeyError):
        invalid_list_entity = ListEntity(invalid_list_data)

def test_list_id_generation(valid_list_data):
    valid_list_entity = ListEntity(valid_list_data)
    list_id = valid_list_entity.list_id
    # TODO change this to regex
    id_type = list_id.split("#")[0] 
    assert len(list_id.split("#")) == 2
    assert id_type == "LIST"


@pytest.fixture
def valid_list_data():
    # list_uuid generated via str(uuid.uuid4())
    item = {
        "list_uuid": "15d72b2b-6d3a-40cd-868e-95cb7955024e",
        "username": "testuser",
        "list_size": 20
    }
    return item


@pytest.fixture
def invalid_list_data():
    # Missing the required list_size field
    item = {
        "list_uuid": "15d72b2b-6d3a-40cd-868e-95cb7955024e",
        "username": "testuser"
    }    
    return item
