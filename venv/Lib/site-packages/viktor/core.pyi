import abc
import dataclasses
import os
import requests
import types
from .api_v1 import Entity
from .parametrization import Parametrization
from .views import Summary
from _typeshed import Incomplete
from abc import ABC, ABCMeta, abstractmethod
from collections import OrderedDict
from enum import Enum
from requests.adapters import HTTPAdapter, Retry
from requests_toolbelt import MultipartEncoder
from typing import Any, BinaryIO, Callable, IO, Iterable, NamedTuple, Sequence, TextIO

__all__ = ['Color', 'Controller', 'ViktorController', 'File', 'InitialEntity', 'ParamsFromFile', 'progress_message', 'Storage', 'UserMessage']

@dataclasses.dataclass
class _EntityTypeSettings:
    section_expansion_setting: str

class _Result(ABC, metaclass=abc.ABCMeta):
    """ Base class for view and button results """

class UserMessage:
    ''' ::version(v14.0.0)

    A non-breaking message that is shown to the user in the web-interface.

    Example usage:

    .. code-block:: python

        vkt.UserMessage.warning("Show this warning")
        vkt.UserMessage.info("Show this info")
        vkt.UserMessage.success("Analysis successfully finished!")
    '''
    class _MessageType(Enum):
        SUCCESS: UserMessage._MessageType
        INFO: UserMessage._MessageType
        WARNING: UserMessage._MessageType
    @classmethod
    def warning(cls, message: str) -> None:
        """ Show a warning message to the user. """
    @classmethod
    def info(cls, message: str) -> None:
        """ Show an info message to the user. """
    @classmethod
    def success(cls, message: str) -> None:
        """ Show a success message to the user. """

class _SSLContextAdapter(HTTPAdapter):
    """ HTTPAdapter for requests that allows for injecting SSLContext into the lower-level urllib3.PoolManager.

    We are loading the system certificates instead of requests' default certificates
    to resolve SSL cert verification errors when using self-signed certificates.
    """
    def __init__(self, max_retries: Retry = None) -> None: ...
    def init_poolmanager(self, *args: Any, **kwargs: Any) -> None: ...

class _Session(requests.Session):
    """ Wrapper around requests Session which allows for mounting custom SSL context adapters. """
    def __init__(self, with_retries: bool) -> None: ...

class _Context:
    """ Helper class for sdk wide variables, to prevent using global variables or passing through a lot of functions.

    Not for use in app, only VIKTOR SDK internal!
    Also don't make an instance, call from class.
    """
    job_token: Incomplete
    workspace_id: int
    entity_id: int | None
    api_local_cache: OrderedDict
    temp_files: list[str]
    session: requests.Session
    session_with_retries: requests.Session
    @staticmethod
    def clear() -> None: ...

class _OrderedClass(type):
    __fields__: list
    @classmethod
    def __prepare__(mcs, name, bases): ...
    def __new__(cls, name, bases, classdict): ...

class InitialEntity:
    def __init__(self, entity_type_name: str, name: str, *, params: dict | str = None, children: list['InitialEntity'] = None, show_on_dashboard: bool = None, use_as_start_page: bool = None) -> None:
        ''' Construct an initial entity in the `app.__init__py` file.

        .. code-block:: python

            import viktor as vkt

            from .settings_database.controller import Controller as SettingsDatabaseController
            from .project_folder.controller import Controller as ProjectFolderController
            from .project.controller import Controller as ProjectController

            initial_entities = [
                vkt.InitialEntity(\'SettingsDatabase\', name=\'Settings\', params=...),
                vkt.InitialEntity(\'ProjectFolder\', name=\'Projects\', children=[
                    vkt.InitialEntity(\'Project\', \'Project X),
                    vkt.InitialEntity(\'Project\', \'Project Y),
                ]),
            ]

        :param entity_type_name: Type of the initial entity.
        :param name: Name of the initial entity.
        :param params: Optional params in dictionary format or path to a .json, relative to the app.__init__.py. Note
                       that path traversal (beyond the root directory) is not permitted (e.g. "../../entity.json").
        :param children: Optional child entities.
        :param show_on_dashboard: Show/hide the entity on the dashboard. Only top-level entities can be shown
         (default: True) ::version(v13.7.0)
        :param use_as_start_page: Appoint the entity as the start page (instead of the dashboard). Only top-level
         entities can be appointed (default: False) ::version(v14.19.0)
        '''

