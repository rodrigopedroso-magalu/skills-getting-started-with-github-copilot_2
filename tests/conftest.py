from copy import deepcopy

import pytest

from src import app as app_module
from fastapi.testclient import TestClient


@pytest.fixture(scope="function")
def client():
    original_activities = deepcopy(app_module.activities)
    client = TestClient(app_module.app)
    yield client
    app_module.activities.clear()
    app_module.activities.update(original_activities)
