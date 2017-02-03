import json
import pprint

import xmltodict
from .exceptions import RequestException, VALID_STATUS_CODES
from .request import Request
import os
import requests
import types


class HTTPClient(object):
    """
    HTTPClient implements calls to python requests through the 'call_api' method.
    """
    @staticmethod
    def get_headers(client_name, method_name):
        """
        Prepares the HTTP HEADERS and returns them.

        :param client_name: The name of the HTTP client
        :param method_name: The method name triggering this HTTP request.

        :returns: A dictionary of HTTP headers
        """
        return {'X-CLIENT': client_name, 'X-METHOD': method_name, 'content-type': 'application/json'}

    def call_api(self, method_name, resource, uid, **kwargs):
        """
        Make HTTP calls.

        :param method_name: python method making the HTTP call
        :param resource: generated resource class
        :param uid: resource unique identifier
        :param kwargs: Additional custom keyword arguments
        """

        self.session.headers.update(self.get_headers(self.Meta.name, method_name))

        url = resource.get_resource_url(resource=resource, base_url=self.Meta.base_url)
        url = resource.get_url(url=url, uid=uid, **kwargs)

        print(url)
        resp = self.session.get(url=url, params=self.query_dict)

        if resp.status_code not in VALID_STATUS_CODES:
            print(resp.reason)
            print(resp.status_code)
            print(resp.headers)
            raise RequestException(resp.reason, url)

        return self._handle_response(resp, resource) if resp.content else []

    def _handle_response(self, resp, resource):
        """
        Handles Response objects

        :param response: An HTTP reponse object
        :param valid_status_codes: A tuple list of valid status codes
        :param resource: The resource class to build from this response

        :returns resources: A list of Resource Module instances
        """

        if "application/xml" in resp.headers['content-type']:
            data_dict = xmltodict.parse(resp.content)
        else:
            data_dict = resp.json() #[resource.Meta.pagination_key]

        #pprint.pprint(data_dict)
        result = []
        if isinstance(data_dict, list):
            # A list of results is always rendered
            result = [resource(**x) for x in data_dict]

        else:
            # Try and find the paginated resources
            key = getattr(resource.Meta, 'pagination_key', None)

            # Only return the paginated responses
            # Else: Attempt to render this whole response as a resource
            result = [resource(**x) for x in data_dict.get(key)] \
                if isinstance(data_dict.get(key), list) \
                else [resource(**data_dict)]
        #pprint.pprint(result)
        return result


class BaseClient(HTTPClient):
    class Meta:
        """
        :var name: The name of this client API
        :var base_url: The base_url for the API of this client.
        :var resources: A list of registered resources
        :var client_key: env mapped to key
        """
        name = NotImplemented
        base_url = NotImplemented
        resources = NotImplemented
        client_key = NotImplemented

    def __init__(self, *args, **kwargs):
        """Initialize the client"""
        super(BaseClient, self).__init__(*args, **kwargs)
        self.assign_resources(self.Meta.resources)
        self.resources = self.Meta.resources
        self._client_key = os.environ.get(self.Meta.client_key)
        self.session = requests.Session()

    def assign_resources(self, resource_class_list):
        """
        Given a tuple of resources.py classes, parse their Meta.methods
        attributes and client methods for communicating with those resources.

        Using reflection, assigns a new GET method to this class.

        :param resource_class_list: A tuple of resources.py classes
        """
        for resource_class in resource_class_list:
            method_name = 'get_{}'.format(resource_class.Meta.name.lower())

            def get(self, method_name=method_name, resource=resource_class, uid=None, **kwargs):
                return self.call_api(method_name, resource, uid=uid, **kwargs)

            setattr(self, method_name, types.MethodType(get, self))

    @property
    def query_dict(self):
        return {'api-key': self._client_key}
