# -*- coding: utf-8 -*-

import types
from urllib.parse import urlparse

import requests

from .clients import HTTPClient


class BaseResource(object):
    """
    @class Representation of a REST API resource.
    """

    class Meta:
        """

        name: Resource name (__str__).
        resource_name: target-url name, i.e. 'resources'
        identifier: Uniquely identifying key
        attributes: desired displayed attributes
        pagination_key: key to render instances of paginated results
        """
        name = 'Resource'
        resource_name = None
        identifier = 'id'
        attributes = (identifier,)
        pagination_key = 'results'

    def __init__(self, **kwargs):
        self.set_attributes(**kwargs)

    def __str__(self):
        """
        Returns name and indexed uid
        """
        return '<{} | {}>'.format(self.Meta.name, getattr(self, self.Meta.identifier))

    def set_attributes(self, **kwargs):
        """
        Set the resource attributes from the kwargs.

        :argument: Keyword arguments passed into the init of this class

        """
        for field, value in kwargs.items():
            if field in self.Meta.attributes:
                setattr(self, field, value)

    @classmethod
    def get_resource_url(cls, resource, base_url):
        """
        Construct the URL for talking to this resource.

        :arg resource: The resource class instance
        :arg base_url: The Base URL of this API service.

        :returns resource_url: The URL for this resource
        """

        url = '{}/{}'.format(base_url, resource.Meta.resource_name)
        return cls._parse_url_and_validate(url)

    @classmethod
    def get_url(cls, url, uid, **kwargs):
        """
        Construct the URL for talking to an individual resource.

        http://myapi.com/api/resource/1

        Args:
            url: The url for this resource
            uid: The unique identifier for an individual resource
            kwargs: Additional keyword argueents
        returns:
            final_url: The URL for this individual resource
        """

        if uid:
            url = '{}/{}'.format(url, uid)

        return cls._parse_url_and_validate(url)

    @classmethod
    def _parse_url_and_validate(cls, url):
        """
        Validates URL string using urlparse.

        :arg url: A URL string
        :returns parsed_url: A validated URL
        :raises BadURLException:
        """
        parsed_url = urlparse(url)
        if parsed_url.scheme and parsed_url.netloc:
            return parsed_url.geturl()
        else:
            return None


class HypermediaResource(BaseResource, HTTPClient):
    """
    HypermediaResource extends BaseResource through
        understanding relationship URLs from attributes to related registered resources.

    :extends BaseResource:
    :extends HTTPClient:
    """

    class Meta(BaseResource.Meta):
        # HypermediaResource requires a base_url attribute
        base_url = NotImplemented
        related_resources = ()

    def __init__(self, *args, **kwargs):
        super(HypermediaResource, self).__init__(*args, **kwargs)
        self.session = requests.Session()

    def set_related_method(self, resource):
        """
        Generate and return the related GET method using reflection.
        """
        method_name = 'get_{}'.format(resource.Meta.name.lower())

        def get(self, method_type='GET', method_name=method_name,
                resource=resource, data=None, uid=None, **kwargs):
            return self.call_api(
                    method_type, method_name, resource,
                    data, uid=uid, **kwargs)

        setattr(self, method_name, types.MethodType(get, self))

    def match_urls_to_resources(self, url_values):
        """
        For the list of related resources, and the list of
        valid URLs, try and match them up.

        If they match, assign a method to this class.

        Args:
        :arg url_values: A dictionary of keys and URL strings that
                        could be related resources.
        :returns: The values that are valid
        """
        return {
            idx: urls
            for resource in self.Meta.related_resources
            for idx, urls in url_values.items()
            if self.match(resource, urls)
            }

    def match(self, resource, urls):
        if resource.get_resource_url(resource, resource.Meta.base_url) in urls:
            self.set_related_method(resource)
            return True

        return False

    def set_attributes(self, **kwargs):
        """
        Overrides BaseResource.set_attributes;
            additionally attempts to:
                match URL strings with related resources then
                build their get_* method and attach it to this resource.
        """
        if not self.Meta.related_resources:
            super(HypermediaResource, self).set_attributes(**kwargs)

        # Extract URL values
        url_values = {k: self._parse_url_and_validate(v) for k, v in kwargs.items()}

        # Assign the valid method values
        assigned_values = self.match_urls_to_resources(url_values)
        [kwargs.pop(k, None) for k in assigned_values.keys()]

        # Assign the rest as attributes.
        [setattr(self, field, value)
         for field, value in kwargs.items()
         if field in self.Meta.attributes]
