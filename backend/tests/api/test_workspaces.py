from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def get_auth_token():
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "authtest@example.com",
            "password": "NewTestPassword123",
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def test_create_workspace_success():
    token = get_auth_token()

    slug = f"test-workspace-{uuid4().hex[:8]}"

    response = client.post(
        "/api/v1/workspaces",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "name": "Test Workspace",
            "slug": slug,
            "description": "Workspace for API testing",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test Workspace"
    assert data["slug"] == slug
    assert data["description"] == "Workspace for API testing"
    assert data["is_active"] is True
    assert data["owner_id"]


def test_create_workspace_without_token():
    slug = f"no-auth-{uuid4().hex[:8]}"

    response = client.post(
        "/api/v1/workspaces",
        json={
            "name": "Unauthorized Workspace",
            "slug": slug,
        },
    )

    assert response.status_code == 401


def test_create_workspace_invalid_slug():
    token = get_auth_token()

    response = client.post(
        "/api/v1/workspaces",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "name": "Invalid Workspace",
            "slug": "Invalid Slug!",
        },
    )

    assert response.status_code == 422


def test_create_workspace_short_name():
    token = get_auth_token()

    response = client.post(
        "/api/v1/workspaces",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "name": "A",
            "slug": f"short-name-{uuid4().hex[:8]}",
        },
    )

    assert response.status_code == 422


def test_create_workspace_duplicate_slug():
    token = get_auth_token()

    slug = f"duplicate-{uuid4().hex[:8]}"

    first_response = client.post(
        "/api/v1/workspaces",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "name": "First Workspace",
            "slug": slug,
        },
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/api/v1/workspaces",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "name": "Second Workspace",
            "slug": slug,
        },
    )

    assert second_response.status_code == 409


def test_list_workspaces():
    token = get_auth_token()

    slug = f"list-test-{uuid4().hex[:8]}"

    create_response = client.post(
        "/api/v1/workspaces",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "name": "List Test Workspace",
            "slug": slug,
        },
    )

    assert create_response.status_code == 201

    response = client.get(
        "/api/v1/workspaces",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert any(
        workspace["slug"] == slug
        for workspace in data
    )


def test_list_workspaces_without_token():
    response = client.get(
        "/api/v1/workspaces",
    )

    assert response.status_code == 401


def test_get_workspace_success():
    token = get_auth_token()

    create_response = client.post(
        "/api/v1/workspaces",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "name": "Get Test Workspace",
            "slug": f"get-test-{uuid4().hex[:8]}",
        },
    )

    assert create_response.status_code == 201

    workspace_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/workspaces/{workspace_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == workspace_id
    assert data["name"] == "Get Test Workspace"


def test_get_nonexistent_workspace():
    token = get_auth_token()

    fake_workspace_id = str(uuid4())

    response = client.get(
        f"/api/v1/workspaces/{fake_workspace_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 404


def test_get_workspace_without_token():
    fake_workspace_id = str(uuid4())

    response = client.get(
        f"/api/v1/workspaces/{fake_workspace_id}",
    )

    assert response.status_code == 401


def test_delete_workspace_success():
    token = get_auth_token()

    create_response = client.post(
        "/api/v1/workspaces",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "name": "Delete Test Workspace",
            "slug": f"delete-test-{uuid4().hex[:8]}",
        },
    )

    assert create_response.status_code == 201

    workspace_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/api/v1/workspaces/{workspace_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/api/v1/workspaces/{workspace_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert get_response.status_code == 404


def test_delete_nonexistent_workspace():
    token = get_auth_token()

    response = client.delete(
        f"/api/v1/workspaces/{uuid4()}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 404


def test_delete_workspace_without_token():
    response = client.delete(
        f"/api/v1/workspaces/{uuid4()}",
    )

    assert response.status_code == 401