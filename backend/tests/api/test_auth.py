from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


TEST_PASSWORD = "TestPassword123"
NEW_PASSWORD = "NewTestPassword123"


def create_test_user():
    """
    Create a unique test user.
    This prevents tests from depending on database state
    created by previous test runs.
    """
    suffix = uuid4().hex[:8]

    email = f"authtest_{suffix}@example.com"
    username = f"authtest_{suffix}"

    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "username": username,
            "full_name": "Auth Test User",
            "password": TEST_PASSWORD,
        },
    )

    assert response.status_code == 201

    return {
        "email": email,
        "username": username,
    }


def register_user(
    email: str,
    username: str,
    password: str = TEST_PASSWORD,
):
    return client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "username": username,
            "full_name": "Auth Test User",
            "password": password,
        },
    )


def login(
    email: str,
    password: str = TEST_PASSWORD,
):
    return client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )


# ============================================================
# REGISTER
# ============================================================


def test_register_success():
    suffix = uuid4().hex[:8]

    email = f"register_{suffix}@example.com"
    username = f"register_{suffix}"

    response = register_user(
        email=email,
        username=username,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == email
    assert data["username"] == username
    assert data["full_name"] == "Auth Test User"
    assert data["is_active"] is True
    assert data["is_verified"] is False


def test_register_duplicate_email():
    user = create_test_user()

    response = register_user(
        email=user["email"],
        username=f"another_{uuid4().hex[:8]}",
    )

    assert response.status_code == 409


def test_register_invalid_email():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "not-an-email",
            "username": f"invalid_{uuid4().hex[:8]}",
            "full_name": "Invalid Email",
            "password": TEST_PASSWORD,
        },
    )

    assert response.status_code == 422


def test_register_short_password():
    suffix = uuid4().hex[:8]

    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": f"shortpass_{suffix}@example.com",
            "username": f"shortpass_{suffix}",
            "full_name": "Short Password",
            "password": "123",
        },
    )

    assert response.status_code == 422


# ============================================================
# LOGIN
# ============================================================


def test_login_success():
    user = create_test_user()

    response = login(
        email=user["email"],
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password():
    user = create_test_user()

    response = login(
        email=user["email"],
        password="WrongPassword123",
    )

    assert response.status_code == 401


def test_login_nonexistent_user():
    response = login(
        email=f"doesnotexist_{uuid4().hex[:8]}@example.com",
        password=TEST_PASSWORD,
    )

    assert response.status_code == 401


def test_login_invalid_email():
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "invalid-email",
            "password": TEST_PASSWORD,
        },
    )

    assert response.status_code == 422


# ============================================================
# GET ME
# ============================================================


def test_get_me_with_valid_token():
    user = create_test_user()

    login_response = login(
        email=user["email"],
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

    assert data["email"] == user["email"]
    assert data["username"] == user["username"]


def test_get_me_without_token():
    response = client.get(
        "/api/v1/auth/me",
    )

    assert response.status_code == 401


def test_get_me_with_invalid_token():
    response = client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": "Bearer invalid-token",
        },
    )

    assert response.status_code == 401


# ============================================================
# REFRESH TOKEN
# ============================================================


