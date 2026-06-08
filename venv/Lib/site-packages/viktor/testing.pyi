import datetime
from .api_v1 import Entity as Entity, EntityList as EntityList, EntityRevision as EntityRevision, EntityType as EntityType, FileResource as FileResource, User as User
from .core import File as File, ViktorController as ViktorController
from .errors import EntityCreateError as EntityCreateError, EntityDeleteError as EntityDeleteError, EntityNotFoundError as EntityNotFoundError, EntityReviseError as EntityReviseError
from .parametrization import Parametrization as Parametrization
from _typeshed import Incomplete
from io import BytesIO, StringIO
from munch import Munch
from typing import Any, Callable, Iterator, Sequence

def mock_ParamsFromFile(controller: type[ViktorController]) -> Callable:
    ''' Decorator that can be used for testing methods decorated with :class:`viktor.core.ParamsFromFile`.

    Example:

    .. code-block:: python

        import unittest
        import viktor as vkt

        from app.my_entity.controller import MyEntityController

        class TestMyEntityController(unittest.TestCase):
            @vkt.testing.mock_ParamsFromFile(MyEntityController)
            def test_process_file(self):
                file = vkt.File.from_data("abc")
                returned_dict = MyEntityController().process_file(file)
                self.assertDictEqual(returned_dict, {...})

    :param controller: Controller class on which the ParamsFromFile should be mocked
    '''
def mock_Storage(*, get: Sequence[File] = None, list: Sequence[dict[str, File]] = None) -> Callable:
    ''' Decorator that can be used for testing methods which invoke the :class:`viktor.core.Storage`.

    Use the `get` and `list` arguments to instruct which file(s) the respective Storage().get(...) and
    Storage().list(...) methods should return.

    Example:

    .. code-block:: python

        import unittest
        import viktor as vkt

        from app.my_entity.controller import MyEntityController

        class TestMyEntityController(unittest.TestCase):
            @vkt.testing.mock_Storage(
                get=[vkt.File.from_data("abc"), vkt.File.from_data("def")],
                list=[{\'data_key_3\': vkt.File.from_data("ghi")}]
            )
            def test_process_analysis_result(self):
                # Storage().get(...) invoked twice, Storage().list(...) invoked once
                result = MyEntityController().process_analysis_result()
                ...

    :param get: Files to be returned by Storage().get(...). The files are returned in order of the input list.
    :param list: File dicts to be returned by Storage().list(...). The dicts are returned in order of the input list.
    '''

class MockedEntityType(EntityType):
    def __init__(self, name: str = 'MockedEntityType', entity_type_id: int = 1) -> None:
        """ ::version(v13.3.0)

        To mock a EntityType.
        """

class MockedEntityRevision(EntityRevision):
    def __init__(self, params: dict | Munch = None, created_date: datetime.datetime = None, entity_revision_id: int = 1) -> None:
        ''' ::version(v13.3.0)

        To mock an EntityRevision.

        Example:

        .. code-block:: python

            import viktor as vkt

            params = {
                \'number\': 1,
                \'entity\': vkt.testing.MockedEntity(name="MyEntity"),
                \'file\': vkt.testing.MockedFileResource(vkt.File.from_data("content"), "file.txt")
            }

            mocked_entity_revision = vkt.testing.MockedEntityRevision(params)

        `params` can be passed from a JSON file by making use of :func:`~.mock_params`:

        .. code-block:: python

            import viktor as vkt

            from app.my_entity.controller import MyEntityController

            json_file = vkt.File.from_path("path to JSON file")
            params = vkt.mock_params(
                json_file, MyEntityController.parametrization,
                entities={1: vkt.testing.MockedEntity(name="MyEntity")},
                file_resources={1: vkt.testing.MockedFileResource(vkt.File.from_data("content"), "file")}
            )

            mocked_entity_revision = vkt.testing.MockedEntityRevision(params)

        :param params: Return value of EntityRevision.params. Must be the deserialized params
         (see :func:`~.mock_params`). None to set default (empty) params.
        :param created_date: Return value of EntityRevision.created_date. None to set default date (2000, 1, 1).
        :param entity_revision_id: Return value of EntityRevision.id.
        '''

class MockedUser(User):
    def __init__(self, *, first_name: str = 'John', last_name: str = 'Doe', email: str = 'john.doe@email.com', job_title: str = 'Employee', user_id: int = 1) -> None:
        """ ::version(v13.3.0)

        To mock a User.
        """

class MockedFileResource:
    @property
    def __class__(self) -> type: ...
    file: Incomplete
    filename: Incomplete
    def __init__(self, file: File = None, filename: str = 'mocked_file.txt') -> None:
        ''' ::version(v13.3.0)

        To mock a FileResource.

        :param file: Return value of FileResource.file. None to set default file with content = "mocked content".
        :param filename: Return value of FileResource.filename.
        '''

