from pydantic import BaseModel


class Address(BaseModel):
    city: str
    zip_code: str


class User(BaseModel):
    id: int
    name: str
    address: Address


user = User(id=1, name="Peter", address=Address(city="Volgograd", zip_code="400112"))
print(user.model_dump_json())
