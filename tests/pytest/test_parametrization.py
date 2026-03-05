import pytest
from _pytest.fixtures import SubRequest


@pytest.mark.parametrize("number", [1, 2, 3, -1])
def test_number(number):
    assert number > 0


@pytest.mark.parametrize("number, expected", [(1, 1), (2, 8), (3, 27), (-1, -1)])
def test_several_numbers(number, expected):
    assert number ** 3 == expected


@pytest.mark.parametrize("os", ["macos", "windows", "linux", "debian"])  # Параметризируем по операционной системе
@pytest.mark.parametrize("host", [
    "https://dev.company.com",
    "https://stable.company.com",
    "https://prod.company.com"
])
def test_multiplication_of_numbers(os: str, host: str):
    assert len(os + host) > 0


@pytest.fixture(params=[
    "https://dev.company.com",
    "https://test.company.com",
    "https://stage.company.com",
    "https://company.com"
])
def host(request: SubRequest) -> str:
    return request.param


def test_host(host: str):
    print(f'Running test on host: {host}')


# Для тестовых классов параметризация указывается для самого класса
@pytest.mark.parametrize("user", ["Alice", "Zara"])
class TestOperations:
    # Параметр "user" передается в качестве аргумента в каждый тестовый метод класса
    def test_user_with_operations(self, user: str):
        print(f"User with operations: {user}")

    # Аналогично тут передается "user"
    def test_user_without_operations(self, user: str):
        print(f"User without operations: {user}")


test_users = {
    "+70000000011": "User with money on bank account",
    "+70000000022": "User without money on bank account",
    "+70000000033": "User with operations on bank account"
}


@pytest.mark.parametrize(
    'phone_number',
    test_users.keys(),
    ids=lambda phone_number: f'{phone_number}: {test_users[phone_number]}'
)
def test_identifiers(phone_number: str):
    pass