class MockedEntity:
    @property
    def __class__(self) -> type: ...
    def __init__(self, *, entity_id: int = 1, name: str = 'Mocked Entity', entity_type: MockedEntityType = None, last_saved_params: dict | Munch = None, last_saved_summary: dict = None, get_file: File = None, parent: MockedEntity = None, children: Sequence['MockedEntity'] = None, siblings: Sequence['MockedEntity'] = None, revisions: Sequence[MockedEntityRevision] = None, invalid: bool = False, workspace_id: int = 1) -> None:
        ''' ::version(v13.3.0)

        To mock an Entity. All arguments are optional: instantiating MockedEntity without parameters returns a default
        MockedEntity.

        Example:

        .. code-block:: python

            import viktor as vkt

            mocked_entity = vkt.testing.MockedEntity(last_saved_params=params, revisions=[vkt.testing.MockedEntityRevision(params)])

        last_saved_params can be passed from a JSON file by making use of :func:`~.mock_params`:

        .. code-block:: python

            import viktor as vkt

            from app.my_entity.controller import MyEntityController

            json_file = vkt.File.from_path("path to JSON file")
            params = vkt.testing.mock_params(json_file, MyEntityController.parametrization)
            mocked_entity = vkt.testing.MockedEntity(last_saved_params=params, revisions=[vkt.testing.MockedEntityRevision(params)])

        :param entity_id: Return value of Entity.id.
        :param name: Return value of Entity.name.
        :param entity_type: Return value of Entity.entity_type. None for default MockedEntityType.
        :param last_saved_params: Return value of Entity.last_saved_params(). Must be the deserialized params
         (see :func:`~.mock_params`). None to simulate an entity without params.
        :param last_saved_summary: Return value of Entity.last_saved_summary(). None to simulate an entity without
         summary.
        :param get_file: Return value of Entity.get_file. None to simulate an entity without file.
        :param parent: Return value of Entity.parent. None to simulate an entity without parent.
        :param children: Return value of Entity.children. None to simulate an entity without children.
        :param siblings: Return value of Entity.siblings. None to simulate an entity without siblings.
        :param revisions: Return value of Entity.revisions. None to simulate an entity without revisions.
        :param invalid: Set to True to simulate failing API calls on this Entity.
        '''
    @property
    def id(self) -> int: ...
    @property
    def name(self) -> str: ...
    @property
    def entity_type(self) -> MockedEntityType: ...
    @property
    def last_saved_params(self) -> Munch: ...
    @property
    def last_saved_summary(self) -> Munch: ...
    def get_file(self, *args: Any, **kwargs: Any) -> File: ...
    def parent(self, *args: Any, **kwargs: Any) -> MockedEntity: ...
    def children(self, *args: Any, entity_type_names: list[str] = None, **kwargs: Any) -> MockedEntityList: ...
    def siblings(self, *args: Any, entity_type_names: list[str] = None, **kwargs: Any) -> MockedEntityList: ...
    def create_child(self, entity_type_name: str, name: str, *args: Any, params: dict | Munch = None, **kwargs: Any) -> MockedEntity: ...
    def delete(self, *args: Any, **kwargs: Any) -> None: ...
    def rename(self, name: str, *args: Any, **kwargs: Any) -> MockedEntity: ...
    def revisions(self, *args: Any, **kwargs: Any) -> list[MockedEntityRevision]: ...
    def set_params(self, params: dict | Munch, *args: Any, **kwargs: Any) -> MockedEntity: ...

class MockedEntityList:
    @property
    def __class__(self) -> type: ...
    def __init__(self, entities: Sequence[MockedEntity], *, error: type[Exception] = None) -> None: ...
    def __len__(self) -> int: ...
    def __getitem__(self, index: int) -> MockedEntity: ...
    def __iter__(self) -> Iterator[MockedEntity]: ...

def mock_API(*, get_entity: Sequence[MockedEntity] | MockedEntity = None, create_child_entity: Sequence[MockedEntity] | MockedEntity = None, generate_upload_url: Sequence[dict] | dict = None, get_current_user: Sequence[MockedUser] | MockedUser = None, get_entities_by_type: Sequence[Sequence[MockedEntity]] | Sequence[MockedEntity] = None, get_entity_children: Sequence[Sequence[MockedEntity]] | Sequence[MockedEntity] = None, get_entity_siblings: Sequence[Sequence[MockedEntity]] | Sequence[MockedEntity] = None, get_root_entities: Sequence[Sequence[MockedEntity]] | Sequence[MockedEntity] = None, get_entity_parent: Sequence[MockedEntity] | MockedEntity = None, get_entity_revisions: Sequence[Sequence[MockedEntityRevision]] | Sequence[MockedEntityRevision] = None, get_entity_file: Sequence[File] | File = None, rename_entity: Sequence[MockedEntity] | MockedEntity = None, set_entity_params: Sequence[MockedEntity] | MockedEntity = None) -> Callable:
    ''' ::version(v13.3.0)

    Decorator that can be used to mock API() method calls, to facilitate easier testing.

    Example:

    .. code-block:: python

        import unittest
        import viktor as vkt

        from app.my_entity.controller import MyEntityController

        class TestMyEntityController(unittest.TestCase):
            @vkt.testing.mock_API(
                get_entity=[vkt.testing.MockedEntity(entity_id=98), vkt.testing.MockedEntity(entity_id=99)],
                get_entity_file=vkt.File.from_data("fake content")
            )
            def test_api_calls(self):
                MyEntityController().api_calls()

    Note that last_saved_params can be passed to MockedEntity from a JSON file by making use of :func:`~.mock_params`:

    .. code-block:: python

        import unittest
        import viktor as vkt

        from app.my_entity.controller import MyEntityController

        class TestMyEntityController(unittest.TestCase):
            json_file = vkt.File.from_path("path to JSON file")
            params = vkt.testing.mock_params(
                json_file, MyEntityController.parametrization,
                entities={1: vkt.testing.MockedEntity(name="MyEntity")},
                file_resources={1: vkt.testing.MockedFileResource(vkt.File.from_data("content"), "file")}
            )

            @vkt.testing.mock_API(
                get_entity=vkt.testing.MockedEntity(last_saved_params=params, revisions=[vkt.testing.MockedEntityRevision(params)])
            )
            def test_api_calls(self):
                MyEntityController().api_calls()

    For all parameters the following holds:
        - If a Sequence type is provided, the next entry is returned for each corresponding API method call. When an
          API method is called on a depleted iterable, an Exception is raised.
        - If a single object is provided, the object is returned each time the corresponding API method is called
          (endlessly).
        - If None is provided (default), a default object is returned each time the corresponding API method is called
          (endlessly).

    :param get_entity: Return value of API.get_entity.
    :param create_child_entity: Return value of API.create_child_entity.
    :param generate_upload_url: Return value of API.generate_upload_url.
    :param get_current_user: Return value of API.get_current_user.
    :param get_entities_by_type: Return value of API.get_entities_by_type.
    :param get_entity_children: Return value of API.get_entity_children.
    :param get_entity_siblings: Return value of API.get_entity_siblings.
    :param get_root_entities: Return value of API.get_root_entities.
    :param get_entity_parent: Return value of API.get_entity_parent.
    :param get_entity_revisions: Return value of API.get_entity_revisions.
    :param get_entity_file: Return value of API.get_entity_file.
    :param rename_entity: Return value of API.rename_entity.
    :param set_entity_params: Return value of API.set_entity_params.
    '''
