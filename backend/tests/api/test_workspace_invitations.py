from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def login(email: str, password: str = "NewTestPassword123") -> str:
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def register_user(email: str, username: str, password: str = "TestPassword123"):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "username": username,
            "full_name": "Invitation Test User",
            "password": password,
        },
    )

    assert response.status_code == 201


def create_workspace(token: str) -> dict:
    response = client.post(
        "/api/v1/workspaces",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "name": "Invitation Test Workspace",
            "slug": f"invitation-{uuid4().hex[:8]}",
        },
    )

    assert response.status_code == 201

    return response.json()


def test_create_invitation_success():
    owner_token = login("authtest@example.com")
    workspace = create_workspace(owner_token)

    invite_email = f"invite-{uuid4().hex[:8]}@example.com"

    response = client.post(
        f"/api/v1/workspaces/{workspace['id']}/invitations",
        headers={
            "Authorization": f"Bearer {owner_token}",
        },
        json={
            "email": invite_email,
            "role": "member",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["workspace_id"] == workspace["id"]
    assert data["email"] == invite_email
    assert data["role"] == "member"
    assert data["token"]
    assert data["accepted_at"] is None
    assert data["expires_at"]


def test_create_admin_invitation_by_owner():
    owner_token = login("authtest@example.com")
    workspace = create_workspace(owner_token)

    invite_email = f"admin-{uuid4().hex[:8]}@example.com"

    response = client.post(
        f"/api/v1/workspaces/{workspace['id']}/invitations",
        headers={
            "Authorization": f"Bearer {owner_token}",
        },
        json={
            "email": invite_email,
            "role": "admin",
        },
    )

    assert response.status_code == 201
    assert response.json()["role"] == "admin"


def test_create_invitation_without_token():
    workspace_id = str(uuid4())

    response = client.post(
        f"/api/v1/workspaces/{workspace_id}/invitations",
        json={
            "email": "invite@example.com",
            "role": "member",
        },
    )

    assert response.status_code == 401


def test_create_invitation_nonexistent_workspace():
    owner_token = login("authtest@example.com")

    response = client.post(
        f"/api/v1/workspaces/{uuid4()}/invitations",
        headers={
            "Authorization": f"Bearer {owner_token}",
        },
        json={
            "email": "invite@example.com",
            "role": "member",
        },
    )

    assert response.status_code == 404


def test_create_invitation_invalid_email():
    owner_token = login("authtest@example.com")
    workspace = create_workspace(owner_token)

    response = client.post(
        f"/api/v1/workspaces/{workspace['id']}/invitations",
        headers={
            "Authorization": f"Bearer {owner_token}",
        },
        json={
            "email": "not-an-email",
            "role": "member",
        },
    )

    assert response.status_code == 422


def test_create_invitation_invalid_role():
    owner_token = login("authtest@example.com")
    workspace = create_workspace(owner_token)

    response = client.post(
        f"/api/v1/workspaces/{workspace['id']}/invitations",
        headers={
            "Authorization": f"Bearer {owner_token}",
        },
        json={
            "email": "invite@example.com",
            "role": "owner",
        },
    )

    assert response.status_code == 422


def test_duplicate_active_invitation():
    owner_token = login("authtest@example.com")
    workspace = create_workspace(owner_token)

    invite_email = f"duplicate-{uuid4().hex[:8]}@example.com"

    first_response = client.post(
        f"/api/v1/workspaces/{workspace['id']}/invitations",
        headers={
            "Authorization": f"Bearer {owner_token}",
        },
        json={
            "email": invite_email,
            "role": "member",
        },
    )

    assert first_response.status_code == 201

    second_response = client.post(
        f"/api/v1/workspaces/{workspace['id']}/invitations",
        headers={
            "Authorization": f"Bearer {owner_token}",
        },
        json={
            "email": invite_email,
            "role": "member",
        },
    )

    assert second_response.status_code == 409


def test_invitation_to_existing_member():
    owner_token = login("authtest@example.com")
    workspace = create_workspace(owner_token)

    response = client.post(
        f"/api/v1/workspaces/{workspace['id']}/invitations",
        headers={
            "Authorization": f"Bearer {owner_token}",
        },
        json={
            "email": "authtest@example.com",
            "role": "member",
        },
    )

    assert response.status_code == 409


def test_accept_invitation_success():
    owner_token = login("authtest@example.com")
    workspace = create_workspace(owner_token)

    invite_email = f"accept-{uuid4().hex[:8]}@example.com"
    invite_password = "InvitePassword123"

    register_user(
        invite_email,
        f"inviteuser{uuid4().hex[:8]}",
        invite_password,
    )

    invitation_response = client.post(
        f"/api/v1/workspaces/{workspace['id']}/invitations",
        headers={
            "Authorization": f"Bearer {owner_token}",
        },
        json={
            "email": invite_email,
            "role": "member",
        },
    )

    assert invitation_response.status_code == 201

    token = invitation_response.json()["token"]

    invitee_token = login(
        invite_email,
        invite_password,
    )

    response = client.post(
        "/api/v1/workspaces/invitations/accept",
        headers={
            "Authorization": f"Bearer {invitee_token}",
        },
        json={
            "token": token,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Invitation accepted successfully"
    assert data["workspace_id"] == workspace["id"]
    assert data["role"] == "member"


def test_accept_nonexistent_invitation():
    token = login("authtest@example.com")

    response = client.post(
        "/api/v1/workspaces/invitations/accept",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "token": "a" * 20,
        },
    )

    assert response.status_code == 404


def test_accept_invitation_without_token():
    response = client.post(
        "/api/v1/workspaces/invitations/accept",
        json={
            "token": "a" * 20,
        },
    )

    assert response.status_code == 401


def test_accept_invitation_wrong_user():
    owner_token = login("authtest@example.com")
    workspace = create_workspace(owner_token)

    invite_email = f"wrong-user-{uuid4().hex[:8]}@example.com"

    invitation_response = client.post(
        f"/api/v1/workspaces/{workspace['id']}/invitations",
        headers={
            "Authorization": f"Bearer {owner_token}",
        },
        json={
            "email": invite_email,
            "role": "member",
        },
    )

    assert invitation_response.status_code == 201

    invitation_token = invitation_response.json()["token"]

    response = client.post(
        "/api/v1/workspaces/invitations/accept",
        headers={
            "Authorization": f"Bearer {owner_token}",
        },
        json={
            "token": invitation_token,
        },
    )

    assert response.status_code == 403


def test_accept_invitation_invalid_token_format():
    token = login("authtest@example.com")

    response = client.post(
        "/api/v1/workspaces/invitations/accept",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "token": "short",
        },
    )

    assert response.status_code == 422