import datetime
import pytest
from starlette.config import environ
from starlette.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

environ['TESTING'] = 'True'

from guid import app, settings
from guid.db import metadata


FAKE_TIME = datetime.datetime(2020, 12, 25, 17, 5, 55)


@pytest.fixture(scope='session', autouse=True)
def create_test_database():
  """
  Create a clean database on every test case.
  For safety, we should abort if a database already exists.

  We use the `sqlalchemy_utils` package here for a few helpers in consistently
  creating and dropping the database.
  """
  url = str(settings.TEST_DATABASE_URL)
  engine = create_engine(url)
  assert not database_exists(
      url), 'Test database already exists. Aborting tests.'
  create_database(url)             # Create the test database.
  metadata.create_all(engine)      # Create the tables.
  yield                            # Run the tests.
  drop_database(url)               # Drop the test database.


@pytest.fixture()
def client():
    """
    When using the 'client' fixture in test cases, we'll get full database
    rollbacks between test cases:

    def test_homepage(client):
        url = app.url_path_for('homepage')
        response = client.get(url)
        assert response.status_code == 200
    """
    client = TestClient(app)
    with TestClient(app) as client:
        yield client


@pytest.fixture
def patch_datetime_now(monkeypatch):

    class mydatetime:
        @classmethod
        def now(cls):
            return FAKE_TIME

    monkeypatch.setattr(datetime, 'datetime', mydatetime)