class ParamsFromFile:
    """ Decorator that can be used on a pre-process method during a file upload, to produce the parameter set that is
    stored in the database.

    .. warning:: Prevent storing the complete file content on the properties if the file is large, as this may cause
      speed and/or stability issues. The file content can be retrieved at all times using the API whenever necessary.

    Example with nothing to store:

    .. code-block:: python

        class Controller(vkt.Controller):
            ...

            @vkt.ParamsFromFile(...)
            def process_file(self, file: vkt.File, **kwargs):
                return {}

    Example with parameters to store:

    .. code-block:: python

        class Controller(vkt.Controller):
            ...

            @vkt.ParamsFromFile(...)
            def process_file(self, file: vkt.File, **kwargs):
                # app specific parsing logic
                file_content = file.getvalue()  # or use reading in chunks, for large files
                number_of_entries = ...
                project_name = ...

                # linking the parsed output to the parametrization fields (names in database)
                return {
                    'tab': {
                        'section': {
                            'number_of_entries': number_of_entries,
                            'project_name': project_name
                        }
                    }
                }

    .. warning:: Loading the content of a large file in memory (`file.getvalue()`) may cause the app to crash
      (out-of-memory). Read the file content in chunks to avoid such memory issues (see :class:`File`).

    .. note:: :meth:`viktor.testing.mock_ParamsFromFile` can be used to test methods decorated with ParamsFromFile.
    """
    def __init__(self, *, max_size: int = None, file_types: Sequence[str] = None) -> None:
        """
        :param max_size: optional restriction on file size in bytes (e.g. 10_000_000 = 10 MB).
        :param file_types: optional restriction on file type(s) (e.g. ['.png', '.jpg', '.jpeg']).
                           Note that the extensions are filtered regardless of capitalization.
        """
    def __call__(self, process_method: Callable) -> Callable: ...

class Controller(metaclass=_OrderedClass):
    '''
    The main function of the ViktorController is to "control" the information flow between the frontend (what is
    inputted by a user) and the application code (what is returned as a result of the user input).

    **(new in v14.15.0)** The \'label\' attribute is now optional.
    '''
    label: str | None
    children: list[str] | None
    show_children_as: str | None
    allow_saving: bool | None
    summary: Summary | None
    parametrization: Parametrization | None
    def __init__(self, **kwargs: Any) -> None: ...
ViktorController = Controller

class _File(ABC, metaclass=abc.ABCMeta):
    def __init__(self, stream: IO) -> None: ...
    def close(self) -> None: ...
    @property
    def closed(self) -> bool: ...
    def fileno(self) -> int: ...
    def flush(self) -> None: ...
    def isatty(self) -> bool: ...
    @property
    def mode(self) -> str: ...
    @property
    def name(self) -> str: ...
    def readable(self) -> bool: ...
    def seek(self, offset: int, whence: int = ...) -> int: ...
    def seekable(self) -> bool: ...
    def tell(self) -> int: ...
    def truncate(self, size: int | None = None) -> int: ...
    def writable(self) -> bool: ...

class _TextFile(_File, TextIO, ABC, metaclass=abc.ABCMeta):
    def read(self, n: int = -1) -> str: ...
    def readline(self, limit: int = -1) -> str: ...
    def readlines(self, hint: int = -1) -> list[str]: ...
    def write(self, s: str) -> int: ...
    def writelines(self, lines: Iterable[str]) -> None: ...
    def __enter__(self) -> TextIO: ...
    def __exit__(self, t: type[BaseException] | None, value: BaseException | None, traceback: types.TracebackType | None) -> None: ...
    def __iter__(self) -> _TextFile: ...
    def __next__(self) -> str: ...
    @property
    def newlines(self) -> None: ...
    @property
    def buffer(self) -> BinaryIO: ...
    @property
    def encoding(self) -> str: ...
    @property
    def errors(self) -> str | None: ...
    @property
    def line_buffering(self) -> int: ...

