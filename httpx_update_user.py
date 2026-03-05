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
  "email": create_payload["email"],
  "password": create_payload["password"]
}
login_response = httpx.post("http://127.0.0.1:8000/api/v1/authentication/login", json=login_payload)
print(login_response.status_code)
print(login_response.json())

headers = {"Authorization": f"Bearer {login_response.json()['token']['accessToken']}"}
update_payload = {
  "email": get_random_email(),
  "lastName": "string1",
  "firstName": "string1",
  "middleName": "string1"
}
update_response = httpx.patch(f"http://127.0.0.1:8000/api/v1/users/{create_response.json()['user']['id']}",
                              headers=headers,
                              json=update_payload
                              )
print(update_response.status_code)
print(update_response.json())
