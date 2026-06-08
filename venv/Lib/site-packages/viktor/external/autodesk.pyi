import dataclasses
from ..core import File as File
from _typeshed import Incomplete

@dataclasses.dataclass
class AutodeskFileVersion:
    """ ::version(v14.25.0)

    .. warning:: Do not instantiate this class directly, it is created from :class:`AutodeskFile`.
    """
    @property
    def urn(self) -> str:
        ''' Get the unique resource name (also called "id") of this version of the file on Autodesk cloud storage. '''
    @property
    def attributes(self) -> dict:
        """ Get the attributes of this version of the file on Autodesk cloud storage. """
    @property
    def storage_url(self) -> str | None:
        """ ::version(v14.26.0)

        Get the storage URL of this version of the file.
        """
    def get_file(self) -> File:
        """ Download the content of this version of the file from Autodesk cloud storage. """

class AutodeskFile:
    ''' ::version(v14.25.0)

    Represents a file stored on Autodesk cloud storage (https://aps.autodesk.com/)

    Example:

    .. code-block:: python

        import viktor as vkt

        # Set up OAuth2 integration to get access token
        integration = vkt.external.OAuth2Integration("autodesk-integration")
        token = integration.get_access_token()

        # Get the AutodeskFile from a parametrization field
        autodesk_file = params.autodesk_file  # value of AutodeskFileField

        # Get the AEC Data Model element group ID (requires API call)
        element_group_id = autodesk_file.get_aec_data_model_element_group_id(token)
        print(f"The element group id is: {element_group_id}")

        # Access file properties and metadata:
        project_id = autodesk_file.project_id        # Can be extracted from URL
        urn = autodesk_file.urn                      # Get the unique resource name
        hub_id = autodesk_file.get_hub_id(token)     # Requires API call
        region = autodesk_file.get_region(token)     # Requires API call
    '''
    def __init__(self, url: str) -> None: ...
    @property
    def url(self) -> str:
        """ URL of the file on Autodesk cloud storage. """
    @property
    def urn(self) -> str:
        ''' ::version(v14.26.0)

        Get the unique resource name (also called "id") of this file on Autodesk cloud storage.
        '''
    @property
    def project_id(self) -> str:
        """ ::version(v14.26.0)

        Get the id of the project this file belongs to.
        """
    def get_hub_id(self, access_token: str) -> str:
        """ ::version(v14.26.0)

        Get the id of the hub this file belongs to.
        """
    def get_region(self, access_token: str) -> str:
        """ ::version(v14.26.0)

        Get the region of the hub this file belongs to.
        """
    def get_latest_version(self, access_token: str) -> AutodeskFileVersion:
        """ Get the latest version of the file on Autodesk cloud storage.

        :param access_token: Autodesk Platform Services token to access the file.
        """
    def get_aec_data_model_element_group_id(self, access_token: str) -> str:
        """ ::version(v14.26.0)

        Get the AEC Data Model ElementGroup ID associated with this file.
        """

class _DataManagementAPI:
    """https://aps.autodesk.com/en/docs/data/v2/developers_guide/overview/"""
    PROJECT_BASE_URL: Incomplete
    DATA_BASE_URL: Incomplete
    OSS_BASE_URL: Incomplete
    @classmethod
    def extract_project_id_from_url(cls, url: str) -> str | None: ...
    @classmethod
    def extract_item_id_from_url(cls, url: str) -> str | None: ...
    @classmethod
    def extract_bucket_key_from_url(cls, url: str) -> str | None: ...
    @classmethod
    def extract_object_key_from_url(cls, url: str) -> str | None: ...
    @classmethod
    def get_item_tip(cls, *, project_id: str, item_id: str, access_token: str) -> dict:
        """https://aps.autodesk.com/en/docs/data/v2/reference/http/projects-project_id-items-item_id-tip-GET/"""
    @classmethod
    def get_signed_s3_url(cls, *, bucket_key: str, object_key: str, access_token: str) -> dict:
        """https://aps.autodesk.com/en/docs/data/v2/reference/http/buckets-:bucketKey-objects-:objectKey-signeds3download-GET/"""
    @classmethod
    def get_hubs(cls, *, access_token: str) -> dict:
        """https://aps.autodesk.com/en/docs/data/v2/reference/http/hubs-GET/"""
    @classmethod
    def get_hub(cls, *, hub_id: str, access_token: str) -> dict:
        """https://aps.autodesk.com/en/docs/data/v2/reference/http/hubs-hub_id-GET/"""
    @classmethod
    def get_project(cls, *, hub_id: str, project_id: str, access_token: str) -> dict:
        """https://aps.autodesk.com/en/docs/data/v2/reference/http/hubs-hub_id-projects-project_id-GET/"""

class _AECDataModelAPI:
    """https://aps.autodesk.com/en/docs/aecdatamodel/v1/developers_guide/overview/"""
    GRAPHQL_URL: Incomplete
    @classmethod
    def get_hubs(cls, *, region: str, access_token: str, limit: int = None, cursor: str = None) -> dict:
        """https://aps.autodesk.com/en/docs/aecdatamodel/v1/reference/queries/hubs/"""
    @classmethod
    def get_element_groups_by_hub(cls, *, hub_id: str, region: str, access_token: str, file_urn: str | None = None, limit: int = None, cursor: str = None) -> dict:
        """https://aps.autodesk.com/en/docs/aecdatamodel/v1/reference/queries/hubs/"""
