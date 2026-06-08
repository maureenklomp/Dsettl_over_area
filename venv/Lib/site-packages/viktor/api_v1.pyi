import datetime
from .core import Color as Color, File as File
from .errors import BadRequestError as BadRequestError, ComputeError as ComputeError, EntityCreateError as EntityCreateError, EntityDeleteError as EntityDeleteError, EntityNotFoundError as EntityNotFoundError, EntityReviseError as EntityReviseError, InternalError as InternalError, PermissionDeniedError as PermissionDeniedError, PreconditionFailedError as PreconditionFailedError, ResourceNotFoundError as ResourceNotFoundError
from _typeshed import Incomplete
from munch import Munch as Munch
from typing import Any, BinaryIO, Iterator, TextIO

logger: Incomplete

class FileResource:
    """ File resource stored in the file manager.

    .. warning:: Do not instantiate this class directly, it will be returned in the parameter set when using a
        :class:`~viktor.parametrization.FileField` or :class:`~viktor.parametrization.MultiFileField`.
    """
    def __init__(self, workspace_id: int, source_id: int, api: _API = None) -> None: ...
    @property
    def file(self) -> File:
        """ Returns the File object (URL-file) attached to the resource. """
    @property
    def filename(self) -> str:
        """ Returns the filename of the resource (API call required!). """
    def open(self, encoding: str = None) -> TextIO:
        """ ::version(v14.27.0)

        Open the file in text mode directly.

        .. code-block:: python

            with params.my_file.open() as f:
                content = f.read()

        :param encoding: Text encoding (default: system encoding)
        :return: Text file-like object
        """
    def open_binary(self) -> BinaryIO:
        """::version(v14.27.0)

        Open the file in binary mode directly.

        .. code-block:: python

            with params.my_file.open_binary() as f:
                content = f.read()

        :return: Binary file-like object
        """

class _FileResource:
    source_id: Incomplete
    scope: Incomplete
    entity_id: Incomplete
    filename: Incomplete
    def __init__(self, *, source_id: int, scope: str, entity_id: int | None, filename: str) -> None:
        """ File resource stored in the file manager.

        :param source_id: Unique identifier
        :param scope: Scope of the file ('entity' | 'workspace')
        :param entity_id: Entity id to which the file is bound in case of 'entity' scope (None for 'workspace' scope)
        :param filename: Name of the file
        """

class User:
    """ User information.


    .. warning:: Do not instantiate this class directly, it is created by the API.

    """
    id: Incomplete
    first_name: Incomplete
    last_name: Incomplete
    email: Incomplete
    job_title: Incomplete
    def __init__(self, api: _API, *, id_: int, first_name: str, last_name: str, email: str, job_title: str, **_kwargs: Any) -> None:
        """
        :param id_: user's id
        :param first_name: user's first name
        :param last_name: user's last name
        :param email: user's email address
        :param job_title: user's job title
        """
    def __eq__(self, other: Any) -> bool: ...
    @property
    def full_name(self) -> str:
        """ User's full name (first name + last name). """

class Label:
    """ ::version(v14.9.0)

    .. warning:: Do not instantiate this class directly, it is created by the API.

    """
    id: Incomplete
    name: Incomplete
    description: Incomplete
    color: Incomplete
    def __init__(self, api: _API, id_: int, name: str, description: str, color: str, **_kwargs: Any) -> None:
        """
        :param api: API instance
        :param id_: ID of the Label
        :param name: Name of the Label
        :param description: Description of the Label
        :param color: Color of the Label
        """
    def __eq__(self, other: object) -> bool: ...

class App:
    """ ::version(v14.9.0)

    .. warning:: Do not instantiate this class directly, it is created by the API.

    """
    id: Incomplete
    name: Incomplete
    def __init__(self, api: _API, id_: int, name: str, **_kwargs: Any) -> None:
        """
        :param api: API instance
        :param id_: ID of the App
        :param name: Name of the App
        """
    def __eq__(self, other: object) -> bool: ...