class _BinaryFile(_File, BinaryIO, ABC, metaclass=abc.ABCMeta):
    def read(self, n: int = -1) -> bytes: ...
    def readline(self, limit: int = -1) -> bytes: ...
    def readlines(self, hint: int = -1) -> list[bytes]: ...
    def write(self, s: bytes | bytearray) -> int: ...
    def writelines(self, lines: Iterable[bytes]) -> None: ...
    def __enter__(self) -> BinaryIO: ...
    def __exit__(self, t: type[BaseException] | None, value: BaseException | None, traceback: types.TracebackType | None) -> None: ...
    def __iter__(self) -> _BinaryFile: ...
    def __next__(self) -> bytes: ...

class _TextDataFile(_TextFile):
    def __init__(self, data: str) -> None: ...
    def getvalue(self) -> str: ...

class _BinaryDataFile(_BinaryFile):
    def __init__(self, data: bytes) -> None: ...
    def getvalue(self) -> bytes: ...

class _TextPathFile(_TextFile):
    def __init__(self, path: str | bytes | os.PathLike, encoding: str = None) -> None: ...

class _BinaryPathFile(_BinaryFile):
    def __init__(self, path: str | bytes | os.PathLike) -> None: ...

class _ResponseStream:
    def __init__(self, writable_stream: IO, url: str, headers: dict, binary_mode: bool, encoding: str = None) -> None: ...
    def close(self) -> None: ...
    def __next__(self) -> str | bytes: ...
    def read(self, n: int = -1) -> str | bytes: ...
    def seek(self, offset: int, whence: int = ...) -> int: ...

class _TextURLFile(_TextFile):
    def __init__(self, url: str, headers: dict, encoding: str = None) -> None: ...
    def close(self) -> None: ...
    def read(self, n: int = -1) -> str: ...
    def readline(self, limit: int = -1) -> str: ...
    def readlines(self, hint: int = -1) -> list[str]: ...
    def seek(self, offset: int, whence: int = ...) -> int: ...
    def __next__(self) -> str: ...

class _BinaryURLFile(_BinaryFile):
    def __init__(self, url: str, headers: dict) -> None: ...
    def close(self) -> None: ...
    def read(self, n: int = -1) -> bytes: ...
    def readline(self, limit: int = -1) -> bytes: ...
    def readlines(self, hint: int = -1) -> list[bytes]: ...
    def seek(self, offset: int, whence: int = ...) -> int: ...
    def __next__(self) -> bytes: ...

class _TextWritableFile(_TextFile):
    def __init__(self, path: str | bytes | os.PathLike, encoding: str = None) -> None: ...
    def write(self, s: str) -> int: ...

class _BinaryWritableFile(_BinaryFile):
    def __init__(self, path: str | bytes | os.PathLike) -> None: ...
    def write(self, s: bytes | bytearray) -> int: ...

class _FileManager(ABC, metaclass=abc.ABCMeta):
    @property
    @abstractmethod
    def source(self) -> str | None: ...
    @property
    @abstractmethod
    def writable(self) -> bool: ...
    @abstractmethod
    def create_text_file(self, encoding: str = None) -> TextIO: ...
    @abstractmethod
    def create_binary_file(self) -> BinaryIO: ...

class _DataFileManager(_FileManager):
    source: Incomplete
    writable: bool
    def __init__(self, data: str | bytes) -> None: ...
    def create_text_file(self, encoding: str = None) -> _TextFile: ...
    def create_binary_file(self) -> _BinaryFile: ...

class _PathFileManager(_FileManager):
    writable: bool
    def __init__(self, path: str | bytes | os.PathLike) -> None: ...
    @property
    def source(self) -> str: ...
    def create_text_file(self, encoding: str = None) -> _TextFile: ...
    def create_binary_file(self) -> _BinaryFile: ...

class _URLFileManager(_FileManager):
    writable: bool
    def __init__(self, url: str, headers: dict | None) -> None: ...
    @property
    def source(self) -> str: ...
    def create_text_file(self, encoding: str = None) -> _TextURLFile: ...
    def create_binary_file(self) -> _BinaryURLFile: ...

class _WritableFileManager(_FileManager):
    writable: bool
    def __init__(self) -> None: ...
    @property
    def source(self) -> str: ...
    def create_text_file(self, encoding: str = None) -> _TextWritableFile: ...
    def create_binary_file(self) -> _BinaryWritableFile: ...