def mock_params(params: dict | File, parametrization: Parametrization | type[Parametrization], file_resources: dict[int, MockedFileResource] = None, entities: dict[int, MockedEntity] = None) -> Munch:
    ''' Convert a plain dict to the (deserialized) params, replacing FileResource and Entity objects with their mocked
    counterpart (MockedFileResource, MockedEntity). Can be used to test methods with params in their signature that are
    called by the VIKTOR platform (e.g. view methods, button methods).

    Example:

    .. code-block:: python

        import unittest
        import viktor as vkt

        from app.my_entity.controller import MyEntityController

        class TestMyEntityController(unittest.TestCase):
            def test_button_method(self):
                // provide the params manually...
                params_dict = {\'number\': 1, \'entity\': 2, \'file\': 3}

                // or from a JSON file...
                params_dict = vkt.File.from_path("path to my JSON file")

                mocked_params = vkt.testing.mock_params(
                    params, MyEntityController.parametrization,
                    entities={2: vkt.testing.MockedEntity(entity_id=2, name="My Entity")}
                    file_resources={3: vkt.testing.MockedFileResource(vkt.File.from_data("content"), "file.txt")},
                )

                MyEntityController().button_method(mocked_params)

    Deserialization only affects the raw values associated with the following fields:

      - DateField
      - EntityOptionField
      - ChildEntityOptionField
      - SiblingEntityOptionField
      - EntityMultiSelectField
      - ChildEntityMultiSelectField
      - SiblingEntityMultiSelectField
      - GeoPointField
      - GeoPolylineField
      - GeoPolygonField
      - FileField
      - MultiFileField

    :param params: Plain dict or JSON file (with serialized params) to be converted to the (deserialized) params.
    :param parametrization: Parametrization corresponding to the params.
    :param file_resources: Maps FileResource source id in params to mocked file resource. If source id is not in
     file_resources, a default MockedFileResource (with default filename and File) is returned.
    :param entities: Maps entity id in params to mocked entity. If entity id is not in entities, a default MockedEntity
     is returned.
    '''
def mock_View(controller: type[ViktorController]) -> Callable:
    """ ::version(v13.3.0)

    Decorator that can be used to mock @View decorators (any subclass of :class:`viktor.views.View`), to facilitate
    easier testing of view methods.

    Example:

    .. code-block:: python

        import unittest
        import viktor as vkt

        from app.my_entity.controller import MyEntityController

        class TestMyEntityController(unittest.TestCase):
            @vkt.testing.mock_View(MyEntityController)
            def test_geometry_view(self):
                params = ...
                geometry_result = MyEntityController().geometry_view(params=params)
                self.assertIsInstance(geometry_result.geometry, vkt.TransformableObject)
                self.assertEqual(geometry_result.labels, ...)

    :param controller: Controller class on which the @View decorator should be mocked
    """
def mock_SciaAnalysis(get_engineering_report: Sequence[BytesIO | File] | BytesIO | File = None, get_updated_esa_model: Sequence[BytesIO | File] | BytesIO | File = None, get_xml_output_file: Sequence[BytesIO | File] | BytesIO | File = None) -> Callable:
    """ ::version(v13.3.0)

    Decorator that can be used to mock :class:`viktor.external.scia.SciaAnalysis`, to facilitate easier testing.

    Example:

    .. code-block:: python

        import unittest
        import viktor as vkt

        from app.my_entity.controller import MyEntityController

        class TestMyEntityController(unittest.TestCase):
            @vkt.testing.mock_SciaAnalysis(
                get_engineering_report=vkt.File.from_path(Path(__file__).parent / 'test_file.pdf'),
                get_updated_esa_model=vkt.File.from_path(Path(__file__).parent / 'test_file.esa'),
                get_xml_output_file=vkt.File.from_path(Path(__file__).parent / 'test_output.xml')
            )
            def test_scia_analysis(self):
                MyEntityController().scia_analysis()

    For all parameters the following holds:
        - If a Sequence type is provided, the next entry is returned for each corresponding method call. When a call is
          performed on a depleted iterable, an Exception is raised.
        - If a single object is provided, the object is returned each time the corresponding method is called
          (endlessly).
        - If None is provided (default), a default File/BytesIO object (with empty content) is returned each time the
          corresponding method is called (endlessly).

    :param get_engineering_report: Return value of SciaAnalysis.get_engineering_report.
    :param get_updated_esa_model: Return value of SciaAnalysis.get_updated_esa_model.
    :param get_xml_output_file: Return value of SciaAnalysis.get_xml_output_file.
    """