class AppVersion:
    """ ::version(v14.9.0)

    .. warning:: Do not instantiate this class directly, it is created by the API.

    """
    id: Incomplete
    tag: Incomplete
    status: Incomplete
    app_type: Incomplete
    sdk_version: Incomplete
    python_version: Incomplete
    created_at: Incomplete
    def __init__(self, api: _API, id_: int, tag: str, status: str, app_type: str, sdk_version: str, python_version: str, created_at: str, **_kwargs: Any) -> None:
        """
        :param api: API instance
        :param id_: ID of the AppVersion
        :param tag: Tag of the AppVersion
        :param status: Status of the AppVersion publish
        :param app_type: Type of App as defined in the App definition
        :param sdk_version: Version of the SDK
        :param python_version: Version of the python
        :param created_at: Timestamp of when AppVersion was created.
        """
    def __eq__(self, other: object) -> bool: ...

class EntityType:
    """
    .. warning:: Do not instantiate this class directly, it is created by the API.

    """
    id: Incomplete
    name: Incomplete
    def __init__(self, api: _API, id_: int, class_name: str, **_kwargs: Any) -> None:
        """
        :param id_: Unique ID of the entity type.
        :param name: Entity type name (not label).
        """
    def __eq__(self, other: object) -> bool: ...

class _ResolvedEntity:
    """ Entity that has been resolved through a get-request. Can be done both with or without params. """
    name: Incomplete
    id: Incomplete
    entity_type: Incomplete
    def __init__(self, api: _API, name: str, id_: int, entity_type: EntityType, params: Munch = None, summary: Munch = None) -> None:
        """

        :param api: API that is used to resolve.
        :param name: Name of the entity.
        :param id_: Unique ID of the entity.
        :param entity_type: Type of the entity.
        :param params: Note that these should be the deserialized params!
        :param summary: Deserialized summary.
        """
    @classmethod
    def from_json(cls, response_json: dict, *, api: _API, workspace_id: int) -> _ResolvedEntity: ...
    @property
    def last_saved_params(self) -> Munch: ...
    @property
    def last_saved_summary(self) -> Munch: ...

class EntityRevision:
    """
    .. warning:: Do not instantiate this class directly, it is created by the API.

    """
    id: Incomplete
    params: Incomplete
    created_date: Incomplete
    def __init__(self, api: _API, id_: int, params: Munch, created_date: datetime.datetime) -> None:
        """
        :param params: Stored params in the entity's revision.
        :param created_date: Date(time) of creation of the entity's revision.
        """

class Entity:
    """
    .. warning:: Do not instantiate this class directly, it is created by the API.
    """
    def __init__(self, api: _API, workspace_id: int, origin_id: int, operations: list[tuple[str, bool]], resolved: _ResolvedEntity = None) -> None: ...
    @property
    def name(self) -> str:
        """Name of the entity."""
    @property
    def entity_type(self) -> EntityType:
        """EntityType of the entity."""
    @property
    def id(self) -> int:
        """id of the entity."""
    @property
    def last_saved_params(self) -> Munch:
        """ Get the params of the last saved entity revision. """
    @property
    def last_saved_summary(self) -> Munch:
        """ Get the summary of the last saved entity revision. """
    def parent(self, *, privileged: bool = False) -> Entity: ...
    def children(self, *, include_params: bool = True, entity_type_names: list[str] = None, privileged: bool = False) -> EntityList: ...
    def siblings(self, *, include_params: bool = True, entity_type_names: list[str] = None, privileged: bool = False) -> EntityList: ...
    def get_file(self) -> File:
        """ Get the file of the entity.

        :return: File object (SourceType.URL)
        :raises ValueError: if file does not have a file associated with it.
        """
    def create_child(self, entity_type_name: str, name: str, *, params: dict | Munch = None, privileged: bool = False, **kwargs: Any) -> Entity: ...
    def revisions(self) -> EntityRevisionList:
        """ Get all revisions of the entity. """
    def delete(self, *, privileged: bool = False) -> None: ...
    def set_params(self, params: dict | Munch, *, privileged: bool = False) -> Entity: ...
    def rename(self, name: str, *, privileged: bool = False) -> Entity: ...
    def compute(self, method_name: str, *, params: dict | Munch, timeout: int = None) -> dict:
        """ ::version(v14.12.0)

        Run a callable entity controller method (view-method, button-method, step-method or preprocess-method) and
        return the result.

        :param method_name: Name of the controller method to call
        :param params: Params to call the method with
        :param timeout: Maximum job duration after which it will time out
        :return: Return value of the controller method
        """