def test_refresh_token_success():
    user = create_test_user()

    login_response = login(
        email=user["email"],
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

    assert new_tokens["refresh_token"] != refresh_token


def test_refresh_token_invalid():
    response = client.post(
        "/api/v1/auth/refresh",
        json={
            "refresh_token": "invalid-refresh-token",
        },
    )

    assert response.status_code == 401


# ============================================================
# LOGOUT
# ============================================================


def test_logout_success():
    user = create_test_user()

    login_response = login(
        email=user["email"],
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
    user = create_test_user()

    login_response = login(
        email=user["email"],
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

    refresh_response = client.post(
        "/api/v1/auth/refresh",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert refresh_response.status_code == 401


# ============================================================
# SEND OTP
# ============================================================


def test_send_otp_success():
    user = create_test_user()

    response = client.post(
        "/api/v1/auth/send-otp",
        json={
            "email": user["email"],
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


# ============================================================
# VERIFY OTP
# ============================================================


def test_verify_otp_success():
    user = create_test_user()

    send_response = client.post(
        "/api/v1/auth/send-otp",
        json={
            "email": user["email"],
        },
    )

    assert send_response.status_code == 200

    otp = send_response.json()["otp"]

    response = client.post(
        "/api/v1/auth/verify-otp",
        json={
            "email": user["email"],
            "otp": otp,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Email verified successfully"
    assert data["email"] == user["email"]
    assert data["is_verified"] is True


def test_verify_otp_invalid():
    user = create_test_user()

    response = client.post(
        "/api/v1/auth/verify-otp",
        json={
            "email": user["email"],
            "otp": "000000",
        },
    )

    assert response.status_code == 400


def test_verify_otp_invalid_format():
    user = create_test_user()

    response = client.post(
        "/api/v1/auth/verify-otp",
        json={
            "email": user["email"],
            "otp": "123",
        },
    )

    assert response.status_code == 422


# ============================================================
# FORGOT PASSWORD
# ============================================================


def test_forgot_password_success():
    user = create_test_user()

    response = client.post(
        "/api/v1/auth/forgot-password",
        json={
            "email": user["email"],
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
            "email": f"doesnotexist_{uuid4().hex[:8]}@example.com",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["message"]
        == "If the email exists, a password reset OTP has been sent."
    )


# ============================================================
# RESET PASSWORD
# ============================================================


def test_reset_password_success():
    user = create_test_user()

    send_response = client.post(
        "/api/v1/auth/send-otp",
        json={
            "email": user["email"],
        },
    )

    assert send_response.status_code == 200

    otp = send_response.json()["otp"]

    response = client.post(
        "/api/v1/auth/reset-password",
        json={
            "email": user["email"],
            "otp": otp,
            "new_password": NEW_PASSWORD,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Password reset successfully"


def test_login_with_new_password_after_reset():
    user = create_test_user()

    send_response = client.post(
        "/api/v1/auth/send-otp",
        json={
            "email": user["email"],
        },
    )

    assert send_response.status_code == 200

    otp = send_response.json()["otp"]

    reset_response = client.post(
        "/api/v1/auth/reset-password",
        json={
            "email": user["email"],
            "otp": otp,
            "new_password": NEW_PASSWORD,
        },
    )

    assert reset_response.status_code == 200

    response = login(
        email=user["email"],
        password=NEW_PASSWORD,
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_with_old_password_after_reset():
    user = create_test_user()

    send_response = client.post(
        "/api/v1/auth/send-otp",
        json={
            "email": user["email"],
        },
    )

    assert send_response.status_code == 200

    otp = send_response.json()["otp"]

    reset_response = client.post(
        "/api/v1/auth/reset-password",
        json={
            "email": user["email"],
            "otp": otp,
            "new_password": NEW_PASSWORD,
        },
    )

    assert reset_response.status_code == 200

    response = login(
        email=user["email"],
        password=TEST_PASSWORD,
    )

    assert response.status_code == 401


def test_reset_password_invalid_otp():
    user = create_test_user()

    response = client.post(
        "/api/v1/auth/reset-password",
        json={
            "email": user["email"],
            "otp": "000000",
            "new_password": "AnotherPassword123",
        },
    )

    assert response.status_code == 400


def test_reset_password_invalid_email():
    response = client.post(
        "/api/v1/auth/reset-password",
        json={
            "email": f"doesnotexist_{uuid4().hex[:8]}@example.com",
            "otp": "000000",
            "new_password": "AnotherPassword123",
        },
    )

    assert response.status_code == 400


def test_reset_password_short_password():
    user = create_test_user()

    response = client.post(
        "/api/v1/auth/reset-password",
        json={
            "email": user["email"],
            "otp": "123",
            "new_password": "short",
        },
    )

    assert response.status_code == 422

# ============================================================
# TOKEN SECURITY
# ============================================================


def test_access_token_cannot_be_used_as_refresh_token():
    user = create_test_user()

    login_response = login(
        email=user["email"],
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    response = client.post(
        "/api/v1/auth/refresh",
        json={
            "refresh_token": access_token,
        },
    )

    assert response.status_code == 401


def test_refresh_token_cannot_be_used_as_access_token():
    user = create_test_user()

    login_response = login(
        email=user["email"],
    )

    assert login_response.status_code == 200

    refresh_token = login_response.json()["refresh_token"]

    response = client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": f"Bearer {refresh_token}",
        },
    )

    assert response.status_code == 401


def test_old_refresh_token_cannot_be_reused_after_rotation():
    user = create_test_user()

    login_response = login(
        email=user["email"],
    )

    assert login_response.status_code == 200

    old_refresh_token = login_response.json()["refresh_token"]

    refresh_response = client.post(
        "/api/v1/auth/refresh",
        json={
            "refresh_token": old_refresh_token,
        },
    )

    assert refresh_response.status_code == 200

    new_refresh_token = refresh_response.json()["refresh_token"]

    assert new_refresh_token != old_refresh_token

    reuse_response = client.post(
        "/api/v1/auth/refresh",
        json={
            "refresh_token": old_refresh_token,
        },
    )

    assert reuse_response.status_code == 401


def test_logout_revokes_refresh_token():
    user = create_test_user()

    login_response = login(
        email=user["email"],
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

    refresh_response = client.post(
        "/api/v1/auth/refresh",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert refresh_response.status_code == 401


def test_tampered_refresh_token_is_rejected():
    user = create_test_user()

    login_response = login(
        email=user["email"],
    )

    assert login_response.status_code == 200

    refresh_token = login_response.json()["refresh_token"]

    tampered_token = refresh_token[:-1] + (
        "x"
        if refresh_token[-1] != "x"
        else "y"
    )

    response = client.post(
        "/api/v1/auth/refresh",
        json={
            "refresh_token": tampered_token,
        },
    )

    assert response.status_code == 401