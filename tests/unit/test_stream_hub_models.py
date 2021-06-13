import pytest
from datetime import datetime
from veides.sdk.stream_hub.models import Trail, TrailTimestamp
from tests.unit.fixtures import trail_timestamp


@pytest.mark.parametrize("name,value", [
    ('name', 'value'),
    ('name', 1),
    ('name', 2.21),
])
def test_trail_should_be_created(name, value):
    trail = Trail(name, value, trail_timestamp)

    assert isinstance(trail, Trail)

    assert trail.name == name
    assert trail.value == value

    assert isinstance(trail.timestamp, TrailTimestamp)
    assert trail.timestamp.strftime('%Y-%m-%dT%H:%M:%SZ') == '2021-01-01T12:00:00Z'


@pytest.mark.parametrize("name,value,timestamp", [
    ('name', None, trail_timestamp),
    ('name', 1, str(trail_timestamp)),
    ('name', 1, {}),
    ('name', 1, datetime.utcnow()),
    ('name', lambda: None, trail_timestamp),
    ('name', [], trail_timestamp),
    ('name', {}, trail_timestamp),
    (None, 12, trail_timestamp),
    (lambda: None, 12, trail_timestamp),
    ([], 12, trail_timestamp),
    ({}, 12, trail_timestamp),
])
def test_should_raise_type_error_on_invalid_trail_parameters(name, value, timestamp):
    with pytest.raises(TypeError):
        Trail(name, value, timestamp)


@pytest.mark.parametrize("name,value", [
    ('', 1),
])
def test_should_raise_value_error_on_invalid_trail_data(name, value):
    with pytest.raises(ValueError):
        Trail(name, value, trail_timestamp)
