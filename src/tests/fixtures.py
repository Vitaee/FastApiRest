import pytest, sys, os, asyncio
from starlette.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from src.config.mongo_service import db_mongo
from src.utils.env_service import env_service

@pytest.fixture(scope="session")
def test_client():
    from main import app
    with TestClient(app) as test_client:
        yield test_client

    db = asyncio.run(db_mongo.connect_to_mongo())

    # db[env_service.get_env_var('DB_NAME')]['user'].drop()
    # db[env_service.get_env_var('DB_NAME')]['student'].drop()