class Workspace:
    """ ::version(v14.9.0)

    .. warning:: Do not instantiate this class directly, it is created by the API.

    Can be used to fetch additional data within the given workspace.

    .. code-block:: python

        # Get workspace object
        workspace: Workspace = api.get_workspace(workspace_id)

        # Iterate over underlying data
        for entity in workspace.get_root_entities():
            ...
        for entity_type in workspace.get_entity_types():
            ...

    """
    id: Incomplete
    name: Incomplete
    description: Incomplete
    visibility: Incomplete
    created_at: Incomplete
    updated_at: Incomplete
    is_archived: Incomplete
    app: Incomplete
    app_version: Incomplete
    labels: Incomplete
    def __init__(self, api: _API, id_: int, name: str, description: str, visibility: str, created_at: str, updated_at: str, is_archived: bool, app: dict | None, app_version: dict | None, labels: list[dict], **kwargs: Any) -> None:
        """
        :param id_: Unique ID of the workspace.
        :param name: Name of the workspace.
        :param description: Descriptive text of the workspace content.
        :param visibility: Visibility of the workspace. (Can be INTERNAL, PRIVATE, PUBLIC, or DEVELOPMENT)
        :param created_at: Timestamp of when workspace was created.
        :param updated_at: Timestamp of when workspace was last updated.
        :param is_archived: Whether the workspace is archived.
        :param app: App assigned to the workspace. (Can be None for Development workspace)
        :param app_version: Published AppVersion assigned to the workspace. (Can be None for Development workspace)
        :param labels: Labels assigned to the workspace.
        """
    def __eq__(self, other: object) -> bool: ...
    def get_root_entities(self, *, include_params: bool = True, entity_type_names: list[str] = None, privileged: bool = False) -> EntityList: ...
    def get_entity(self, id_: int, privileged: bool = False) -> Entity: ...
    def get_entity_types(self) -> EntityTypeList: ...
    def get_entity_type(self, id_: int) -> EntityType: ...
    def entity_compute(self, *, entity_id: int, method_name: str, params: dict | Munch, timeout: int = None) -> dict:
        """ ::version(v14.12.0)

        Run a callable entity controller method (view-method, button-method, step-method or preprocess-method) and
        return the result.

        :param entity_id: ID of the entity to call the method from
        :param method_name: Name of the controller method to call
        :param params: Params to call the method with
        :param timeout: Maximum job duration after which it will time out
        :return: Return value of the controller method
        """

class EntityList:
    """
    .. warning:: Do not instantiate this class directly, it is created by the API.

    Object which resembles a list of Entity objects.

    Most commonly used list operations are supported:

    .. code-block:: python

        # indexing
        children = entity.children()
        children[0]  # first child entity
        children[-1]  # last child entity

        # length
        number_of_children = len(children)

        # for loop
        for child in children:
            # perform operation on child

    """
    def __init__(self, api: _API, workspace_id: int, relation: str, origin: Entity | None, entity_type_names: list[str] | None, include_params: bool, *, privileged: bool = False) -> None: ...
    def __len__(self) -> int: ...
    def __getitem__(self, index: int) -> Entity: ...
    def __iter__(self) -> Iterator[Entity]: ...

class EntityRevisionList:
    """
    .. warning:: Do not instantiate this class directly, it is created by the API.

    Object which resembles a list of EntityRevision objects.

    Most commonly used list operations are supported:

    .. code-block:: python

        # indexing
        revisions = entity.revisions()
        revisions[0]  # first revision
        revisions[-1]  # last revision

        # length
        number_of_revisions = len(revisions)

        # for loop
        for revision in revisions:
            # perform operation on revision

    """
    def __init__(self, api: _API, entity: Entity, *, privileged: bool = False) -> None: ...
    def __len__(self) -> int:
        """Do a paginated request to retrieve the count"""
    def __getitem__(self, index: int) -> EntityRevision:
        """Do a paginated request to retrieve with specific limit and offset to retrieve the resource at an index"""
    def __iter__(self) -> Iterator[EntityRevision]:
        """Create an iterator of a paginated request"""

class EntityTypeList:
    """ ::version(v14.9.0)

    .. warning:: Do not instantiate this class directly, it is created by the API.

    Object which resembles a list of EntityType objects.

    Most commonly used list operations are supported:

    .. code-block:: python

        # indexing
        entity_types = api.get_entity_types()
        entity_types[0]  # first entity_type
        entity_types[-1]  # last entity_type

        # length
        number_of_entity_types = len(entity_types)

        # for loop
        for entity_type in entity_types:
            # perform operation on entity_type

    """
    def __init__(self, api: _API, workspace_id: int) -> None: ...
    def __len__(self) -> int:
        """Do a paginated request to retrieve the count"""
    def __getitem__(self, index: int) -> EntityType:
        """Do a paginated request to retrieve with specific limit and offset to retrieve the resource at an index"""
    def __iter__(self) -> Iterator[EntityType]:
        """Create an iterator of a paginated request"""

