from unittest import TestCase
from unittest.mock import MagicMock, patch

import requests.exceptions

from module.modules.common import validate_request_response_status, create_document_parser_for_url


class TestCommonFunctionality(TestCase):

    def test_validate_request_response_status__with_response_status_code_403__exit_the_program_with_status_code_1(self):
        mock_response = MagicMock()
        mock_response.status_code = 403

        with self.assertRaises(SystemExit) as cm:
            validate_request_response_status(mock_response)

        self.assertEqual(cm.exception.code, 1)

    def test_validate_request_response_status__with_response_status_code_200__return_none(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        self.assertEqual(None, validate_request_response_status(mock_response))

    @patch('module.modules.common.requests.get')
    def test_create_document_parser_for_url__when_raised_connection_error__exit_program_with_status_code_1(self,
                                                                                                           mock_requests):
        mock_requests.exceptions = requests.exceptions
        mock_requests.side_effect = requests.exceptions.ConnectionError(1)
        with self.assertRaises(SystemExit) as cm:
            create_document_parser_for_url('testUrl')

        self.assertEqual(cm.exception.code, 1)

    @patch('module.modules.common.requests')
    def test_create_document_parser_for_url__return_document_parser(self, mock_request):

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'test data'

        mock_request.get.return_value = mock_response
        result = create_document_parser_for_url('test url')
        self.assertEqual(result.contents[0], 'test data')