class File:
    ''' Creates a File object. Only 1 of data, path or url should be set, or File() for writable file. Or use the
    corresponding class-methods.

    A File object can have one of the following 4 types:

        - SourceType.DATA: File object with in-memory data as its source

            - Created with `File.from_data(...)`
            - writable: False

        - SourceType.PATH: File object with an existing file (path) as its source

            - Created with `File.from_path(...)`
            - writable: False

        - SourceType.URL: File object with a URL as its source

            - Created with `File.from_url(...)`
            - writable: False

        - SourceType.WRITABLE: File object with a (temporary) writable file on disk as its source

            - Created with `File()`
            - writable: True (writing always takes place at end of file)

    Note: Reading from a File with SourceType.URL downloads (part of the) URL content to a (temporary) file on disk, so
    that re-reading (previously read) content within the same open-context does not require downloading twice. Opening
    the File object a second time DOES involve downloading the content anew. If such a File needs to be opened multiple
    times, consider copying the File locally (:meth:`~.copy`), so that downloading takes place only once.

    Example usage:

        .. code-block:: python

            data_file = vkt.File.from_data("my content")
            path_file = vkt.File.from_path(Path(__file__).parent / "my_file.txt")
            url_file = vkt.File.from_url("https://...")
            writable_file = vkt.File()

            data_content = data_file.getvalue_binary()  # bytes (b"my content")
            path_content = path_file.getvalue()  # str

            with url_file.open() as r:  # open in text-mode, so read -> str
                first_character = r.read(1)  # downloads only partially
                all_other_characters = r.read()  # downloads the rest

            with writable_file.open_binary() as w:  # open as binary-mode, so read/write -> bytes
                w.write(b"my content")

            writable_content = writable_file.getvalue()  # "my content"
    '''
    class SourceType(Enum):
        DATA: File.SourceType
        PATH: File.SourceType
        URL: File.SourceType
        WRITABLE: File.SourceType
    def __init__(self, *, data: str | bytes | None = None, path: str | bytes | os.PathLike | None = None, url: str | None = None, **kwargs: Any) -> None:
        """
        :param data: in-memory data source (also :meth:`~.from_data`)
        :param path: existing file path source (also :meth:`~.from_path`)
        :param url: URL source (also :meth:`~.from_url`)
        """
    @classmethod
    def from_data(cls, data: str | bytes) -> File:
        """ Create a File object with in-memory data as its source. """
    @classmethod
    def from_path(cls, path: str | bytes | os.PathLike) -> File:
        """ Create a File object with an existing file (path) as its source. """
    @classmethod
    def from_url(cls, url: str, *, headers: dict = None) -> File:
        """ Create a File object with a URL as its source. """
    @property
    def source(self) -> str | None:
        """ Source of the File object:

            - SourceType.DATA -> None
            - SourceType.PATH -> path of (readable) file on disk
            - SourceType.URL -> url
            - SourceType.WRITABLE -> path of (writable) file on disk

        """
    @property
    def source_type(self) -> SourceType:
        """ Source type of the file. """
    @property
    def writable(self) -> bool:
        """ Whether the File is writable or not (only True for SourceType.WRITABLE). """
    def open(self, encoding: str = None) -> TextIO:
        """ Open the file in text-mode.

        :param encoding: encoding used for reading the bytes -> str (default: default local encoding)
        :return: opened text file
        """
    def open_binary(self) -> BinaryIO:
        """ Open the file in binary-mode.

        :return: opened binary file
        """
    def getvalue(self, encoding: str = None) -> str:
        """ Read the content (text) of the file in memory. For large files, open the file and read in chunks, to
        prevent the app from running out of memory. """
    def getvalue_binary(self) -> bytes:
        """ Read the content (binary) of the file in memory. For large files, open the file and read in chunks, to
        prevent the app from running out of memory."""
    def copy(self, writable: bool = False) -> File:
        ''' Make a local copy of the file to disk.

        Example usages:

        URL-file that needs to be opened multiple times:

        .. code-block:: python

            # copying to path-file prevents re-downloading if opening more than once.
            path_file = url_file.copy()  # download the complete content locally

            with path_file.open() as r:  # no downloading
                ...

            with path_file.open() as r:  # no downloading
                ...

        Make writable file from read-only file:

        .. code-block:: python

            writable_file = read_only_file.copy(writable=True)

            with writable_file.open() as w:
                w.write("my content")

        :param writable: True to return writable file, False for read-only (default: False).
        :return: File object (SourceType.WRITABLE if writable = True, else SourceType.PATH).
        '''

