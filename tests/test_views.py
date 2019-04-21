from fastapi import FastAPI
from starlette.config import environ
from starlette.testclient import TestClient


SAMPLE_GUID = '2b10b67540f74a4f8d8197dc1429e30b'


def test_empty_list(client):
    response = client.get('/guid')
    assert response.status_code == 200
    assert response.json() == []


def test_crud(client):
    # Create
    response = client.post('/guid/', json={'name': 'foo'})
    assert response.status_code == 201
    data = response.json()
    assert data['name'] == 'foo'

    # Retrieve
    guid = data['id']
    response = client.get(f'/guid/{guid}')
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == guid
    assert data['name'] == 'foo'

    # Update
    response = client.patch(f'/guid/{guid}',  json={'name': 'bar'})
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'bar'

    # Delete
    response = client.delete(f'/guid/{guid}')
    assert response.status_code == 200

    # Confirm Deletion
    response = client.get(f'/guid/{guid}')
    assert response.status_code == 404
