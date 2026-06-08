from ..api_v1 import API as API
from ..core import File as File, _SerializableObject
from ..errors import ExecutionError as ExecutionError
from _typeshed import Incomplete
from abc import ABC
from typing import Any, ItemsView, Iterator, KeysView

logger: Incomplete
RESULT_CONTENT_NOT_PRESENT: str

class _JobContent(_SerializableObject):
    """
    Container for the input of a Job class instance. Can be instantiated similarly to a dictionary, either with a curly
    braces input ({'key1': value1, 'key2': value2}) or with a kwargs specification (key1=value1, key2=value2)
    """
    def __init__(self, _dict: dict = None, **kwargs: Any) -> None:
        """
        :param _dict:
        :param kwargs:
        """

class _StreamedDict:
    """ Helper class that can be used in ExternalProgram.execute to save the _result_content, so that it can be handled
     both as a dict (backward compatibility), or streamed, to cope with large files. """
    def __init__(self, file: File, encoding: str = 'utf-8') -> None: ...
    @classmethod
    def from_url(cls, url: str, encoding: str = 'utf-8') -> _StreamedDict: ...
    @classmethod
    def from_dict(cls, d: dict, encoding: str = 'utf-8') -> _StreamedDict:
        """ Mainly for testing. """
    @property
    def encoding(self) -> str: ...
    def keys(self) -> KeysView[str]: ...
    def __contains__(self, item: Any) -> bool: ...
    def __getitem__(self, item: str) -> Any: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def items(self) -> ItemsView[str, Any]: ...
    def to_dict(self) -> dict: ...
    def stream_dict_value(self, key: str, *, buffer_size: int = ...) -> Iterator[str]:
        ''' Returns the key value as iterator without loading the content in memory. Assumes key and value to be in
        double quotes according to JSON standard ("key": "value"). Hence, only works if value is of type str and does
        NOT contain \'"\' character!

        :param key: key to get the value from.
        :param buffer_size: number of characters that is returned in a single iterator next call.
        '''
    def get_value_as_file(self, key: str, *, base64_decode: bool = True, decompress: bool = False) -> File | None:
        """ Return the key value as a file without loading the content in memory.

        :param key: key to get the value from.
        :param base64_decode: decode the value with base64 before returning it.
        :param decompress: decompress AND base64-decode the value before returning it.
        """

class ExternalProgram(ABC):
    """
    .. warning:: Do not use this class directly in an application!

    Base-class of an external analysis.
    """
    def __init__(self, queue_name: str, version: int) -> None:
        """
        :param queue_name: Name of the external integration.
        :param version: Version of the API between SDK <-> worker.
        """
    def execute(self, timeout: int = 25) -> None:
        """
        Run method to start an external analysis using a VIKTOR worker.

        .. note:: This method needs to be mocked in (automated) unit and integration tests.

        :param timeout: Timeout period in seconds.

        :raises:
            - TimeoutError when timeout has been exceeded
            - ConnectionError if no worker installed or connected
            - LicenseError if no license is available
            - ExecutionError if the external program cannot execute with the provided inputs
        """

class OAuth2Integration:
    """ ::version(14.23.0)

    Third-party OAuth 2.0 integration.

    Usage:

    .. code-block:: python

        integration = vkt.external.OAuth2Integration('my-oauth2-integration')
        access_token = integration.get_access_token()
        # use access_token to do request on host URL associated with integration 'my-oauth2-integration'
    """
    def __init__(self, name: str) -> None: ...
    def get_access_token(self) -> str:
        """
        Obtain the personal access token

        :raises:
            - PermissionDeniedError: needs login from user
            - ResourceNotFoundError: integration not found
            - PreconditionFailedError: integration not assigned to this app
        """
