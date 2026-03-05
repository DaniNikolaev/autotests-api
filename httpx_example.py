import httpx


# response = httpx.get("https://jsonplaceholder.typicode.com/todos/2")
# print(response.status_code)
# print(response.json())


# data = {
#     "title": "Новая задача",
#     "completed": False,
#     "userId": 1
# }
#
# response = httpx.post("https://jsonplaceholder.typicode.com/todos", json=data)
# print(response.status_code)
# print(response.json())

# data = {"username": "test_user", "password": "123456"}
#
# response = httpx.post("https://httpbin.org/post", json=data)

# params = {"UserId": 2}
# response = httpx.get("https://jsonplaceholder.typicode.com/todos", params=params)
# print(response.status_code)
# print(response.json())
#print(response.headers)


client = httpx.Client(headers={"Authorization": "Bearer my_secret_token"})

response = client.get("https://jsonplaceholder.typicode.com/todos")

print(response.headers)  # Заголовки включены в ответ
client.close()