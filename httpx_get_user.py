import httpx

from tools.fakers import fake


create_payload = {
  "email": get_random_email(),
  "password": "string",
  "lastName": "string",
  "firstName": "string",
  "middleName": "string"
}
create_response = httpx.post("http://127.0.0.1:8000/api/v1/users", json=create_payload)
print(create_response.status_code)
print(create_response.json())

login_payload = {
  "email": create_response.json()['user']['email'],
  "password": "string"
}
login_response = httpx.post("http://127.0.0.1:8000/api/v1/authentication/login", json=login_payload)
print(login_response.status_code)
print(login_response.json())

headers = {f"Authorization": f"Bearer {login_response.json()['token']['accessToken']}"}
get_user_response = httpx.get(f"http://127.0.0.1:8000/api/v1/users/{create_response.json()['user']['id']}",
                              headers=headers)
print(get_user_response.status_code)
print(get_user_response.json())