def mock_DSettlementAnalysis(get_output_file: dict[str, Sequence[BytesIO | File] | BytesIO | File] = None, get_sld_file: Sequence[StringIO | File] | StringIO | File = None) -> Callable:
    """ ::version(v13.5.0)

    Decorator that can be used to mock :class:`viktor.external.dsettlement.DSettlementAnalysis`, to facilitate 
    easier testing.

    Example:

    .. code-block:: python

        import unittest
        import viktor as vkt

        from app.my_entity_type.controller import MyEntityTypeController

        class TestMyEntityTypeController(unittest.TestCase):
            @vkt.testing.mock_DSettlementAnalysis(get_output_file={
                '.sld': vkt.File.from_path(Path(__file__).parent / 'test_output.sld'),
                '.slo': vkt.File.from_path(Path(__file__).parent / 'test_output.slo')
            })
            def test_dsettlement_analysis(self):
                MyEntityTypeController().dsettlement_analysis()

    For all parameters the following holds:
        - If a Sequence type is provided, the next entry is returned for each corresponding method call. When a call is
          performed on a depleted iterable, an Exception is raised.
        - If a single object is provided, the object is returned each time the corresponding method is called
          (endlessly).
        - If None is provided (default), a default File or StringIO/BytesIO object (with empty content) is returned 
          each time the corresponding method is called (endlessly).

    :param get_output_file: Return value of DSettlementAnalysis.get_output_file.
    :param get_sld_file: Return value of DSettlementAnalysis.get_sld_file.
    """
def mock_DSheetPilingAnalysis(get_output_file: dict[str, Sequence[BytesIO | File] | BytesIO | File] = None) -> Callable:
    """ ::version(v13.5.0)

    Decorator that can be used to mock :class:`viktor.external.dsheetpiling.DSheetPilingAnalysis`, to facilitate easier
    testing.

    Example:

    .. code-block:: python

        import unittest
        import viktor as vkt
        
        from app.my_entity_type.controller import MyEntityTypeController

        class TestMyEntityTypeController(unittest.TestCase):
            @vkt.testing.mock_DSheetPilingAnalysis(get_output_file={
                '.shd': vkt.File.from_path(Path(__file__).parent / 'test_output.shd'),
                '.shl': vkt.File.from_path(Path(__file__).parent / 'test_output.shl'),
                '.shs': vkt.File.from_path(Path(__file__).parent / 'test_output.shs'),
                '.sho': vkt.File.from_path(Path(__file__).parent / 'test_output.sho')
            })
            def test_dsheetpiling_analysis(self):
                MyEntityTypeController().dsheetpiling_analysis()

    For all parameters the following holds:
        - If a Sequence type is provided, the next entry is returned for each corresponding method call. When a call is
          performed on a depleted iterable, an Exception is raised.
        - If a single object is provided, the object is returned each time the corresponding method is called
          (endlessly).
        - If None is provided (default), a default File/BytesIO object (with empty content) is returned each time the
          corresponding method is called (endlessly).

    :param get_output_file: Return value of DSheetPilingAnalysis.get_output_file.
    """
def mock_DStabilityAnalysis(get_output_file: dict[str, Sequence[File] | File] = None) -> Callable:
    """ ::version(v13.5.0)

    Decorator that can be used to mock :class:`viktor.external.dstability.DStabilityAnalysis`, to facilitate easier
    testing.

    Example:

    .. code-block:: python

        import unittest
        import viktor as vkt
        
        from app.my_entity_type.controller import MyEntityTypeController

        class TestMyEntityTypeController(unittest.TestCase):
            @vkt.testing.mock_DStabilityAnalysis(get_output_file={
                '.stix': vkt.File.from_path(Path(__file__).parent / 'test_output.stix')
            })
            def test_dstability_analysis(self):
                MyEntityTypeController().dstability_analysis()

    For all parameters the following holds:
        - If a Sequence type is provided, the next entry is returned for each corresponding method call. When a call is
          performed on a depleted iterable, an Exception is raised.
        - If a single object is provided, the object is returned each time the corresponding method is called
          (endlessly).
        - If None is provided (default), a default File object (with empty content) is returned each time the
          corresponding method is called (endlessly).

    :param get_output_file: Return value of DStabilityAnalysis.get_output_file.
    """
def mock_DGeoStabilityAnalysis(get_output_file: dict[str, Sequence[BytesIO | File] | BytesIO | File] = None) -> Callable:
    """ ::version(v13.5.0)

    Decorator that can be used to mock :class:`viktor.external.dgeostability.DGeoStabilityAnalysis`, to facilitate
    easier testing.

    Example:

    .. code-block:: python

        import unittest
        import viktor as vkt
        
        from app.my_entity_type.controller import MyEntityTypeController

        class TestMyEntityTypeController(unittest.TestCase):
            @vkt.testing.mock_DGeoStabilityAnalysis(get_output_file={
                '.sto': vkt.File.from_path(Path(__file__).parent / 'test_output.sto')
            })
            def test_dgeostability_analysis(self):
                MyEntityTypeController().dgeostability_analysis()

    For all parameters the following holds:
        - If a Sequence type is provided, the next entry is returned for each corresponding method call. When a call is
          performed on a depleted iterable, an Exception is raised.
        - If a single object is provided, the object is returned each time the corresponding method is called
          (endlessly).
        - If None is provided (default), a default File/BytesIO object (with empty content) is returned each time the
          corresponding method is called (endlessly).

    :param get_output_file: Return value of DGeoStabilityAnalysis.get_output_file.
    """
