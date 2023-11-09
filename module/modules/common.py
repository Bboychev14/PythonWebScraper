from bs4 import BeautifulSoup
import requests
import sys


def validate_request_response_status(response_to_validate):
    """
    Validate that the response from the server is 200(ok).
    If not response == 200, we print msg and exit the whole program.
    :param response_to_validate: The response from the server when we make some request
    """
    response_status_code = response_to_validate.status_code
    if response_status_code != 200:
        print(f'Server status code {response_status_code}')
        return sys.exit(1)


def create_document_parser_for_url(url_to_request_to):
    """
    Creates request to the server and if the response is ok create and returns document parser.
    :param url_to_request_to: The url that we are making get request
    :return BeautifulSoup parser
    """
    try:
        response = requests.get(url_to_request_to)
    except requests.exceptions.ConnectionError:
        print('Can"t connect to the server')
        return sys.exit(1)

    validate_request_response_status(response)
    document_parser = BeautifulSoup(response.content.decode(encoding='UTF-8', errors='ignore'), 'html.parser')
    return document_parser