class WorkspaceList:
    """ ::version(v14.9.0)

    .. warning:: Do not instantiate this class directly, it is created by the API.

    Object which resembles a list of Workspace objects.

    Most commonly used list operations are supported:

    .. code-block:: python

        # indexing
        workspaces = api.get_workspaces()
        workspaces[0]  # first workspace
        workspaces[-1]  # last workspace

        # length
        number_of_workspaces = len(workspaces)

        # for loop
        for workspace in workspaces:
            # perform operation on workspace

    """
    def __init__(self, api: _API, app_name: str = None, include_archived: bool = False) -> None: ...
    def __len__(self) -> int:
        """Do a paginated request to retrieve the count"""
    def __getitem__(self, index: int) -> Workspace:
        """Do a paginated request to retrieve with specific limit and offset to retrieve the resource at an index"""
    def __iter__(self) -> Iterator[Workspace]:
        """Create an iterator of a paginated request"""

class Job:
    """ ::version(v14.12.0)

    .. warning:: Do not instantiate this class directly, it is created by the API.

    """
    id: Incomplete
    def __init__(self, api: _API, workspace_id: int, id_: int) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def get_result(self, *, timeout: int = 15) -> dict:
        """ Obtain the job result

        :return: Job result
        :raises TimeoutError: If timeout is exceeded
        """

class _ConversationExchange:
    prompt: Incomplete
    response: Incomplete
    def __init__(self, prompt: list[dict], response: list[dict]) -> None: ...
    @classmethod
    def from_json(cls, response_json: dict[str, list[dict]]) -> _ConversationExchange: ...
    def to_llm_format(self) -> list[dict[str, str]]: ...

class ChatConversation:
    """ ::version(v14.21.0)

    .. warning:: Do not instantiate this class directly, it is created by the API.
    """
    def __init__(self, *, api: _API, workspace_id: int, entity_id: int, latest_exchange_id: int) -> None: ...
    def get_messages(self) -> list[dict[str, str]]:
        """ Get the full history of the conversation as a list of messages.

        Each message in the list has the following format:

        .. code-block:: python

            {
                'role': str,        # user | assistant
                'content': str,     # the actual message
            }
        """