def mock_DFoundationsAnalysis(get_output_file: dict[str, Sequence[BytesIO | File] | BytesIO | File] = None) -> Callable:
    """ ::version(v13.5.0)

    Decorator that can be used to mock :class:`viktor.external.dfoundations.DFoundationsAnalysis`, to facilitate easier
    testing.

    Example:

    .. code-block:: python

        import unittest
        import viktor as vkt
        
        from app.my_entity_type.controller import MyEntityTypeController

        class TestMyEntityTypeController(unittest.TestCase):
            @vkt.testing.mock_DFoundationsAnalysis(get_output_file={
                '.fod': vkt.File.from_path(Path(__file__).parent / 'test_output.fod'),
                '.fos': vkt.File.from_path(Path(__file__).parent / 'test_output.fos')
            })
            def test_dfoundations_analysis(self):
                MyEntityTypeController().dfoundations_analysis()

    For all parameters the following holds:
        - If a Sequence type is provided, the next entry is returned for each corresponding method call. When a call is
          performed on a depleted iterable, an Exception is raised.
        - If a single object is provided, the object is returned each time the corresponding method is called
          (endlessly).
        - If None is provided (default), a default File/BytesIO object (with empty content) is returned each time the
          corresponding method is called (endlessly).

    :param get_output_file: Return value of DFoundationsAnalysis.get_output_file.
    """
def mock_GRLWeapAnalysis(get_output_file: Sequence[BytesIO | File] | BytesIO | File = None) -> Callable:
    """ ::version(v13.5.0)

    Decorator that can be used to mock :class:`viktor.external.grlweap.GRLWeapAnalysis`, to facilitate easier testing.

    Example:

    .. code-block:: python

        import unittest
        import viktor as vkt
        
        from app.my_entity_type.controller import MyEntityTypeController

        class TestMyEntityTypeController(unittest.TestCase):
            @vkt.testing.mock_GRLWeapAnalysis(
                get_output_file=vkt.File.from_path(Path(__file__).parent / 'test_output.GWO')
            )
            def test_grlweap_analysis(self):
                MyEntityTypeController().grlweap_analysis()

    For all parameters the following holds:
        - If a Sequence type is provided, the next entry is returned for each corresponding method call. When a call is
          performed on a depleted iterable, an Exception is raised.
        - If a single object is provided, the object is returned each time the corresponding method is called
          (endlessly).
        - If None is provided (default), a default File/BytesIO object (with empty content) is returned each time the
          corresponding method is called (endlessly).

    :param get_output_file: Return value of GRLWeapAnalysis.get_output_file.
    """
def mock_IdeaRcsAnalysis(get_output_file: Sequence[BytesIO | File] | BytesIO | File = None, get_idea_rcs_file: Sequence[BytesIO | File] | BytesIO | File = None) -> Callable:
    """ ::version(v13.5.0)

    Decorator that can be used to mock :class:`viktor.external.idea_rcs.IdeaRcsAnalysis`, to facilitate easier testing.

    Example:

    .. code-block:: python

        import unittest
        import viktor as vkt

        from app.my_entity_type.controller import MyEntityTypeController

        class TestMyEntityTypeController(unittest.TestCase):
            @vkt.testing.mock_IdeaRcsAnalysis(
                get_output_file=vkt.File.from_path(Path(__file__).parent / 'test_output.xml'),
                get_idea_rcs_file=vkt.File.from_path(Path(__file__).parent / 'test_rcs.ideaRcs')
            )
            def test_idea_rcs_analysis(self):
                MyEntityTypeController().idea_rcs_analysis()

    For all parameters the following holds:
        - If a Sequence type is provided, the next entry is returned for each corresponding method call. When a call is
          performed on a depleted iterable, an Exception is raised.
        - If a single object is provided, the object is returned each time the corresponding method is called
          (endlessly).
        - If None is provided (default), a default File/BytesIO object (with empty content) is returned each time the
          corresponding method is called (endlessly).

    :param get_output_file: Return value of IdeaRcsAnalysis.get_output_file.
    :param get_idea_rcs_file: Return value of IdeaRcsAnalysis.get_idea_rcs_file.
    """
def mock_RobotAnalysis(get_model_file: Sequence[File] | File = None, get_results: Sequence[dict] | dict = None) -> Callable:
    """ ::version(v13.5.0)

    Decorator that can be used to mock :class:`viktor.external.robot.RobotAnalysis`, to facilitate
    easier testing.

    Example:

    .. code-block:: python

        import unittest
        import viktor as vkt

        from app.my_entity_type.controller import MyEntityTypeController

        class TestMyEntityTypeController(unittest.TestCase):
            @vkt.testing.mock_RobotAnalysis(
                get_model_file=vkt.File.from_path(Path(__file__).parent / 'test_model.rtd'),
                get_results={'bar_forces': {...}, ...}
            )
            def test_robot_analysis(self):
                MyEntityTypeController().robot_analysis()

    For all parameters the following holds:
        - If a Sequence type is provided, the next entry is returned for each corresponding method call. When a call is
          performed on a depleted iterable, an Exception is raised.
        - If a single object is provided, the object is returned each time the corresponding method is called
          (endlessly).
        - If None is provided (default), a default File/dict object (with empty content) is returned each time the
          corresponding method is called (endlessly).

    :param get_model_file: Return value of RobotAnalysis.get_model_file.
    :param get_results: Return value of RobotAnalysis.get_results.
    """
