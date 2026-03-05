import pytest
import allure
from http import HTTPStatus

from allure_commons.types import Severity

from clients.errors_schema import InternalErrorResponseSchema
from clients.users.private_users_client import PrivateUsersClient
from clients.users.public_users_client import PublicUsersClient
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema, \
    UpdateUserRequestSchema, UpdateUserResponseSchema
from fixtures.users import UserFixture
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.users import assert_create_user_response, assert_get_user_response, assert_update_user_response, \
    assert_user_not_found_response
from tools.fakers import fake


@pytest.mark.users
@pytest.mark.regression
@allure.tag(AllureTag.USERS, AllureTag.REGRESSION)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.USERS)
class TestUsers:
    @allure.title("Create user")
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.severity(Severity.BLOCKER)
    @pytest.mark.parametrize('email', ['mail.ru', 'gmail.com', 'example.com'])
    def test_create_user(self, public_users_client: PublicUsersClient, email: str):
        request = CreateUserRequestSchema(email=fake.email(domain=email))
        print(request.email, request.password)
        response = public_users_client.create_user_api(request)
        response_data = CreateUserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)

        assert_create_user_response(request, response_data)

        validate_json_schema(response.json(), CreateUserResponseSchema.model_json_schema())

    @allure.title("Update user")
    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    def test_update_user(self, private_users_client: PrivateUsersClient, function_user: UserFixture):
        request = UpdateUserRequestSchema()
        response = private_users_client.update_user_api(user_id=function_user.id,
                                                        request=request)
        response_data = UpdateUserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)

        assert_update_user_response(request, response_data)

        validate_json_schema(response.json(), UpdateUserResponseSchema.model_json_schema())

    @allure.title("Get user me")
    @allure.tag(AllureTag.GET_ENTITY)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.severity(Severity.CRITICAL)
    def test_get_user_me(self, private_users_client: PrivateUsersClient, function_user: UserFixture):
        response = private_users_client.get_user_me_api()
        response_data = GetUserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)

        assert_get_user_response(response_data, function_user.response)

        validate_json_schema(response.json(), GetUserResponseSchema.model_json_schema())

    @allure.title("Get user")
    @allure.tag(AllureTag.GET_ENTITY)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.severity(Severity.CRITICAL)
    def test_get_user(self, private_users_client: PrivateUsersClient, function_user: UserFixture):
        response = private_users_client.get_user_api(user_id=function_user.id)
        response_data = GetUserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)

        assert_get_user_response(response_data, function_user.response)

        validate_json_schema(response.json(), GetUserResponseSchema.model_json_schema())

    @allure.title("Delete user")
    @allure.tag(AllureTag.DELETE_ENTITY)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.severity(Severity.NORMAL)
    def test_delete_user(self,
                         public_users_client: PublicUsersClient,
                         private_users_client: PrivateUsersClient
                         ):
        create_request = CreateUserRequestSchema()
        create_response = public_users_client.create_user_api(create_request)
        create_response_data = CreateUserResponseSchema.model_validate_json(create_response.text)
        assert_status_code(create_response.status_code, HTTPStatus.OK)

        delete_response = private_users_client.delete_user_api(user_id=create_response_data.user.id)

        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        get_response = private_users_client.get_user_api(user_id=create_response_data.user.id)
        get_response_data = InternalErrorResponseSchema.model_validate_json(get_response.text)

        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)

        assert_user_not_found_response(get_response_data)

        validate_json_schema(get_response.json(), InternalErrorResponseSchema.model_json_schema())
