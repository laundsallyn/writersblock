from json import loads as load

from requests import get
from xmltodict import parse


class Request:
    def __init__(self, client, path, query_dict, req_format='xml'):
        """Initialize request object."""
        self.params = dict(**query_dict, **client.query_dict)
        self.host = client.base_url
        self.path = path
        self.req_format = req_format

    def request(self):
        resp = get(self.host + self.path, params=self.params)
        if resp.status_code != 200:
            raise RequestException(resp.reason, self.path)
        if self.req_format == 'xml':
            data_dict = parse(resp.content)
            return data_dict['GoodreadsResponse']
        elif self.req_format == 'json':
            return load(resp.content)
        else:
            raise Exception("Invalid format")