def mock_AxisVMAnalysis(get_model_file: Sequence[BytesIO | File] | BytesIO | File = None, get_result_file: Sequence[BytesIO | File] | BytesIO | File = None, get_results: Sequence[dict] | dict = None) -> Callable:
    """ ::version(v13.5.0)

    Decorator that can be used to mock :class:`viktor.external.axisvm.AxisVMAnalysis`, to facilitate
    easier testing.

    Example:

    .. code-block:: python

        import unittest
        import viktor as vkt

        from app.my_entity_type.controller import MyEntityTypeController

        class TestMyEntityTypeController(unittest.TestCase):
            @vkt.testing.mock_AxisVMAnalysis(
                get_model_file=vkt.File.from_path(Path(__file__).parent / 'test_model.axs'),
                get_result_file=vkt.File.from_path(Path(__file__).parent / 'test_model.axe'),
                get_results={'Forces': ...}
            )
            def test_axisvm_analysis(self):
                MyEntityTypeController().axisvm_analysis()

    For all parameters the following holds:
        - If a Sequence type is provided, the next entry is returned for each corresponding method call. When a call is
          performed on a depleted iterable, an Exception is raised.
        - If a single object is provided, the object is returned each time the corresponding method is called
          (endlessly).
        - If None is provided (default), a default File/BytesIO/dict object (with empty content) is returned each time
          the corresponding method is called (endlessly).

    :param get_model_file: Return value of AxisVMAnalysis.get_model_file.
    :param get_result_file: Return value of AxisVMAnalysis.get_result_file.
    :param get_results: Return value of AxisVMAnalysis.get_results.
    """
def mock_GenericAnalysis(get_output_file: dict[str, Sequence[BytesIO | File] | BytesIO | File] = None) -> Callable:
    """ ::version(v13.5.0)

    Decorator that can be used to mock :class:`viktor.external.generic.GenericAnalysis`, to facilitate
    easier testing.

    Example:

    .. code-block:: python

        import unittest
        import viktor as vkt

        from app.my_entity_type.controller import MyEntityTypeController

        class TestMyEntityTypeController(unittest.TestCase):
            @vkt.testing.mock_GenericAnalysis(get_output_file={
                'data.out': vkt.File.from_path(Path(__file__).parent / 'data.out'),
                'info.log': vkt.File.from_path(Path(__file__).parent / 'info.log')
            })
            def test_generic_analysis(self):
                MyEntityTypeController().generic_analysis()

    For all parameters the following holds:
        - If a Sequence type is provided, the next entry is returned for each corresponding method call. When a call is
          performed on a depleted iterable, an Exception is raised.
        - If a single object is provided, the object is returned each time the corresponding method is called
          (endlessly).
        - If None is provided (default), a default File or BytesIO object (with empty content) is returned each time
          the corresponding method is called (endlessly).

    :param get_output_file: Return value of GenericAnalysis.get_output_file.
    """
def mock_MatlabAnalysis(get_output_file: dict[str, Sequence[BytesIO | File] | BytesIO | File] = None) -> Callable:
    """ ::version(14.17.0)

    Decorator that can be used to mock :class:`viktor.external.matlab.MatlabAnalysis`, to facilitate
    easier testing.

    Example:

    .. code-block:: python

        import unittest
        import viktor as vkt

        from app.my_entity_type.controller import MyEntityTypeController

        class TestMyEntityTypeController(unittest.TestCase):
            @vkt.testing.mock_MatlabAnalysis(get_output_file={
                'data.out': vkt.File.from_path(Path(__file__).parent / 'data.out'),
                'info.log': vkt.File.from_path(Path(__file__).parent / 'info.log')
            })
            def test_matlab_analysis(self):
                MyEntityTypeController().matlab_analysis()

    For all parameters the following holds:
        - If a Sequence type is provided, the next entry is returned for each corresponding method call. When a call is
          performed on a depleted iterable, an Exception is raised.
        - If a single object is provided, the object is returned each time the corresponding method is called
          (endlessly).
        - If None is provided (default), a default File or BytesIO object (with empty content) is returned each time
          the corresponding method is called (endlessly).

    :param get_output_file: Return value of MatlabAnalysis.get_output_file.
    """
def mock_DynamoAnalysis(get_output_file: dict[str, Sequence[BytesIO | File] | BytesIO | File] = None) -> Callable:
    """ ::version(14.17.0)
    Decorator that can be used to mock :class:`viktor.external.dynamo.DynamoAnalysis`, to facilitate
    easier testing.

    Example:

    .. code-block:: python

        import unittest
        import viktor as vkt
        
        from app.my_entity_type.controller import MyEntityTypeController

        class TestMyEntityTypeController(unittest.TestCase):
            @vkt.testing.mock_DynamoAnalysis(get_output_file={
                'data.out': vkt.File.from_path(Path(__file__).parent / 'data.out'),
                'info.log': vkt.File.from_path(Path(__file__).parent / 'info.log')
            })
            def test_dynamo_analysis(self):
                MyEntityTypeController().dynamo_analysis()

    For all parameters the following holds:
        - If a Sequence type is provided, the next entry is returned for each corresponding method call. When a call is
          performed on a depleted iterable, an Exception is raised.
        - If a single object is provided, the object is returned each time the corresponding method is called
          (endlessly).
        - If None is provided (default), a default File or BytesIO object (with empty content) is returned each time
          the corresponding method is called (endlessly).

    :param get_output_file: Return value of DynamoAnalysis.get_output_file.
    """