class _MultipartEncoder(MultipartEncoder):
    """ This class is required because file is not read correctly by MultipartEncoder if it originates from
    File.from_url. By downloading the content completely to the local disk first, this problem is resolved. """
    def __init__(self, data: dict, file: BinaryIO) -> None: ...

class Color(NamedTuple('Color', [('r', int), ('g', int), ('b', int)])):
    def __new__(cls, r: int, g: int, b: int) -> Color:
        """ Create an immutable instance of Color

        :param r: red-value (0-255)
        :param g: green-value (0-255)
        :param b: blue-value (0-255)

        **plotly / bokeh:** Color objects are directly compatible with plotly and bokeh:

        .. code-block:: python

            import plotly.graph_objects as go
            from bokeh.plotting import figure

            color = vkt.Color(30, 144, 255)

            # plotly
            go.Scatter(x=x, y=y, mode='lines', line=dict(color=color, width=2))

            # bokeh
            p = figure()
            p.line(x, y, line_color=color, line_width=2)

        **matplotlib / seaborn:** Use the ``.hex`` property:

        .. code-block:: python

            import matplotlib.pyplot as plt
            import seaborn as sns

            color = vkt.Color(30, 144, 255)

            # ✓ CORRECT: Use .hex property for matplotlib and seaborn
            ax.bar(x, height, color=color.hex)
            sns.lineplot(x=x, y=y, color=color.hex)

            # ❌ INCORRECT: matplotlib/seaborn do not accept Color objects directly
            # ax.bar(x, height, color=color)
            # sns.lineplot(x=x, y=y, color=color)
        """
    def __copy__(self) -> Color: ...
    def __deepcopy__(self, memo: dict) -> Color: ...
    def __eq__(self, other: object) -> bool: ...
    @staticmethod
    def black() -> Color: ...
    @staticmethod
    def white() -> Color: ...
    @staticmethod
    def red() -> Color: ...
    @staticmethod
    def lime() -> Color: ...
    @staticmethod
    def green() -> Color: ...
    @staticmethod
    def blue() -> Color: ...
    @staticmethod
    def viktor_black() -> Color: ...
    @staticmethod
    def viktor_blue() -> Color: ...
    @staticmethod
    def viktor_yellow() -> Color: ...
    @classmethod
    def from_hex(cls, hex_value: str) -> Color:
        """ Color defined by hexadecimal code. """
    @classmethod
    def from_deltares(cls, value: int) -> Color:
        """ Color defined by Deltares-type integer.

        :param value: Integer representation of the color as used in the Deltares software series.
        """
    @staticmethod
    def random() -> Color:
        """ Generate a random color. """
    @property
    def rgb(self) -> tuple[int, int, int]: ...
    @property
    def hex(self) -> str:
        """ Hexadecimal representation of the color. """
    @property
    def deltares(self) -> int: ...
    @staticmethod
    def rgb_to_hex(r: int, g: int, b: int, include_hashtag: bool = True) -> str:
        """ Conversion from red-green-blue to hexadecimal value """
    @staticmethod
    def hex_to_rgb(hex_value: str) -> tuple[int, int, int]:
        """ Conversion from hexadecimal to red-green-blue value """
    @staticmethod
    def rgb_to_deltares(r: int, g: int, b: int) -> int:
        """ Conversion from Deltares-type color value to red-green-blue value.

        :return Integer representation of the color as used in the Deltares software series.
        """
    @staticmethod
    def deltares_to_rgb(value: int) -> tuple[int, int, int]:
        """ Conversion from red-green-blue to Deltares-type color value.

        :param value: Integer representation of the color as used in the Deltares software series.
        """

class _SerializableObject(metaclass=ABCMeta):
    """
    Abstract base class for Viktor objects that are serializable into a Python dict, primarily used for encoding output
    of automation jobs.
    """

