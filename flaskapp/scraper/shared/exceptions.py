from requests import codes


VALID_STATUS_CODES = (
    codes.ok,  # 200
    codes.created,  # 201
    codes.no_content,  # 204
)


class InvalidStatusCodeError(Exception):

    def __init__(self, sc, exp):
        self.sc = sc
        self.exp = exp

    def __str__(self):
        return "Received status code: {}, expected: {}".format(self.sc, self.exp)


class RequestException(Exception):
    """ An invalid status code was returned for this resource """
    def __init__(self, error_msg, url):
        self.error_msg = error_msg
        self.url = url

    def __str__(self):
        return self.url, ':', self.error_msg


class ClientException(Exception):
    def __init__(self, error_msg):
        self.error_msg = error_msg

    def __str__(self):
        return self.error_msg


class BadURLException(ClientException):
    """ An Invalid URL was parsed """


class MissingUidException(ClientException):
    """ A uid attribute was missing! """