def mock_PythonAnalysis(get_output_file: dict[str, Sequence[File] | File] = None) -> Callable:
    """ ::version(14.17.0)

    Decorator that can be used to mock :class:`viktor.external.python.PythonAnalysis`, to facilitate
    easier testing.

    Example:

    .. code-block:: python

        import unittest
        import viktor as vkt

        from app.my_entity_type.controller import MyEntityTypeController

        class TestMyEntityTypeController(unittest.TestCase):
            @vkt.testing.mock_PythonAnalysis(get_output_file={
                'data.out': vkt.File.from_path(Path(__file__).parent / 'data.out'),
                'info.log': vkt.File.from_path(Path(__file__).parent / 'info.log')
            })
            def test_python_analysis(self):
                MyEntityTypeController().python_analysis()

    For all parameters the following holds:
        - If a Sequence type is provided, the next entry is returned for each corresponding method call. When a call is
          performed on a depleted iterable, an Exception is raised.
        - If a single object is provided, the object is returned each time the corresponding method is called
          (endlessly).
        - If None is provided (default), a default File object (with empty content) is returned each time
          the corresponding method is called (endlessly).

    :param get_output_file: Return value of PythonAnalysis.get_output_file.
    """
def mock_ETABSAnalysis(get_output_file: dict[str, Sequence[File] | File] = None) -> Callable:
    """ ::version(14.17.0)

    Decorator that can be used to mock :class:`viktor.external.etabs.ETABSAnalysis`, to facilitate
    easier testing.

    Example:

    .. code-block:: python

        import unittest
        import viktor as vkt

        from app.my_entity_type.controller import MyEntityTypeController

        class TestMyEntityTypeController(unittest.TestCase):
            @vkt.testing.mock_ETABSAnalysis(get_output_file={
                'data.out': vkt.File.from_path(Path(__file__).parent / 'data.out'),
                'info.log': vkt.File.from_path(Path(__file__).parent / 'info.log')
            })
            def test_etabs_analysis(self):
                MyEntityTypeController().etabs_analysis()

    For all parameters the following holds:
        - If a Sequence type is provided, the next entry is returned for each corresponding method call. When a call is
          performed on a depleted iterable, an Exception is raised.
        - If a single object is provided, the object is returned each time the corresponding method is called
          (endlessly).
        - If None is provided (default), a default File object (with empty content) is returned each time
          the corresponding method is called (endlessly).

    :param get_output_file: Return value of ETABSAnalysis.get_output_file.
    """
def mock_PlaxisAnalysis(get_output_file: dict[str, Sequence[File] | File] = None) -> Callable:
    """ ::version(14.17.0)

    Decorator that can be used to mock :class:`viktor.external.plaxis.PlaxisAnalysis`, to facilitate
    easier testing.

    Example:

    .. code-block:: python

        import unittest
        import viktor as vkt

        from app.my_entity_type.controller import MyEntityTypeController

        class TestMyEntityTypeController(unittest.TestCase):
            @vkt.testing.mock_PlaxisAnalysis(get_output_file={
                'data.out': vkt.File.from_path(Path(__file__).parent / 'data.out'),
                'info.log': vkt.File.from_path(Path(__file__).parent / 'info.log')
            })
            def test_plaxis_analysis(self):
                MyEntityTypeController().plaxis_analysis()

    For all parameters the following holds:
        - If a Sequence type is provided, the next entry is returned for each corresponding method call. When a call is
          performed on a depleted iterable, an Exception is raised.
        - If a single object is provided, the object is returned each time the corresponding method is called
          (endlessly).
        - If None is provided (default), a default File object (with empty content) is returned each time
          the corresponding method is called (endlessly).

    :param get_output_file: Return value of PlaxisAnalysis.get_output_file.
    """
def mock_RevitAnalysis(get_output_file: dict[str, Sequence[File] | File] = None) -> Callable:
    """ ::version(14.17.0)

    Decorator that can be used to mock :class:`viktor.external.revit.RevitAnalysis`, to facilitate
    easier testing.

    Example:

    .. code-block:: python

        import unittest
        import viktor as vkt

        from app.my_entity_type.controller import MyEntityTypeController

        class TestMyEntityTypeController(unittest.TestCase):
            @vkt.testing.mock_RevitAnalysis(get_output_file={
                'data.out': vkt.File.from_path(Path(__file__).parent / 'data.out'),
                'info.log': vkt.File.from_path(Path(__file__).parent / 'info.log')
            })
            def test_revit_analysis(self):
                MyEntityTypeController().revit_analysis()

    For all parameters the following holds:
        - If a Sequence type is provided, the next entry is returned for each corresponding method call. When a call is
          performed on a depleted iterable, an Exception is raised.
        - If a single object is provided, the object is returned each time the corresponding method is called
          (endlessly).
        - If None is provided (default), a default File object (with empty content) is returned each time
          the corresponding method is called (endlessly).

    :param get_output_file: Return value of RevitAnalysis.get_output_file.
    """
