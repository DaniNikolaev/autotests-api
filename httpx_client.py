import httpx

login_payload = {
    "email": "ttt@ttt.com",
    "password": "ttt"
}
login_response = httpx.post("http://localhost:8000/api/v1/authentication/login", json=login_payload)
login_response_data = login_response.json()
print(login_response_data)

headers = {"Authorization": f"Bearer {login_response_data['token']['accessToken']}"}
client = httpx.Client(base_url="http://127.0.0.1:8000/",
                      timeout=15,
                      headers=headers)

get_user_me_response = client.get("/api/v1/users/me")
get_user_me_response_data = get_user_me_response.json()
print('Get user me data:', get_user_me_response_data)
