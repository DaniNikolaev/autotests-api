from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from clients.errors_schema import ValidationErrorResponseSchema, InternalErrorResponseSchema
from clients.files.files_client import FilesClient
from clients.files.files_schema import CreateFileRequestSchema, CreateFileResponseSchema, GetFileResponseSchema
from config import settings
from fixtures.files import FileFixture
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.files import assert_create_file_response, assert_get_file_response, \
    assert_create_file_with_empty_filename_response, assert_create_file_with_empty_directory_response, \
    assert_get_file_with_incorrect_file_id_response, assert_file_not_found_response
from tools.assertions.schema import validate_json_schema


@pytest.mark.files
@pytest.mark.regression
@allure.tag(AllureTag.FILES, AllureTag.REGRESSION)
@allure.epic(AllureEpic.LMS)
@allure.parent_suite(AllureEpic.LMS)
@allure.feature(AllureFeature.FILES)
@allure.suite(AllureFeature.FILES)
class TestFiles:
    @allure.title("Create file")
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    @allure.severity(Severity.BLOCKER)
    def test_create_file(self, files_client: FilesClient):
        request = CreateFileRequestSchema(upload_file=settings.test_data.image_jpg_file)
        response = files_client.create_file_api(request)
        response_data = CreateFileResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)

        assert_create_file_response(request=request, response=response_data)

        validate_json_schema(response.json(), CreateFileResponseSchema.model_json_schema())

    @allure.title("Get file")
    @allure.story(AllureStory.GET_ENTITY)
    @allure.sub_suite(AllureStory.GET_ENTITY)
    @allure.severity(Severity.CRITICAL)
    def test_get_file(self, files_client: FilesClient, function_file: FileFixture):
        response = files_client.get_file_api(function_file.id)
        response_data = GetFileResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)

        assert_get_file_response(response_data, function_file.response)

        validate_json_schema(response.json(), GetFileResponseSchema.model_json_schema())

    @allure.title("Create file with empty filename")
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    def test_create_file_with_empty_filename(self, files_client: FilesClient):
        request = CreateFileRequestSchema(
            filename="",
            upload_file=settings.test_data.image_jpg_file
        )
        response = files_client.create_file_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

        assert_create_file_with_empty_filename_response(response_data)

        validate_json_schema(response.json(), ValidationErrorResponseSchema.model_json_schema())

    @allure.title("Create file with empty directory")
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    def test_create_file_with_empty_directory(self, files_client: FilesClient):
        request = CreateFileRequestSchema(
            directory="",
            upload_file=settings.test_data.image_jpg_file
        )
        response = files_client.create_file_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

        assert_create_file_with_empty_directory_response(response_data)

        validate_json_schema(response.json(), ValidationErrorResponseSchema.model_json_schema())

    @allure.title("Create file with incorrect file id")
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    def test_create_file_with_incorrect_file_id(self, files_client: FilesClient):
        response = files_client.get_file_api("incorrect-file-id")
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

        assert_get_file_with_incorrect_file_id_response(response_data)

        validate_json_schema(response.json(), ValidationErrorResponseSchema.model_json_schema())

    @allure.title("Delete file")
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    @allure.severity(Severity.NORMAL)
    def test_delete_file(self, files_client: FilesClient, function_file: FileFixture):
        delete_response = files_client.delete_file_api(function_file.id)

        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        get_response = files_client.get_file_api(function_file.id)
        get_response_data = InternalErrorResponseSchema.model_validate_json(get_response.text)
        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)

        assert_file_not_found_response(get_response_data)

        validate_json_schema(get_response.json(), InternalErrorResponseSchema.model_json_schema())