def mock_SAP2000Analysis(get_output_file: dict[str, Sequence[File] | File] = None) -> Callable:
    """ ::version(14.17.0)

    Decorator that can be used to mock :class:`viktor.external.sap2000.SAP2000Analysis`, to facilitate
    easier testing.

    Example:

    .. code-block:: python

        import unittest
        import viktor as vkt

        from app.my_entity_type.controller import MyEntityTypeController

        class TestMyEntityTypeController(unittest.TestCase):
            @vkt.testing.mock_SAP2000Analysis(get_output_file={
                'data.out': vkt.File.from_path(Path(__file__).parent / 'data.out'),
                'info.log': vkt.File.from_path(Path(__file__).parent / 'info.log')
            })
            def test_sap2000_analysis(self):
                MyEntityTypeController().sap2000_analysis()

    For all parameters the following holds:
        - If a Sequence type is provided, the next entry is returned for each corresponding method call. When a call is
          performed on a depleted iterable, an Exception is raised.
        - If a single object is provided, the object is returned each time the corresponding method is called
          (endlessly).
        - If None is provided (default), a default File object (with empty content) is returned each time
          the corresponding method is called (endlessly).

    :param get_output_file: Return value of SAP2000Analysis.get_output_file.
    """
def mock_TeklaAnalysis(get_output_file: dict[str, Sequence[File] | File] = None) -> Callable:
    """ ::version(14.17.0)

    Decorator that can be used to mock :class:`viktor.external.tekla.TeklaAnalysis`, to facilitate
    easier testing.

    Example:

    .. code-block:: python

        import unittest
        import viktor as vkt

        from app.my_entity_type.controller import MyEntityTypeController

        class TestMyEntityTypeController(unittest.TestCase):
            @vkt.testing.mock_TeklaAnalysis(get_output_file={
                'data.out': vkt.File.from_path(Path(__file__).parent / 'data.out'),
                'info.log': vkt.File.from_path(Path(__file__).parent / 'info.log')
            })
            def test_tekla_analysis(self):
                MyEntityTypeController().tekla_analysis()

    For all parameters the following holds:
        - If a Sequence type is provided, the next entry is returned for each corresponding method call. When a call is
          performed on a depleted iterable, an Exception is raised.
        - If a single object is provided, the object is returned each time the corresponding method is called
          (endlessly).
        - If None is provided (default), a default File object (with empty content) is returned each time
          the corresponding method is called (endlessly).

    :param get_output_file: Return value of TeklaAnalysis.get_output_file.
    """
CellValue = str | int | float | bool

def mock_Excel(get_named_cell_result: dict[str, Sequence[CellValue] | CellValue] = None, get_direct_cell_result: dict[tuple[str, str, int], Sequence[CellValue] | CellValue] = None, get_filled_template: Sequence[File] | File = None) -> Callable:
    ''' ::version(v13.5.0)

    Decorator that can be used to mock :class:`viktor.external.excel.Excel`, to facilitate
    easier testing.

    Example:

    .. code-block:: python

        import unittest
        import viktor as vkt

        from app.my_entity_type.controller import MyEntityTypeController

        class TestMyEntityTypeController(unittest.TestCase):
            @vkt.testing.mock_Excel(
                get_filled_template=vkt.File.from_path(Path(__file__).parent / \'test_model.xlsx\'),
                get_named_cell_result={"cell name": 5.5},
                get_direct_cell_result={
                    ("Sheet1", "A", 5): "cell value",
                    ("Sheet2", "B", 1): 1.4,
                }
            )
            def test_excel_analysis(self):
                MyEntityTypeController().excel_analysis()

    For all parameters the following holds:
        - If a Sequence type is provided, the next entry is returned for each corresponding method call. When a call is
          performed on a depleted iterable, an Exception is raised.
        - If a single object is provided, the object is returned each time the corresponding method is called
          (endlessly).
        - If None is provided (default), a default File object (with empty content) is returned for the template,
          whereas None is returned for the cell values, each time the corresponding method is called (endlessly).

    :param get_named_cell_result: Return value of Excel.get_named_cell_result.
    :param get_direct_cell_result: Return value of Excel.get_direct_cell_result.
    :param get_filled_template: Return value of Excel.get_filled_template.
    '''
def mock_RFEMAnalysis(get_model: Sequence[File | BytesIO] | File | BytesIO = None, get_result: dict[int, Sequence[File | BytesIO] | File | BytesIO] = None) -> Callable:
    """ ::version(v13.5.0)

    Decorator that can be used to mock :class:`viktor.external.rfem.RFEMAnalysis`, to facilitate
    easier testing.

    Example:

    .. code-block:: python

        import unittest
        import viktor as vkt

        from app.my_entity_type.controller import MyEntityTypeController

        class TestMyEntityTypeController(unittest.TestCase):
            @vkt.testing.mock_RFEMAnalysis(
                get_model=vkt.File.from_path(Path(__file__).parent / 'test_model.rfx')
                get_result={
                    3: vkt.File.from_path(Path(__file__).parent / 'load_case_3.json'),
                    5: vkt.File.from_path(Path(__file__).parent / 'load_case_5.json')
                }
            )
            def test_rfem_analysis(self):
                MyEntityTypeController().rfem_analysis()
            })
            def test_rfem_analysis(self):
                MyEntityTypeController().rfem_analysis()

    For all parameters the following can be provided:
        - If a Sequence type is provided, the next entry is returned for each corresponding method call. When a call is
          performed on a depleted iterable, an Exception is raised.
        - If a single object is provided, the object is returned each time the corresponding method is called
          (endlessly).
        - If None is provided (default), a default BytesIO/File object (with empty content) is returned each time
          the corresponding method is called (endlessly).

    :param get_model: Return value of RFEMAnalysis.get_model.
    :param get_result: Return value of RFEMAnalysis.get_result.
    """
