from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from clients.authentication.authentication_client import AuthenticationClient
from clients.authentication.authentication_schema import LoginRequestSchema, LoginResponseSchema, RefreshRequestSchema, \
    RefreshResponseSchema
from clients.users.public_users_client import PublicUsersClient
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema
from fixtures.users import UserFixture
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.authentication import assert_login_response, assert_refresh_token_response
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema


@pytest.mark.authentication
@pytest.mark.regression
@allure.tag(AllureTag.AUTHENTICATION, AllureTag.REGRESSION)
@allure.epic(AllureEpic.LMS)
@allure.parent_suite(AllureEpic.LMS)
@allure.feature(AllureFeature.AUTHENTICATION)
@allure.suite(AllureFeature.AUTHENTICATION)
class TestAuthentication:
    @allure.title("Login with correct email and password")
    @allure.story(AllureStory.LOGIN)
    @allure.sub_suite(AllureStory.LOGIN)
    @allure.severity(Severity.BLOCKER)
    def test_success_authentication(self,
                                    function_user: UserFixture,
                                    authentication_client: AuthenticationClient):
        request = LoginRequestSchema(
            email=function_user.email,
            password=function_user.password
        )
        response = authentication_client.login_api(request)
        response_data = LoginResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)

        validate_json_schema(response.json(), LoginResponseSchema.model_json_schema())

        assert_login_response(response_data)

    @allure.title("Successful refresh token")
    @allure.story(AllureStory.REFRESH_TOKEN)
    @allure.sub_suite(AllureStory.REFRESH_TOKEN)
    @allure.severity(Severity.CRITICAL)
    @pytest.mark.skip(reason="Feature in development")
    def test_refresh_token(self,
                           public_users_client: PublicUsersClient,
                           function_user: UserFixture,
                           authentication_client: AuthenticationClient):
        create_request = CreateUserRequestSchema()
        create_response = public_users_client.create_user_api(create_request)
        CreateUserResponseSchema.model_validate_json(create_response.text)
        assert_status_code(create_response.status_code, HTTPStatus.OK)

        login_request = LoginRequestSchema(
            email=create_request.email,
            password=create_request.password
        )
        login_response = authentication_client.login_api(login_request)
        login_response_data = LoginResponseSchema.model_validate_json(login_response.text)
        assert_status_code(login_response.status_code, HTTPStatus.OK)

        refresh_request = RefreshRequestSchema(refresh_token=login_response_data.token.refresh_token)
        refresh_response = authentication_client.refresh_api(refresh_request)
        refresh_response_data = RefreshResponseSchema.model_validate_json(refresh_response.text)

        assert_status_code(refresh_response.status_code, HTTPStatus.OK)

        assert_refresh_token_response(refresh_response_data)

        validate_json_schema(refresh_response.json(), RefreshResponseSchema.model_json_schema())