class _API:
    host: Incomplete
    def __init__(self, token: str, host: str) -> None: ...
    def __del__(self) -> None: ...
    def get_current_user(self) -> User: ...
    def get_workspaces(self, *, app_name: str | None = None, include_archived: bool = False) -> WorkspaceList:
        ''' ::version(v14.9.0)

        Get the workspaces in the environment. (Requires a `token` to be set on the API class)

        :param app_name: Filter the workspaces by app name.
        :param include_archived: True to include the archived workspaces. (Only permitted for Organization Admins)

        Can be used to iterate over the workspaces:

            .. code-block:: python

                api = API(token=os.environ["TOKEN"])
                for workspace in api.get_workspaces():
                    for entity in workspace.get_root_entities():
                        ...
        '''
    def get_workspace(self, id_: int) -> Workspace:
        """ ::version(v14.9.0)

        Get the workspace with given id.  (Requires a `token` to be set on the API class)

        :param id_: workspace_id
        """
    def get_entity(self, id_: int, *, privileged: bool = False, workspace_id: int = None) -> Entity: ...
    def get_entity_type(self, id_: int, *, workspace_id: int = None) -> EntityType:
        """ ::version(v14.9.0)

        Get the entity type with given id.

        :param id_: entity_type_id
        :param workspace_id: (optional) Provide workspace id if you want to access entity types outside the context of the app.
        """
    def get_entity_types(self, *, workspace_id: int = None) -> EntityTypeList:
        """ ::version(v14.9.0)

        Get the entity types.

        :param workspace_id: (optional) Provide id if you want to access resource from outside the context of the app
        """
    def get_root_entities(self, *, include_params: bool = True, entity_type_names: list[str] = None, privileged: bool = False, workspace_id: int = None) -> EntityList: ...
    def get_entity_parent(self, entity_id: int, *, privileged: bool = False, workspace_id: int = None) -> Entity: ...
    def get_entity_children(self, entity_id: int, *, include_params: bool = True, entity_type_names: list[str] = None, privileged: bool = False, workspace_id: int = None) -> EntityList: ...
    def get_entity_siblings(self, entity_id: int, *, include_params: bool = True, entity_type_names: list[str] = None, privileged: bool = False, workspace_id: int = None) -> EntityList: ...
    def get_entity_file(self, entity_id: int, *, privileged: bool = False, workspace_id: int = None) -> File: ...
    def entity_compute(self, *, workspace_id: int, entity_id: int, method_name: str, params: dict | Munch, timeout: int = None) -> dict:
        """ ::version(v14.12.0)

        Run a callable entity controller method (view-method, button-method, step-method or preprocess-method) and
        return the result.

        :param workspace_id: ID of the workspace the entity resides in
        :param entity_id: ID of the entity to call the method from
        :param method_name: Name of the controller method to call
        :param params: Params to call the method with
        :param timeout: Maximum job duration after which it will time out
        :return: Return value of the controller method
        """
    def create_child_entity(self, parent_entity_id: int, entity_type_name: str, name: str, *, params: dict | Munch = None, privileged: bool = False, workspace_id: int = None, **kwargs: Any) -> Entity: ...
    def get_entity_revisions(self, entity_id: int, *, privileged: bool = False, workspace_id: int = None) -> EntityRevisionList: ...
    def delete_entity(self, entity_id: int, *, privileged: bool = False, workspace_id: int = None) -> None: ...
    def set_entity_params(self, entity_id: int, params: dict | Munch, *, privileged: bool = False, workspace_id: int = None) -> Entity: ...
    def rename_entity(self, entity_id: int, name: str, *, privileged: bool = False, workspace_id: int = None) -> Entity: ...
    def get_entities_by_type(self, entity_type_name: str, *, include_params: bool = True, privileged: bool = False, workspace_id: int = None) -> EntityList: ...
    def generate_upload_url(self, entity_type_name: str, *, privileged: bool = False, workspace_id: int = None) -> dict: ...

class API(_API):
    ''' Starting point of making an API call to, for example, retrieve properties of an entity.

    Can be initialized:

       1. within a VIKTOR app, without init-arguments, to perform API calls to any data within the corresponding workspace.
       2. **(new in v14.9.0)** within a VIKTOR app, with `token` argument, to perform API calls to any data within the environment (cross-workspace).
       3. **(new in v14.9.0)** outside a VIKTOR app, with `token` and `environment` arguments, to perform API calls to any data within the specified environment.

    Note that the permissions of a user (group) are reflected on the permissions of this API call, e.g. if a user
    only has read-navigate or read-basic permission, calling the params (read-all) of the object using this API
    will NOT work for this specific user.

    Example for case 1 (inside app, within context of current workspace):

    .. code-block:: python

        from viktor.api_v1 import API

        api = API()
        current_entity = api.get_entity(entity_id)
        parent = current_entity.parent()
        parent_params = parent.last_saved_params

    Example for case 2 (inside app, outside context of current workspace):

    .. code-block:: python

        from viktor.api_v1 import API

        api = API(token=os.environ["TOKEN"])
        for workspace in api.get_workspaces():
            for entity in workspace.get_root_entities():
                entity_params = entity.last_saved_params

    Example for case 3 (external to VIKTOR platform):

    .. code-block:: python

        from viktor.api_v1 import API

        if __name__ == "__main__":
            api = API(token=os.environ["TOKEN"], environment="cloud.us1.viktor.ai")
            for workspace in api.get_workspaces():
                for entity in workspace.get_root_entities():
                    entity_params = entity.last_saved_params

    '''
    def __init__(self, environment: str | None = None, token: str | None = None) -> None:
        """
        .. automethod:: get_workspace
        .. automethod:: get_workspaces
        .. automethod:: get_entity_type
        .. automethod:: get_entity_types
        .. automethod:: get_entity
        .. automethod:: get_entities_by_type
        .. automethod:: get_root_entities
        .. automethod:: get_entity_parent
        .. automethod:: get_entity_children
        .. automethod:: get_entity_siblings
        .. automethod:: get_entity_revisions
        .. automethod:: get_entity_file
        .. automethod:: get_current_user
        .. automethod:: create_child_entity
        .. automethod:: delete_entity
        .. automethod:: rename_entity
        .. automethod:: set_entity_params
        """
