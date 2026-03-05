import httpx


login_payload = {
  "email": "ttt@ttt.com",
  "password": "ttt"
}

login_response = httpx.post("http://127.0.0.1:8000/api/v1/authentication/login", json=login_payload)
print(login_response.json())
print(login_response.status_code)

headers = {"Authorization": f"Bearer {login_response.json()['token']['accessToken']}"}
users_me_response = httpx.get("http://127.0.0.1:8000/api/v1/users/me", headers=headers)
print(users_me_response.json())
print(users_me_response.status_code)
