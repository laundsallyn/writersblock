import requests
import xmltodict
import json
import types

from .exceptions import RequestException, VALID_STATUS_CODES


class Request:
    def __init__(self, client, path, query_dict, req_format='xml'):
        """Initialize request object."""
        self.params = dict(**query_dict, **client.query_dict)
        self.host = client.base_url
        self.path = path
        self.req_format = req_format
        self.response_root = client.response_root

    def call_api(self, method_name, resource, uid, **kwargs):
        # print(self.host+self.path)

        self.session.headers.update(self.get_http_headers(self.Meta.name, method_name))
        url = resource.get_url(url=self.Meta.base_url, resource=resource, uid=uid, **kwargs)
        resp = self.session.get(url=url, **params)

        if resp.status_code not in VALID_STATUS_CODES:
            raise RequestException(resp.reason, self.path)

        return self._handle_response(resp, resource) if resp.content else []

    @staticmethod
    def get_http_headers(client_name, method_name):
        """
        Prepares the HTTP HEADERS and returns them.

        :param client_name: The name of the HTTP client
        :param method_name: The method name triggering this HTTP request.

        :returns: A dictionary of HTTP headers
        """
        return {'X-CLIENT': client_name, 'X-METHOD': method_name, 'content-type': 'application/json'}

    @staticmethod
    def _handle_response(cls, resp, resource):
        """
        Handles Response objects

        :param response: An HTTP reponse object
        :param resource: The resource class to build from this response

        :returns resources: A list of Resource Module instances
        """

        data_dict = cls._extract(resp)

        if isinstance(data_dict, list):
            # A list of results is always rendered
            return [resource(**x) for x in data_dict]

        else:
            # Try and find the paginated resources
            key = getattr(resource.Meta, 'pagination_key', None)

            # Only return the paginated responses
            # Else: Attempt to render this whole response as a resource
            return [resource(**x) for x in data_dict.get(key)] \
                if isinstance(data_dict.get(key), list) \
                else [resource(**data_dict)]


    @staticmethod
    def _extract(self, resp):
        """

        :param response:
        :param resource:
        :return: python dictionary
        """
        return xmltodict.parse(resp.content) \
            if self.req_format == 'xml' \
            else json.loads(resp.content)
