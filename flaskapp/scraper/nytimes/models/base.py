from pprint import pformat


class BaseModel:
    def __init__(self, results_dict, client):
        self._results_dict = results_dict
        self._client = client

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}
        for attr, _ in self.swagger_types:
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                        lambda x: x.to_dict()
                        if hasattr(x, "to_dict") else x, value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())
