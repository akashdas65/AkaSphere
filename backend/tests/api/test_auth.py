from uuid import uuid4
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_register_success():
    email = f"authtest_{uuid4().hex[:8]}@example.com"
    username = f"authtest_{uuid4().hex[:8]}"

    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "username": username,
            "full_name": "Auth Test User",
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == email
    assert data["username"] == username
    assert data["full_name"] == "Auth Test User"
    assert data["is_active"] is True
    assert data["is_verified"] is False


def test_register_duplicate_email():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "authtest@example.com",
            "username": "anotheruser",
            "full_name": "Another User",
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 409


def test_register_invalid_email():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "not-an-email",
            "username": "invalidemailuser",
            "full_name": "Invalid Email",
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 422


def test_register_short_password():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "shortpass@example.com",
            "username": "shortpassuser",
            "full_name": "Short Password",
            "password": "123",
        },
    )

    assert response.status_code == 422

def test_login_success():
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "authtest@example.com",
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password():
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "authtest@example.com",
            "password": "WrongPassword123",
        },
    )

    assert response.status_code == 401


def test_login_nonexistent_user():
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "doesnotexist@example.com",
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 401


def test_login_invalid_email():
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "invalid-email",
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 422

def test_get_me_with_valid_token():
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "authtest@example.com",
            "password": "TestPassword123",
        },
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    response = client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "authtest@example.com"
    assert data["username"] == "authtestuser"


def test_get_me_without_token():
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401


def test_get_me_with_invalid_token():
    response = client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": "Bearer invalid-token",
        },
    )

    assert response.status_code == 401

def test_refresh_token_success():
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "authtest@example.com",
            "password": "TestPassword123",
        },
    )

    assert login_response.status_code == 200

    tokens = login_response.json()

    refresh_token = tokens["refresh_token"]

    response = client.post(
        "/api/v1/auth/refresh",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert response.status_code == 200

    new_tokens = response.json()

    assert "access_token" in new_tokens
    assert "refresh_token" in new_tokens
    assert new_tokens["token_type"] == "bearer"

    # Refresh-token rotation:
    assert new_tokens["refresh_token"] != refresh_token


def test_refresh_token_invalid():
    response = client.post(
        "/api/v1/auth/refresh",
        json={
            "refresh_token": "invalid-refresh-token",
        },
    )

    assert response.status_code == 401


def test_logout_success():
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "authtest@example.com",
            "password": "TestPassword123",
        },
    )

    assert login_response.status_code == 200

    refresh_token = login_response.json()["refresh_token"]

    response = client.post(
        "/api/v1/auth/logout",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert response.status_code == 204


def test_refresh_token_after_logout():
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "authtest@example.com",
            "password": "TestPassword123",
        },
    )

    assert login_response.status_code == 200

    refresh_token = login_response.json()["refresh_token"]

    logout_response = client.post(
        "/api/v1/auth/logout",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert logout_response.status_code == 204

    # The revoked refresh token must no longer work.
    refresh_response = client.post(
        "/api/v1/auth/refresh",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert refresh_response.status_code == 401

def test_send_otp_success():
    response = client.post(
        "/api/v1/auth/send-otp",
        json={
            "email": "authtest@example.com",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "OTP generated successfully"
    assert "otp" in data
    assert len(data["otp"]) == 6
    assert data["otp"].isdigit()
    assert data["expires_in"] > 0


def test_send_otp_invalid_email():
    response = client.post(
        "/api/v1/auth/send-otp",
        json={
            "email": "invalid-email",
        },
    )

    assert response.status_code == 422


def test_verify_otp_success():
    send_response = client.post(
        "/api/v1/auth/send-otp",
        json={
            "email": "authtest@example.com",
        },
    )

    assert send_response.status_code == 200

    otp = send_response.json()["otp"]

    response = client.post(
        "/api/v1/auth/verify-otp",
        json={
            "email": "authtest@example.com",
            "otp": otp,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Email verified successfully"
    assert data["email"] == "authtest@example.com"
    assert data["is_verified"] is True


def test_verify_otp_invalid():
    response = client.post(
        "/api/v1/auth/verify-otp",
        json={
            "email": "authtest@example.com",
            "otp": "000000",
        },
    )

    assert response.status_code == 400


def test_verify_otp_invalid_format():
    response = client.post(
        "/api/v1/auth/verify-otp",
        json={
            "email": "authtest@example.com",
            "otp": "123",
        },
    )

    assert response.status_code == 422


def test_forgot_password_success():
    response = client.post(
        "/api/v1/auth/forgot-password",
        json={
            "email": "authtest@example.com",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["message"]
        == "If the email exists, a password reset OTP has been sent."
    )


def test_forgot_password_nonexistent_email():
    response = client.post(
        "/api/v1/auth/forgot-password",
        json={
            "email": "doesnotexist@example.com",
        },
    )

    assert response.status_code == 200

    data = response.json()

    # Same response prevents user enumeration.
    assert (
        data["message"]
        == "If the email exists, a password reset OTP has been sent."
    )

def test_reset_password_success():
    email = "authtest@example.com"

    send_response = client.post(
        "/api/v1/auth/forgot-password",
        json={
            "email": email,
        },
    )

    assert send_response.status_code == 200

    # OTP is printed by the current development implementation,
    # so generate one directly for the test.
    otp_response = client.post(
        "/api/v1/auth/send-otp",
        json={
            "email": email,
        },
    )

    assert otp_response.status_code == 200

    otp = otp_response.json()["otp"]

    response = client.post(
        "/api/v1/auth/reset-password",
        json={
            "email": email,
            "otp": otp,
            "new_password": "NewTestPassword123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Password reset successfully"


def test_login_with_new_password_after_reset():
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "authtest@example.com",
            "password": "NewTestPassword123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_with_old_password_after_reset():
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "authtest@example.com",
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 401


def test_reset_password_invalid_otp():
    response = client.post(
        "/api/v1/auth/reset-password",
        json={
            "email": "authtest@example.com",
            "otp": "000000",
            "new_password": "AnotherPassword123",
        },
    )

    assert response.status_code == 400


def test_reset_password_invalid_email():
    response = client.post(
        "/api/v1/auth/reset-password",
        json={
            "email": "doesnotexist@example.com",
            "otp": "000000",
            "new_password": "AnotherPassword123",
        },
    )

    assert response.status_code == 400


def test_reset_password_short_password():
    response = client.post(
        "/api/v1/auth/reset-password",
        json={
            "email": "authtest@example.com",
            "otp": "123",
            "new_password": "short",
        },
    )

    assert response.status_code == 422