def progress_message(message: str, percentage: float = None) -> None:
    """
    Send a user facing progress message informing the progress of an evaluation.
    Messages are truncated to 500 characters

    :param message: Message shown to the user
    :param percentage: Value between 0 and 100 quantifying the progress
    """

class Storage:
    """ Starting point to communicate with the storage to, for example, set or retrieve analysis results.

    The following actions are supported:

    .. code-block:: python

        storage = vkt.Storage()

        # Setting data on a key
        storage.set('data_key_1', data=vkt.File.from_data('abc'), scope='entity')
        storage.set('data_key_2', data=vkt.File.from_data('def'), scope='entity')

        # Retrieve the data by key
        storage.get('data_key_1', scope='entity')

        # List available data keys (by prefix)
        storage.list(scope='entity')                      # lists all files in current entity scope
        storage.list(prefix='data_key_', scope='entity')  # lists 'data_key_1', 'data_key_2', ... etc.

        # Delete data by key
        storage.delete('data_key_1', scope='entity')

    For each of these methods, a scope can be defined to point to a specific section in the storage. These scopes
    ensure efficient arrangement and handling of data. The following scopes can be used:

      - entity          : when data needs to be accessed within a specific entity
      - workspace       : when data needs to be accessed workspace-wide

    """
    def __init__(self) -> None: ...
    @_validate_storage_scope
    def set(self, key: str, data: File, *, scope: str, entity: Entity = None) -> None:
        """ Set data on a key for the specified scope.

        :param key: Unique key on which the data is set (max. 64 characters).
        :param data: Data to be stored.
        :param scope: Applicable scope, 'entity' | 'workspace'.
        :param entity: Applicable entity, used in combination with scope=='entity' (default: current entity).
        """
    @_validate_storage_scope
    def get(self, key: str, *, scope: str, entity: Entity = None) -> File:
        """ Retrieve data from a key for the specified scope.

        :param key: Unique key from which the data should be retrieved.
        :param scope: Applicable scope, 'entity' | 'workspace'.
        :param entity: Applicable entity, used in combination with scope=='entity' (default: current entity).
        :raises FileNotFoundError: When trying to retrieve a file that does not exist in the defined storage scope.
        """
    @_validate_storage_scope
    def delete(self, key: str, *, scope: str, entity: Entity = None) -> None:
        """ Delete a key-value pair for the specified scope.

        :param key: Unique key from which the key-value pair should be deleted.
        :param scope: Applicable scope, 'entity' | 'workspace'.
        :param entity: Applicable entity, used in combination with scope=='entity' (default: current entity).
        :raises FileNotFoundError: When trying to delete a file that does not exist in the defined storage scope.
        """
    @_validate_storage_scope
    def list(self, *, prefix: str = None, scope: str, entity: Entity = None) -> dict[str, File]:
        """ List all available key-value pairs for the specified scope.

        :param prefix: List all data of which the keys start with the provided prefix. Using a prefix potentially
            results in much higher performance due to a more efficient lookup in case of many stored files.
        :param scope: Applicable scope, 'entity' | 'workspace'.
        :param entity: Applicable entity, used in combination with scope=='entity' (default: current entity).
        """

class _MovedClass:
    '''
    Helper class to move/rename a class and deprecate the old. New class must be backward-compatible (implement all of
    old class).

    Note: Shows deprecation warning at call-time, not import. Consequently, does not show deprecation warning if only
    used for type hinting!

    Example usage:

    .. code-block:: python

        from viktor.core import _MovedClass
        from new_package.new_class import NewClass as _NewClass  # private! Should not become available here...
        OldClass = _MovedClass(_NewClass, "OldClass has been renamed to NewClass and moved to new_package", 20)

    '''
    new_class: Incomplete
    message: Incomplete
    upgrade_id: Incomplete
    def __init__(self, new_class: type, message: str, upgrade_id: int) -> None:
        """

        :param new_class: new class that replaces the deprecated class
        :param message: deprecation message to be shown
        :param upgrade_id: id in the upgrade instructions (part of the deprecation message)
        """
    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...
    def __getattr__(self, attr: Any) -> Any: ...
    def __instancecheck__(self, instance: Any) -> bool: ...
