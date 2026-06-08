import abc
import datetime
import os
import pandas as pd
import plotly.graph_objects as go
from .api_v1 import FileResource
from .core import Color, File, _Result
from .external.autodesk import AutodeskFile
from .geometry import GeoPoint, GeoPolygon, GeoPolyline, Point, TransformableObject
from _typeshed import Incomplete
from abc import ABC
from collections import OrderedDict
from enum import Enum
from io import BytesIO, StringIO
from pandas.io.formats.style import Styler
from typing import Any, Callable, Literal, Sequence

__all__ = ['AutodeskResult', 'AutodeskView', 'DataGroup', 'DataItem', 'DataResult', 'DataStatus', 'DataView', 'GeoJSONAndDataResult', 'GeoJSONAndDataView', 'GeoJSONResult', 'GeoJSONView', 'GeometryAndDataResult', 'GeometryAndDataView', 'GeometryResult', 'GeometryView', 'IFCAndDataResult', 'IFCAndDataView', 'IFCResult', 'IFCView', 'ImageAndDataResult', 'ImageAndDataView', 'ImageResult', 'ImageView', 'InteractionEvent', 'Label', 'MapAndDataResult', 'MapAndDataView', 'MapCircle', 'MapEntityLink', 'MapFeature', 'MapLabel', 'MapLegend', 'MapLine', 'MapPoint', 'MapPolygon', 'MapPolyline', 'MapResult', 'MapView', 'PDFResult', 'PDFView', 'PlotlyAndDataResult', 'PlotlyAndDataView', 'PlotlyResult', 'PlotlyView', 'Summary', 'SummaryItem', 'TableCell', 'TableHeader', 'TableResult', 'TableView', 'WebAndDataResult', 'WebAndDataView', 'WebResult', 'WebView']

class DataStatus(Enum):
    """Enumeration of statuses to annotate a DataItem."""
    INFO: DataStatus
    SUCCESS: DataStatus
    WARNING: DataStatus
    ERROR: DataStatus

class DataItem:
    '''
    Constructs an entry that can be used as input of a DataGroup, to fill the data view with results.

    The data view is dynamic, which means that a DataItem itself can consist of another DataGroup as subgroup. Both
    examples are demonstrated below.

    Example single entry:

    .. code-block:: python

        result = "I am a great result"
        item = DataItem(\'output 1\', result)

    Example subgroup:

    .. code-block:: python

        result = "I am a great result"
        item = DataItem(\'output 1\', result, subgroup=DataGroup(
            output11=DataItem(\'output 1.1\', "I can also be a numeric result"),
            output12=DataItem(\'output 1.2\', 123)
        ))

    The prefix / suffix can potentially change with every call. However, when the result is used in the Summary, the
    prefix / suffix of the DataItem should be equal to the prefix / suffix of the SummaryItem to maintain a consistent
    database.
    '''
    label: Incomplete
    value: Incomplete
    prefix: Incomplete
    suffix: Incomplete
    status: Incomplete
    status_message: Incomplete
    explanation_label: Incomplete
    def __init__(self, label: str, value: str | float = None, subgroup: DataGroup = None, *, prefix: str = '', suffix: str = '', number_of_decimals: int = None, status: DataStatus = ..., status_message: str = '', explanation_label: str = '') -> None:
        """
        :param label: Description of the value which is shown. e.g: 'Uc bending'
        :param value: Value of the data. e.g: 0.9
        :param subgroup: Optional DataItems grouped together in a DataGroup underneath this DataItem. Maximum depth = 3
        :param prefix: E.g: €. Should be equal to the prefix of the SummaryItem if linked.
        :param suffix: E.g: N. Should be equal to the suffix of the SummaryItem if linked.
        :param number_of_decimals: Number of decimals with which the value is rounded for display.
        :param status: Status of value. This controls the formatting of the status_message:

           - status=DataStatus.INFO: black text
           - status=DataStatus.SUCCESS: green text
           - status=DataStatus.WARNING: orange text
           - status=DataStatus.ERROR: red text

        :param status_message: Message which will be shown underneath the value. Color can be formatted with status.
        :param explanation_label: Optional text which is placed between the label and the value.
                                  Could for instance be used for a calculation.

        :raises TypeError: if number_of_decimals is used on a non-numeric value.
        """
    @property
    def subgroup(self) -> DataGroup: ...

class DataGroup(dict):
    """
    Container for DataItems (max. 100).

    DataItems can be added with or without a keyword argument. Keywords are
    required when you want to use a DataItem in the summary (for lookup).

    Example:

    .. code-block:: python

        DataGroup(
            DataItem('a', 1),
            DataItem('b', 2),
            output_c=DataItem('c', 3),  # 'output_c' can be used in the entity summary
            output_d=DataItem('d', 4),  # 'output_d' can be used in the entity summary
        )

    **(new in v14.22.0)** Append items to an existing data group using `DataGroup.add()`:

    .. code-block:: python

        d = DataGroup(
            DataItem('a', 1),
        )
        d.add(DataItem('b', 2))
        d.add(DataItem('c', 3), DataItem('d', 4))

    """
    def __init__(self, *args: DataItem, **kwargs: DataItem) -> None:
        """
        :param args: DataItem entries.
        :param kwargs: Keyworded DataItem entries.
        :raises:
            - AttributeError when more than 100 DataItems are used
        """
    def add(self, *items: DataItem) -> None:
        """ ::version(v14.22.0)

        Add one or more DataItems to an existing DataGroup.
        """
    @classmethod
    def from_data_groups(cls, groups: list['DataGroup']) -> DataGroup:
        """
        Constructs a combined DataGroup object from a list of individual DataGroup entries.

        Note that is not possible to have multiple DataGroups that share a specific key for a DataItem, e.g. the
        following will result in an error:

        .. code-block:: python

            d1 = DataGroup(output_a=DataItem(...))
            d2 = DataGroup(output_a=DataItem(...))
            d3 = DataGroup.from_data_groups([d1, d2])  # raises KeyError
        """

class MapEntityLink:
    """
    Represents a link between a feature in a MapView and a specific entity.

    Example usage:

    .. code-block:: python

        gef_link = MapEntityLink('GEF x', gef_entity_id)
        gef_marker = MapPoint(51.99311570849245, 4.385752379894256, entity_links=[gef_link])
    """
    def __init__(self, label: str, entity_id: int) -> None:
        """
        :param label: text which is shown to the user.
        :param entity_id: id of the linked entity.
        """

class MapFeature(ABC, metaclass=abc.ABCMeta):
    """
    Base class for features that can be shown in a MapView.
    See the documentation of the subclasses for example implementations.
    """
    def __init__(self, *, title: str = None, description: str = None, color: Color = ..., entity_links: list[MapEntityLink] = None, identifier: int | str = None) -> None:
        """
        :param title: Title of a clickable map feature.
        :param description: Description of a clickable map feature.
        :param color: Specifies the color of the map feature.
        :param entity_links: When clicking on the map feature, links towards multiple entities can be shown.
        :param identifier: feature identifier ::version(v13.2.0)
        """

class MapPoint(MapFeature):
    """
    Represents a point on the Earth's surface described by a latitude/longitude coordinate pair.

    Example usage:

    .. code-block:: python

         marker = MapPoint(51.99311570849245, 4.385752379894256)
    """
    def __init__(self, lat: float, lon: float, alt: float = 0, *, icon: str = None, size: Literal['small', 'medium', 'large'] = 'medium', **kwargs: Any) -> None:
        '''
        :param lat: Latitude.
        :param lon: Longitude.
        :param alt: Altitude.
        :param icon: icon to be shown (default: "pin"). See below for all possible icons.
        :param size: size of the marker ("small" | "medium" | "large") ::version(v14.5.0).
        :param kwargs: See :class:`MapFeature` for possible kwargs.

        List of icons:

            - arrow-down: |arrow-down|
            - arrow-left: |arrow-left|
            - arrow-right: |arrow-right|
            - arrow-up: |arrow-up|
            - chevron-down: |chevron-down|
            - chevron-left: |chevron-left|
            - chevron-right: |chevron-right|
            - chevron-up: |chevron-up|
            - circle: |circle|
            - circle-filled: |circle-filled|
            - cross: |cross|
            - diamond: |diamond|
            - diamond-horizontal: |diamond-horizontal|
            - drop: |drop|
            - exclamation-circle: |exclamation-circle|
            - exclamation-circle-filled: |exclamation-circle-filled|
            - message: |message|
            - minus: |minus|
            - minus-circle: |minus-circle|
            - minus-circle-filled: |minus-circle-filled|
            - pin: |pin|
            - pin-add: |pin-add|
            - pin-edit: |pin-edit|
            - plus: |plus|
            - plus-circle: |plus-circle|
            - plus-circle-filled: |plus-circle-filled|
            - plus-thick: |plus-thick|
            - question-circle: |question-circle|
            - question-circle-filled: |question-circle-filled|
            - square: |square|
            - square-filled: |square-filled|
            - star: |star|
            - triangle: |triangle|
            - triangle-down: |triangle-down|
            - triangle-down-filled: |triangle-down-filled|
            - triangle-filled: |triangle-filled|
            - triangle-left: |triangle-left|
            - triangle-left-filled: |triangle-left-filled|
            - triangle-right: |triangle-right|
            - triangle-right-filled: |triangle-right-filled|
            - viktor: |viktor|
            - warning: |warning|
            - warning-filled: |warning-filled|
            - wye: |wye|

        .. |arrow-down| image:: ../_static/arrow-down.svg
            :height: 25px
        .. |arrow-left| image:: ../_static/arrow-left.svg
            :height: 25px
        .. |arrow-right| image:: ../_static/arrow-right.svg
            :height: 25px
        .. |arrow-up| image:: ../_static/arrow-up.svg
            :height: 25px
        .. |chevron-down| image:: ../_static/chevron-down.svg
            :height: 25px
        .. |chevron-left| image:: ../_static/chevron-left.svg
            :height: 25px
        .. |chevron-right| image:: ../_static/chevron-right.svg
            :height: 25px
        .. |chevron-up| image:: ../_static/chevron-up.svg
            :height: 25px
        .. |circle| image:: ../_static/circle.svg
            :height: 25px
        .. |circle-filled| image:: ../_static/circle-filled.svg
            :height: 25px
        .. |cross| image:: ../_static/cross.svg
            :height: 25px
        .. |diamond| image:: ../_static/diamond.svg
            :height: 25px
        .. |diamond-horizontal| image:: ../_static/diamond-horizontal.svg
            :height: 25px
        .. |drop| image:: ../_static/drop.svg
            :height: 25px
        .. |exclamation-circle| image:: ../_static/exclamation-circle.svg
            :height: 25px
        .. |exclamation-circle-filled| image:: ../_static/exclamation-circle-filled.svg
            :height: 25px
        .. |message| image:: ../_static/message.svg
            :height: 25px
        .. |minus| image:: ../_static/minus.svg
            :height: 25px
        .. |minus-circle| image:: ../_static/minus-circle.svg
            :height: 25px
        .. |minus-circle-filled| image:: ../_static/minus-circle-filled.svg
            :height: 25px
        .. |pin| image:: ../_static/pin.svg
            :height: 25px
        .. |pin-add| image:: ../_static/pin-add.svg
            :height: 25px
        .. |pin-edit| image:: ../_static/pin-edit.svg
            :height: 25px
        .. |plus| image:: ../_static/plus.svg
            :height: 25px
        .. |plus-circle| image:: ../_static/plus-circle.svg
            :height: 25px
        .. |plus-circle-filled| image:: ../_static/plus-circle-filled.svg
            :height: 25px
        .. |plus-thick| image:: ../_static/plus-thick.svg
            :height: 25px
        .. |question-circle| image:: ../_static/question-circle.svg
            :height: 25px
        .. |question-circle-filled| image:: ../_static/question-circle-filled.svg
            :height: 25px
        .. |square| image:: ../_static/square.svg
            :height: 25px
        .. |square-filled| image:: ../_static/square-filled.svg
            :height: 25px
        .. |star| image:: ../_static/star.svg
            :height: 25px
        .. |triangle| image:: ../_static/triangle.svg
            :height: 25px
        .. |triangle-down| image:: ../_static/triangle-down.svg
            :height: 25px
        .. |triangle-down-filled| image:: ../_static/triangle-down-filled.svg
            :height: 25px
        .. |triangle-filled| image:: ../_static/triangle-filled.svg
            :height: 25px
        .. |triangle-left| image:: ../_static/triangle-left.svg
            :height: 25px
        .. |triangle-left-filled| image:: ../_static/triangle-left-filled.svg
            :height: 25px
        .. |triangle-right| image:: ../_static/triangle-right.svg
            :height: 25px
        .. |triangle-right-filled| image:: ../_static/triangle-right-filled.svg
            :height: 25px
        .. |viktor| image:: ../_static/viktor.svg
            :height: 25px
        .. |warning| image:: ../_static/warning.svg
            :height: 25px
        .. |warning-filled| image:: ../_static/warning-filled.svg
            :height: 25px
        .. |wye| image:: ../_static/wye.svg
            :height: 25px
        '''
    @classmethod
    def from_geo_point(cls, point: GeoPoint, *, icon: str = None, size: Literal['small', 'medium', 'large'] = 'medium', **kwargs: Any) -> MapPoint:
        ''' Instantiates a MapPoint from the provided GeoPoint.

        :param point: GeoPoint.
        :param icon: icon to be shown (default: "pin"). For a complete list of all available markers, see
            :meth:`__init__`
        :param size: size of the marker ("small" | "medium" | "large") ::version(v14.5.0).
        :param kwargs: See :class:`MapFeature` for possible kwargs.
        '''
    @property
    def lat(self) -> float: ...
    @property
    def lon(self) -> float: ...
    @property
    def alt(self) -> float: ...

class MapPolyline(MapFeature):
    """
    Represents a polyline on the earth's surface between several latitude/longitude pairs.

    Example usage:

    .. code-block:: python

         line = MapPolyline(
            MapPoint(51.99311570849245, 4.385752379894256),
            MapPoint(52.40912125231122, 5.031738281255681),
            ...
        )
    """
    def __init__(self, *points: MapPoint, **kwargs: Any) -> None:
        """
        :param points: MapPoints with latitude and longitude pair.
        :param kwargs: See :class:`MapFeature` for possible kwargs.
        """
    @classmethod
    def from_geo_polyline(cls, polyline: GeoPolyline, **kwargs: Any) -> MapPolyline:
        """ Instantiates a MapPolyline from the provided GeoPolyline.

        :param polyline: GeoPolyline.
        :param kwargs: See :class:`MapFeature` for possible kwargs.
        """
    @property
    def points(self) -> list[MapPoint]: ...

class MapLine(MapPolyline):
    """
    Represents a line on the earth's surface between two latitude/longitude pairs.

    In case multiple line segments are to be created, a :class:`MapPolyline` may be preferred.

    Example usage:

    .. code-block:: python

         line = MapLine(
            MapPoint(51.99311570849245, 4.385752379894256),
            MapPoint(52.40912125231122, 5.031738281255681)
        )
    """
    def __init__(self, start_point: MapPoint, end_point: MapPoint, **kwargs: Any) -> None:
        """
        :param start_point: Map point with latitude and longitude pair.
        :param end_point: Map point with latitude and longitude pair.
        :param kwargs: See :class:`MapFeature` for possible kwargs.
        """
    @property
    def start_point(self) -> MapPoint: ...
    @property
    def end_point(self) -> MapPoint: ...

class MapPolygon(MapFeature):
    """
    Represents a polygon on the earth's surface formed by a set of latitude/longitude pairs.

    Example usage:

    .. code-block:: python

        polygon = MapPolygon([
            MapPoint(52.373922404495474, 5.2459716796875),
            MapPoint(52.10313118589299, 5.3997802734375),
            MapPoint(52.373922404495474, 5.57281494140625),
        ])
    """
    def __init__(self, points: list[MapPoint], *, holes: list['MapPolygon'] = None, **kwargs: Any) -> None:
        """
        :param points: Map points with latitude and longitude pair. The profile is automatically closed, so it is not
            necessary to add the start point at the end.
        :param holes: List of interior polygons which form holes in the exterior polygon.
        :param kwargs: See :class:`MapFeature` for possible kwargs.
        """
    @classmethod
    def from_geo_polygon(cls, polygon: GeoPolygon, **kwargs: Any) -> MapPolygon:
        """ Instantiates a MapPolygon from the provided GeoPolygon.

        :param polygon: GeoPolygon.
        :param kwargs: See :class:`MapFeature` for possible kwargs.
        """
    @property
    def points(self) -> list[MapPoint]: ...
    @property
    def holes(self) -> list['MapPolygon']: ...

class MapCircle(MapFeature):
    """ ::version(v14.22.0)

    Represents a circular polygon on the Earth's surface formed by a latitude/longitude coordinate and radius [m].

    Example usage:

    .. code-block:: python

        circle = MapCircle(
            center=MapPoint(52.373922404495474, 5.2459716796875),
            radius=500
        )
    """
    center: Incomplete
    radius: Incomplete
    def __init__(self, center: MapPoint, radius: float, *, num_edges: int = 64, **kwargs: Any) -> None:
        """
        :param center: Center point of the circle.
        :param radius: Radius in [m].
        :param num_edges: Number of polygon edges.
        :param kwargs: See :class:`MapFeature` for possible kwargs.
        """

class MapLegend:
    '''
    A legend which is placed as an overlay on a map view.

    Example usage:

    .. code-block:: python

        legend = MapLegend([
            (Color.from_hex(\'#0016FF\'), "I\'m blue"),
            (Color.from_hex(\'#FF0000\'), "I\'m red"),
            ...
        ])
    '''
    def __init__(self, entries: list[tuple[Color, str]]) -> None:
        """
        :param entries: Items in the legend, defined by color and label.
        """

class MapLabel:
    """
    Text which is placed as an overlay on the map.

    Scale 0-5 is approximately the scale for countries:

    .. figure:: ../_static/map_label_scale_0_5.png
        :width: 800px
        :align: center

    Scale 6-10 is approximately the scale for cities:

    .. figure:: ../_static/map_label_scale_6_11.png
        :width: 800px
        :align: center

    Scale 11-15 is approximately the scale for neighborhoods and streets

    .. figure:: ../_static/map_label_scale_11_15.png
        :width: 800px
        :align: center

    Scale 16-18 is approximately for individual houses.

    .. figure:: ../_static/map_label_scale_14_19.png
        :width: 800px
        :align: center

    """
    def __init__(self, lat: float, lon: float, text: str, scale: float, *, fixed_size: bool = False) -> None:
        """
        :param lat: Latitude of text in degrees.
        :param lon: Longitude of text in degrees.
        :param text: Text with is displayed on the map.
        :param scale: Size of the text on an exponential scale. See example in class docstring for estimate.
        :param fixed_size: When True, the size of the text is fixed regardless of zoom level (default: False).
        """

class Label:
    size_factor: Incomplete
    color: Incomplete
    def __init__(self, point: Point, *text: str, size_factor: float = 1, color: Color = ...) -> None:
        """ Text label

        :param point: Position of the label.
        :param text: Text to show; multiple text arguments will each be shown on a new line.
        :param size_factor: Factor to be applied to the font size (0 < size_factor <= 10).
        :param color: Color of the text.
        """
    @property
    def point(self) -> Point: ...
    @property
    def text(self) -> str | tuple[str, ...]: ...
    def serialize(self) -> dict: ...
TableCellValue = str | float | int | bool | datetime.datetime | datetime.date | None

class TableCell:
    value: Incomplete
    text_color: Incomplete
    background_color: Incomplete
    def __init__(self, value: TableCellValue, *, text_color: Color | None = None, background_color: Color | None = None, text_style: Literal['bold', 'italic'] | None = None) -> None: ...

class TableHeader:
    class _TYPE(Enum):
        STRING = 'string'
        NUMBER = 'number'
        BOOLEAN = 'boolean'
        DATE = 'date'
        MIXED = 'mixed'
    class _ALIGN(Enum):
        CENTER = 'center'
        LEFT = 'left'
        RIGHT = 'right'
    title: Incomplete
    def __init__(self, title: str, *, align: Literal['center', 'left', 'right'] | None = None, num_decimals: int | None = None) -> None:
        """ Header object that can be used in :class:`TableResult` to set styling.

        :param title: Title that will be shown in the header.
        :param align: Visual alignment of the corresponding row/column values within the table
        :param num_decimals: Number of decimals that is shown for the row/column values (requires corresponding
          row/column to contain only numbers).
        """

class _SubResult(_Result, ABC, metaclass=abc.ABCMeta):
    """
    Each _ViewResult consists of a combination of sub results, which allows for easy plug-and-play of different type of
    views.
    """

class _ViewResult(ABC, metaclass=abc.ABCMeta):
    """
    Base-class of a view result.
    A subclass consists of the visualization data results.
    """
    def __init__(self, version: int) -> None: ...

class _DataSubResult(_SubResult):
    data: Incomplete
    def __init__(self, data: DataGroup) -> None: ...

class _GeometrySubResult(_SubResult):
    geometry: Incomplete
    geometry_type: Incomplete
    labels: Incomplete
    def __init__(self, geometry: TransformableObject | Sequence[TransformableObject] | File | FileResource, labels: list[Label] = None, *, geometry_type: str = 'gltf') -> None: ...

class _ImageSubResult(_SubResult):
    image: File
    def __init__(self, image: File | FileResource | StringIO | BytesIO, image_type: str | None) -> None: ...

class _GeoJSONSubResult(_SubResult):
    geojson: Incomplete
    labels: Incomplete
    legend: Incomplete
    interaction_groups: Incomplete
    def __init__(self, geojson: dict, labels: list[MapLabel] = None, legend: MapLegend = None, interaction_groups: dict[str, Sequence[int | str | MapFeature]] = None) -> None: ...

class _WebSubResult(_SubResult):
    html: Incomplete
    url: Incomplete
    def __init__(self, *, html: File = None, url: str = None) -> None: ...

class _PlotlySubResult(_SubResult):
    figure: Incomplete
    def __init__(self, figure: str | dict | go.Figure) -> None: ...

class _PDFSubResult(_SubResult):
    url: Incomplete
    file: Incomplete
    def __init__(self, *, file: File | FileResource = None, url: str = None) -> None: ...

class _IFCSubResult(_SubResult):
    ifc: Incomplete
    def __init__(self, ifc: File | FileResource) -> None: ...

class _TableSubResult(_SubResult):
    data: Incomplete
    column_headers: Incomplete
    row_headers: Incomplete
    enable_sorting_and_filtering: Incomplete
    def __init__(self, data: Sequence[Sequence[TableCellValue | TableCell]], column_headers: Sequence[str | TableHeader] | None, row_headers: Sequence[str | TableHeader] | None, enable_sorting_and_filtering: bool | None) -> None: ...

class GeometryResult(_ViewResult):
    '''
    Container with the results that should be visualized in a GeometryView. This consists of three-dimensional geometry
    object(s) and optional text labels.

    To enable a geometric object for interaction, the object must be named using the \'identifier\' argument. In case of
    a glTF/GLB-file, the objects name can be provided on the "name" key within a node. If none of the objects in the
    GeometryResult have a name assigned, default names are assigned to all of them (enabling them for interaction).
    Note: if there are multiple objects with the same name, a number will automatically be appended to enforce
    uniqueness.

    Example viktor.geometry TransformableObject(s):

    .. code-block:: python

        geometry = vkt.Sphere(Point(0, 0), 10, identifier="MySphere")
        vkt.GeometryResult(geometry)  # or [obj1, obj2, ...] in case of multiple objects

    By specifying the `geometry_type` you can render 3D geometry files either by providing a path, URL, or dynamically
    created (e.g. using `trimesh`). Currently supported geometry types are: "gltf", "3dm".

    Example static geometry file from path:

    .. code-block:: python

        geometry = vkt.File.from_path(Path(__file__).parent / "my_model.gltf")
        vkt.GeometryResult(geometry, geometry_type="gltf")

    Example static geometry file from a URL:

    .. code-block:: python

        geometry = vkt.File.from_url("https://github.com/KhronosGroup/glTF-Sample-Models/tree/main/2.0/CesiumMilkTruck/glTF-Binary/CesiumMilkTruck.glb")
        vkt.GeometryResult(geometry, geometry_type="gltf")

    Example from FileField:

    .. code-block:: python

        vkt.GeometryResult(params.my_geometry_file, geometry_type="gltf")

    Example dynamic geometry file (e.g. using trimesh):

    .. code-block:: python

        sphere = trimesh.creation.uv_sphere(10)
        scene = trimesh.Scene(geometry={\'sphere\': sphere})
        geometry = vkt.File()
        with geometry.open_binary() as w:
            w.write(trimesh.exchange.gltf.export_glb(scene))
        vkt.GeometryResult(geometry, geometry_type="gltf")

    '''
    geometry: Incomplete
    geometry_type: Incomplete
    labels: Incomplete
    def __init__(self, geometry: TransformableObject | Sequence[TransformableObject] | File | FileResource, labels: list[Label] = None, *, geometry_type: str = 'gltf') -> None:
        '''
        :param geometry: TransformableObject(s) that contain the geometric objects, or a geometry file such as
            glTF/GLB (v2.0) (https://en.wikipedia.org/wiki/GlTF).
        :param geometry_type: Type of loader that should be used to render the geometry
            ("gltf", "3dm") ::version(v14.4.0).
        :param labels: Text labels that can be used to provide additional information.
        '''

class GeometryAndDataResult(_ViewResult):
    """
    Container with the results that should be visualized in a GeometryAndDataView. This consists of three-dimensional
    geometry object(s) with optional text labels and data.

    Please have a look at GeometryResult for examples.
    """
    geometry: Incomplete
    geometry_type: Incomplete
    labels: Incomplete
    data: Incomplete
    def __init__(self, geometry: TransformableObject | Sequence[TransformableObject] | File | FileResource, data: DataGroup, labels: list[Label] = None, *, geometry_type: str = 'gltf') -> None:
        '''
        :param geometry: TransformableObject(s) that contain the geometric objects, or a geometry file such as
            glTF/GLB (v2.0) (https://en.wikipedia.org/wiki/GlTF).
        :param geometry_type: Type of loader that should be used to render the geometry
            ("gltf", "3dm") ::version(v14.4.0).
        :param data: Result data.
        :param labels: Text labels that can be used to provide additional information.
        '''

class DataResult(_ViewResult):
    """ Container with the data that should be shown in a DataView. This data can be nested up to three levels deep. """
    data: Incomplete
    def __init__(self, data: DataGroup) -> None:
        """
        :param data: Result data.
        """

class ImageResult(_ViewResult):
    image: Incomplete
    def __init__(self, image: StringIO | BytesIO | File | FileResource) -> None:
        """ ::version(v13.7.0)

        Image to be visualized in an ImageView.

        Supported image types are 'svg', 'jpeg', 'png', 'gif'.

        Example from FileField:

        .. code-block:: python

            vkt.ImageResult(params.my_image_file)

        :param image: image file.
        """
    @classmethod
    def from_path(cls, file_path: str | bytes | os.PathLike) -> ImageResult:
        """ Use file path to construct the image result.

        :param file_path: Path to the image.
        """

class ImageAndDataResult(_ViewResult):
    image: Incomplete
    data: Incomplete
    def __init__(self, image: StringIO | BytesIO | File, data: DataGroup) -> None:
        """ ::version(v13.7.0)

        Container with the image and result data that should be visualized in a ImageAndDataView.

        Supported image types are 'svg', 'jpeg', 'png', 'gif'.

        :param image: image file.
        :param data: Result data.
        """

class GeoJSONResult(_ViewResult):
    '''
    Container with the GeoJSON data that should be visualized in a GeoJSONView. Optionally a legend and map labels can
    be included.

    The following geojson properties are supported that can be used for styling of the map elements:

        - icon (geometry type \'Point\' only): icon to be shown (default: "pin"). For a complete list of all available markers, see :class:`MapPoint`
        - marker-color: the color of a marker [*]_
        - description: text to show when this item is clicked
        - stroke: the color of a line as part of a polygon, polyline, or multigeometry *
        - fill: the color of the interior of a polygon *

    .. [*] color rules: Colors can be in short form "#ace" or long form "#aaccee", and should contain the # prefix.
                        Colors are interpreted the same as in CSS, in #RRGGBB and #RGB order.

    To enable interaction, the map feature identifiers can be defined within the geojson dict by adding an "id"
    attribute to a feature as follows:

    .. code-block::

        {
          "type": "FeatureCollection",
          "features": [
            {
              "type": "Feature",
              "properties": ...,
              "geometry": ...
              "id": "my identifier",
              ...

    '''
    labels: Incomplete
    legend: Incomplete
    interaction_groups: Incomplete
    def __init__(self, geojson: dict, labels: list[MapLabel] = None, legend: MapLegend = None, *, interaction_groups: dict[str, Sequence[int | str | MapFeature]] = None) -> None:
        """
        :param geojson: GeoJSON dictionary.
        :param labels: Labels that should be placed on the map.
        :param legend: Map legend.
        :param interaction_groups: create named groups that can be referred to in a map interaction ::version(v13.2.0)
        """
    @property
    def geojson(self) -> dict: ...
    @geojson.setter
    def geojson(self, value: dict) -> None: ...

class GeoJSONAndDataResult(_ViewResult):
    """
    Container with the GeoJSON data and result data that should be visualized in a GeoJSONAndDataView. Optionally a
    legend and map labels can be included.
    """
    data: Incomplete
    labels: Incomplete
    legend: Incomplete
    interaction_groups: Incomplete
    def __init__(self, geojson: dict, data: DataGroup, labels: list[MapLabel] = None, legend: MapLegend = None, *, interaction_groups: dict[str, Sequence[int | str | MapFeature]] = None) -> None:
        """
        :param geojson: GeoJSON dictionary.
        :param data: Result data.
        :param labels: Labels that should be placed on the map.
        :param legend: Map legend.
        :param interaction_groups: create named groups that can be referred to in a map interaction ::version(v13.2.0)
        """
    @property
    def geojson(self) -> dict: ...
    @geojson.setter
    def geojson(self, value: dict) -> None: ...

class MapResult(GeoJSONResult):
    """
    Container with the Map data that should be visualized in a MapView. Optionally a legend and map labels can
    be included.
    """
    def __init__(self, features: list[MapFeature], labels: list[MapLabel] = None, legend: MapLegend = None, *, interaction_groups: dict[str, Sequence[int | str | MapFeature]] = None) -> None:
        """
        :param features: List that contains the map objects.
        :param labels: Labels that should be placed on the map.
        :param legend: Map legend.
        :param interaction_groups: create named groups that can be referred to in a map interaction ::version(v13.2.0)
        """
    @property
    def features(self) -> list[MapFeature]: ...
    @features.setter
    def features(self, value: list[MapFeature]) -> None: ...
    @property
    def geojson(self) -> dict: ...
    @geojson.setter
    def geojson(self, value: dict) -> None: ...

class MapAndDataResult(GeoJSONAndDataResult):
    """
    Container with the Map data and result data that should be visualized in a MapAndDataView. Optionally a
    legend and map labels can be included.
    """
    def __init__(self, features: list[MapFeature], data: DataGroup, labels: list[MapLabel] = None, legend: MapLegend = None, *, interaction_groups: dict[str, Sequence[int | str | MapFeature]] = None) -> None:
        """
        :param features: List that contains the map objects.
        :param data: Result data.
        :param labels: Labels that should be placed on the map.
        :param legend: Map legend.
        :param interaction_groups: create named groups that can be referred to in a map interaction ::version(v13.2.0)
        """
    @property
    def features(self) -> list[MapFeature]: ...
    @features.setter
    def features(self, value: list[MapFeature]) -> None: ...
    @property
    def geojson(self) -> dict: ...
    @geojson.setter
    def geojson(self, value: dict) -> None: ...

class WebResult(_ViewResult):
    '''
    Container with the data that should be visualized in a WebView.
    There are two options, which should not be used together:

    - url: to serve a URL (takes precedence if both are defined)
    - html: for serving a single html page

    Example usage:

    .. code-block:: python

        @vkt.WebView("Hello world")
        def get_web_view(self, params, **kwargs):
            html = textwrap.dedent("""
            <html>
            <head>
                <meta charset="UTF-8">
                <title>My View</title>
            </head>
            <body>
                <h1>Hello world 🌎</h1>
            </body>
            </html>
            """)
            return vkt.WebResult(html=html)

    .. code-block:: python

        @vkt.WebView(\'Python wiki\')
        def get_web_view(self, params, **kwargs):
            return vkt.WebResult(url=\'https://en.wikipedia.org/wiki/Python_(programming_language)\')
    '''
    html: Incomplete
    url: Incomplete
    def __init__(self, *, html: StringIO | File | str = None, url: str = None) -> None:
        """

        :param html: HTML formatted content.
        :param url: Direct URL.
        """
    @classmethod
    def from_path(cls, file_path: str | bytes | os.PathLike) -> WebResult: ...

class WebAndDataResult(_ViewResult):
    """
    Container with the web data and result data that should be visualized in a WebAndDataView.

    The Web part can be constructed in two ways, which should not be used together:

    - url: to serve a URL (takes precedence if both are defined)
    - html: for serving a single html page
    """
    html: Incomplete
    url: Incomplete
    data: Incomplete
    def __init__(self, *, html: StringIO | File | str = None, url: str = None, data: DataGroup = None) -> None:
        """
        :param html: HTML formatted content.
        :param url: Direct URL.
        :param data: Result data.
        """

class PlotlyResult(_ViewResult):
    ''' Plotly figure to be visualized in a PlotlyView. The figure can be provided in json-string or dict format.

    **(new in v14.22.0)** Support a plotly \'Figure\' object.

    Example usages:

    .. code-block:: python

        @PlotlyView("Plotly view")
        def get_plotly_view(self, params, **kwargs):
            fig = go.Figure(
                data=[go.Bar(x=[1, 2, 3], y=[1, 3, 2])],
                layout=go.Layout(title=go.layout.Title(text="A Figure Specified By A Graph Object"))
            )
            return PlotlyResult(fig)

    .. code-block:: python

        @PlotlyView("Plotly view")
        def get_plotly_view(self, params, **kwargs):
            fig = {
                "data": [{"type": "bar", "x": [1, 2, 3], "y": [1, 3, 2]}],
                "layout": {"title": {"text": "A Figure Specified By Python Dictionary"}}
            }
            return PlotlyResult(fig)
    '''
    figure: Incomplete
    def __init__(self, figure: str | dict | go.Figure) -> None:
        """
        :param figure: Plotly figure
        """

class PlotlyAndDataResult(_ViewResult):
    ''' Plotly figure to be visualized in a PlotlyAndDataView. The figure can be provided in json-string or dict format.

    **(new in v14.22.0)** Support a plotly \'Figure\' object.

    Example usage:

    .. code-block:: python

        @PlotlyAndDataView("Plotly and data view")
        def get_plotly_and_data_view(self, params, **kwargs):
            data_group = ...

            fig = go.Figure(
                data=[go.Bar(x=[1, 2, 3], y=[1, 3, 2])],
                layout=go.Layout(title=go.layout.Title(text="A Figure Specified By A Graph Object"))
            )
            return PlotlyAndDataResult(fig, data_group)

    '''
    figure: Incomplete
    data: Incomplete
    def __init__(self, figure: str | dict | go.Figure, data: DataGroup) -> None:
        """
        :param figure: Plotly figure
        :param data: result data
        """

class PDFResult(_ViewResult):
    file: Incomplete
    url: Incomplete
    def __init__(self, *, file: File | FileResource = None, url: str = None) -> None:
        ''' PDF document to be visualized in a PDFView. Can be defined from a File object or from a URL
        (direct-sharing). If both file and url are defined, url takes precedence.

        In case of URL: the hosting website must allow for direct accessing for the document to be shown. If this is
        forbidden (undefined CORS-headers), the document can alternatively be shown via the file argument with a
        File.from_url(...), in which it is downloaded first and viewed subsequently (indirect-sharing).

        Example usages:

        From URL (direct-sharing):

        .. code-block:: python

            PDFResult(url="https://www...")

        From URL (indirect-sharing):

        .. code-block:: python

            f = File.from_url("https://www...")
            PDFResult(file=f)

        From path:

        .. code-block:: python

            file_path = Path(__file__).parent / \'sample.pdf\'
            PDFResult.from_path(file_path)  # or ...
            PDFResult(File.from_path(file_path))

        From FileField:

        .. code-block:: python

            PDFResult(file=params.my_pdf_file)

        :param file: PDF document to view
        :param url: URL of PDF document to view. If accessing the PDF directly from the URL is not allowed by the host
         website (undefined CORS-headers), this will result in the document not showing up in the view (as an
         alternative one can use File.from_url).
        '''
    @classmethod
    def from_path(cls, file_path: str | bytes | os.PathLike) -> PDFResult:
        """ Create the PDFResult from a path to the PDF file.

        :param file_path: file path to a PDF file
        """

class IFCResult(_ViewResult):
    ''' ::version(v14.6.0)

    IFC to be visualized in an IFCView.

    Example static geometry file from path:

    .. code-block:: python

        ifc = File.from_path(Path(__file__).parent / \'sample.ifc\')
        IFCResult(ifc)

    Example static geometry file from a URL:

    .. code-block:: python

        ifc = File.from_url("https://github.com/IFCjs/test-ifc-files/raw/main/Others/haus.ifc")
        IFCResult(ifc)

    **(new in v14.6.1)** In order to improve performance it is possible to use the value of a FileField
    (i.e. FileResource) directly:

    .. code-block:: python

        IFCResult(params.file_field)

    '''
    ifc: Incomplete
    def __init__(self, ifc: File | FileResource) -> None:
        """
        :param ifc: IFC geometry file.
        """

class IFCAndDataResult(_ViewResult):
    """ ::version(v14.6.0)

    Container with the results that should be visualized in an IFCAndDataView.

    Please have a look at IFCResult for examples.
    """
    ifc: Incomplete
    data: Incomplete
    def __init__(self, ifc: File | FileResource, data: DataGroup) -> None:
        """
        :param ifc: IFC geometry file.
        :param data: Result data.
        """

class TableResult(_ViewResult):
    ''' ::version(v14.13.0)

    Data to be visualized in an TableView.

    Example of a simple TableResult:

    .. code-block:: python

        data = [
            [1.5, "Square"],
            [3.1, "Circle"],
        ]
        TableResult(data)

    Example of a simple TableResult with column header titles:

    .. code-block:: python

        data = [
            [1.5, "Square"],
            [3.1, "Circle"],
        ]
        TableResult(data, column_headers=["Area [m²]", "Shape"])

    Example of a more complex TableResult with column and cell styling:

    .. code-block:: python

        data = [
            [1.5, "Square"],
            [
                TableCell(3.1, text_color=Color.green()),
                TableCell("Circle", background_color=Color(211, 211, 211), text_style=\'italic\')
            ],
        ]
        TableResult(data, column_headers=[
            TableHeader("Area [m²]", num_decimals=2),
            TableHeader("Shape", align=\'center\')
        ]))

    Example of a transposed table:

    .. code-block:: python

        data = [
            [1.5, "Square"],
            [3.1, "Circle"],
        ]
        transposed_data = [list(i) for i in zip(*data)]
        TableResult(
            transposed_data,
            row_headers=[
                TableHeader("Area [m²]", num_decimals=2),
                TableHeader("Shape", align=\'center\')
            ],
            column_headers=["Object 1", "Object 2"]
        ))

    Example of a pandas Dataframe object:

    .. code-block:: python

        df = pd.DataFrame([[1, 4], [2, 3]])
        TableResult(df)

    Example of a pandas Styler object:

    .. code-block:: python

        df = pd.DataFrame([[1, 4], [2, 3]])
        styler = df.style.highlight_min(color="red")
        TableResult(styler)
    '''
    data: Incomplete
    column_headers: Incomplete
    row_headers: Incomplete
    enable_sorting_and_filtering: Incomplete
    def __init__(self, data: Sequence[Sequence[TableCellValue | TableCell]] | pd.DataFrame | Styler, *, column_headers: Sequence[str | TableHeader] | None = None, row_headers: Sequence[str | TableHeader] | None = None, enable_sorting_and_filtering: bool | None = None) -> None:
        """ Result to be shown in a TableView.

        In case the data is a pandas Styler object, the following properties will be inherited:

        -  background_color (per cell)
        -  text_color (per cell)
        -  text_style (per cell, bold or italic)
        -  align (per column/row, only if all cells in a row/column have the same alignment)

        :param data: Table content. Can also be a pandas DataFrame or Styler object.
        :param column_headers: Headers shown above the columns. Can be used for custom titles and styling. In case the
          data is a pandas Styler object, this can be set explicitly to overwrite the generated titles and styling.
        :param row_headers: Headers shown next to the rows. Can be used for custom titles and styling. In case the
          data is a pandas Styler object, this can be set explicitly to overwrite the generated titles and styling.
        :param enable_sorting_and_filtering: Enable sorting and filtering on columns. If set to None (default),
          sorting and filtering will be enabled if each of the columns in data is of homogeneous type, and disabled
          otherwise. If sorting and filtering is enabled explicitly, each column must be of homogeneous type.
        """

class AutodeskResult(_ViewResult):
    """ ::version(v14.25.0)

    Container with the Autodesk cloud storage file that should be visualized in a AutodeskView.
    """
    def __init__(self, autodesk_file: AutodeskFile | str, *, access_token: str) -> None:
        '''

        :param autodesk_file: Autodesk file to show. Can also pass the URN (unique resource name) of the versioned file
         on Autodesk cloud storage (of the form "urn:adsk.wipprod:fs.file:vf.XXX?version=Y") directly.
        :param access_token: Autodesk cloud storage token to access the file.
        '''

class SummaryItem:
    """
    A summary consists of SummaryItem objects, that define which input / result values should be displayed.

    Suppose we have a data view with a controller method 'data_view', which returns a DataItem with key 'output_item_1'.
    The following summary item can be constructed to refer to this result:

    .. code-block:: python

        item_1 = SummaryItem('Label', float, 'data_view', 'output_item_1', suffix='N')

    Suppose we have a parametrization with a certain parameter defined as `geometry.input.length`, this can be converted
    to a summary item by doing:

    .. code-block:: python

        item_2 = SummaryItem('Length', float, 'parametrization', 'geometry.input.length', suffix='m')
    """
    def __init__(self, label: str, item_type: type[str | float], source: str, value_path: str, *, suffix: str = '', prefix: str = '') -> None:
        """
        :param label: Text label of the item.
        :param item_type: Type of value, options are 'str' | 'float'.
        :param source: Source from which the input / output should be extracted.
        :param value_path: Dotted path of value in parametrization / data structure of view. e.g: level1.level2.value
        :param suffix: A suffix will be put behind the value to provide additional information such as units.
        :param prefix: A prefix will be put in front of the value to provide info such as a dollar sign.
        """

class Summary(OrderedDict):
    """
    Summary of resulting data items, which can be used in the summary view of an entity.

    Example usage:

    .. code-block:: python

        class Controller:
            ...
            summary = Summary(
                item_1=SummaryItem(...),
                item_2=SummaryItem(...),
                item_3=SummaryItem(...)
            )
    """
    def __init__(self, **items: SummaryItem) -> None:
        """
        :param items: Items that are shown in the summary, with a maximum of 6 items per summary.
        """

class View(ABC, metaclass=abc.ABCMeta):
    """
    .. warning:: Do not use this class directly in an application.

    Base-class of a function decorator that can be used to specify the desired view to be returned.
    See the subclasses for specific examples of each type of view.

    **(new in v14.15.0)** The 'duration_guess' argument is now optional.
    """
    def __init__(self, label: str, duration_guess: int = None, *, description: str = None, update_label: str = None, visible: bool | Callable = True, **kwargs: Any) -> None:
        """
        :param label: Name which is shown on tab in interface. e.g: '3D Representation'
        :param duration_guess: Estimation of view calculation in seconds. This will be used to add a
                               manual refresh button for long-running tasks (larger than 3s). This estimation does not
                               need to be very precise, but the performance will be better if this is close to the real
                               maximum computation time (defaults to 1).
        :param description: Show more information to the user through a tooltip on hover (max. 200 characters).
        :param update_label: Name which is shown on the update button in case of a slow view (max. 30 characters).
        :param visible: Visibility of the view. Can depend on params by using a callback function ::version(v14.22.0)
        """
    def __call__(self, view_function: Callable) -> Callable: ...

class GeometryView(View):
    '''
    Function decorator to instruct the controller method to return a geometry view (2D / 3D).

    Example usage:

    .. code-block:: python

        @GeometryView("3D model")
        def get_geometry_view(self, params, **kwargs):
            ...
            return GeometryResult(...)

        @GeometryView("2D model", view_mode=\'2D\')
        def get_geometry_view_2d(self, params, **kwargs):
            ...
            return GeometryResult(...)


    **(new in v14.15.0)** The \'duration_guess\' argument is now optional.

    See :class:`GeometryResult` for example implementations.
    '''
    def __init__(self, label: str, duration_guess: int = None, *, description: str = None, update_label: str = None, view_mode: Literal['2D', '3D'] = '3D', default_shadow: bool = False, up_axis: Literal['Y', 'Z'] = 'Z', x_axis_to_right: bool = None, visible: bool | Callable = True) -> None:
        """
        :param label: See :class:`View`.
        :param duration_guess: See :class:`View`.
        :param description: See :class:`View`.
        :param update_label: See :class:`View`.
        :param view_mode: Sets the view mode:

            - '3D': Camera is free to move and user can choose between orthographic and perspective view.
            - '2D': Camera is fixed on the xy-plane and view is orthographic.

        :param default_shadow: Show shadow when editor is opened. User can still switch it off.
        :param up_axis: (view_mode='3D' only) Upwards pointing axis. Possible options: 'Y', 'Z' (default: 'Z')
        :param x_axis_to_right: (view_mode='3D' and up_axis='Y' only) X-axis pointing to the right in the initial view
         ::version(v14.8.0)
        :param visible: Visibility of the view. Can depend on params by using a callback function ::version(v14.22.0)
        """

class DataView(View):
    '''
    Function decorator to instruct the controller method to return a data view that contains calculation result.

    Example usage:

    .. code-block:: python

        @DataView("Cost breakdown")
        def get_data_view(self, params, **kwargs):
            # calculate data
            ...
            return DataResult(data_group)

    **(new in v14.15.0)** The \'duration_guess\' argument is now optional.
    '''

class GeometryAndDataView(View):
    '''
    Function decorator to instruct the controller method to return a combined view consisting of geometries and data.

    Example usage:

    .. code-block:: python

        @GeometryAndDataView("Model / Cost")
        def get_geometry_data_view(self, params, **kwargs):
            ...
            return GeometryAndDataResult(...)

    **(new in v14.15.0)** The \'duration_guess\' argument is now optional.
    '''
    def __init__(self, label: str, duration_guess: int = None, *, description: str = None, update_label: str = None, view_mode: Literal['2D', '3D'] = '3D', default_shadow: bool = False, up_axis: Literal['Y', 'Z'] = 'Z', x_axis_to_right: bool = None, visible: bool | Callable = True) -> None: ...

class GeoJSONView(View):
    '''
    Function decorator to instruct the controller method to return a GeoJSON (geographic data) view.

    Example usage:

    .. code-block:: python

        @GeoJSONView("Map")
        def get_geojson_view(self, params, **kwargs):
            ...
            return GeoJSONResult(...)

    **(new in v14.15.0)** The \'duration_guess\' argument is now optional.
    '''
class GeoJSONAndDataView(View):
    '''
    Function decorator to instruct the controller method to return a combined view consisting of a GeoJSON and data.

    Example usage:

    .. code-block:: python

        @vkt.GeoJSONAndDataView("Map / Data")
        def get_geojson_data_view(self, params, **kwargs):
            ...
            return vkt.GeoJSONAndDataResult(...)

    **(new in v14.15.0)** The \'duration_guess\' argument is now optional.
    '''
class MapView(View):
    '''
    Function decorator to instruct the controller method to return a Map (geographic data) view.

    Example usage:

    .. code-block:: python

        @vkt.MapView("Map")
        def get_map_view(self, params, **kwargs):
            ...
            return vkt.MapResult(...)

    **(new in v14.15.0)** The \'duration_guess\' argument is now optional.
    '''
class MapAndDataView(View):
    '''
    Function decorator to instruct the controller method to return a combined view consisting of a Map and data.

    Example usage:

    .. code-block:: python

        @vkt.MapAndDataView("Map / Data")
        def get_map_data_view(self, params, **kwargs):
            ...
            return vkt.MapAndDataResult(...)

    **(new in v14.15.0)** The \'duration_guess\' argument is now optional.
    '''
class ImageView(View):
    ''' ::version(v13.7.0)

    Function decorator to instruct the controller method to return an ImageView.

    Supported image types are \'svg\', \'jpeg\', \'png\', \'gif\'.

    Example usage:

    .. code-block:: python

        @vkt.ImageView("Image View")
        def get_image_view(self, params, **kwargs):
            file_path = Path(__file__).parent / \'sample.png\'
            return vkt.ImageResult(File.from_path(file_path))  # or `vkt.ImageResult.from_path(file_path)`

    **(new in v14.15.0)** The \'duration_guess\' argument is now optional.
    '''
class ImageAndDataView(View):
    ''' ::version(v13.7.0)

    Function decorator to instruct the controller method to return a combined view consisting of an image and data.

    Supported image types are \'svg\', \'jpeg\', \'png\', \'gif\'.

    Example usage:

    .. code-block:: python

        @vkt.ImageAndDataView("Image View")
        def get_image_data_view(self, params, **kwargs):
            ...
            return vkt.ImageAndDataResult(image, data_group)

    **(new in v14.15.0)** The \'duration_guess\' argument is now optional.
    '''
class WebView(View):
    '''
    Function decorator to instruct the controller method to return a web-content view.

    Example usage:

    .. code-block:: python

        @vkt.WebView("Hello world")
        def get_web_view(self, params, **kwargs):
            return vkt.WebResult(html="<html>Hello world</html>")

    **(new in v14.15.0)** The \'duration_guess\' argument is now optional.
    '''
class WebAndDataView(View):
    '''
    Function decorator to instruct the controller method to return a combined view consisting of web-content and data.

    Example usage:

    .. code-block:: python

        @WebAndDataView("Web / Data")
        def get_web_data_view(self, params, **kwargs):
            # calculate data
            ...
            return WebAndDataResult(html="<html>Hello world</html>", data=data_group)

    **(new in v14.15.0)** The \'duration_guess\' argument is now optional.
    '''
class PlotlyView(View):
    '''
    Function decorator to instruct the controller method to return a PlotlyView.

    Example usage:

    .. code-block:: python

        @PlotlyView("Plotly view")
        def get_plotly_view(self, params, **kwargs):
            ...
            return PlotlyResult(figure)

    **(new in v14.15.0)** The \'duration_guess\' argument is now optional.
    '''
class PlotlyAndDataView(View):
    '''
    Function decorator to instruct the controller method to return a combined view consisting of a PlotlyView and a
    DataView.

    Example usage:

    .. code-block:: python

        @PlotlyAndDataView("Plotly and data view")
        def get_plotly_and_data_view(self, params, **kwargs):
            ...
            return PlotlyAndDataResult(figure, data_group)

    **(new in v14.15.0)** The \'duration_guess\' argument is now optional.
    '''
class PDFView(View):
    '''
    Function decorator to instruct the controller method to return a PDFView.

    Example usage:

    .. code-block:: python

        @PDFView("PDF View")
        def get_pdf_view(self, params, **kwargs):
            file_path = Path(__file__).parent / \'sample.pdf\'
            return PDFResult(File.from_path(file_path))  # or `PDFResult.from_path(file_path)`

    **(new in v14.15.0)** The \'duration_guess\' argument is now optional.
    '''
class IFCView(View):
    ''' ::version(v14.6.0)

    Function decorator to instruct the controller method to return an IFCView.

    Example usage:

    .. code-block:: python

        @IFCView("IFC view")
        def get_ifc_view(self, params, **kwargs):
            ifc = File.from_path(Path(__file__).parent / \'sample.ifc\')
            return IFCResult(ifc)

    **(new in v14.15.0)** The \'duration_guess\' argument is now optional.
    '''
class IFCAndDataView(View):
    ''' ::version(v14.6.0)

    Function decorator to instruct the controller method to return a combined view consisting of an IFCView and a
    DataView.

    Example usage:

    .. code-block:: python

        @IFCAndDataView("IFC and data view")
        def get_ifc_and_data_view(self, params, **kwargs):
            ifc = File.from_path(Path(__file__).parent / \'sample.ifc\')
            data = ...
            return IFCAndDataResult(ifc, data)

    **(new in v14.15.0)** The \'duration_guess\' argument is now optional.
    '''
class TableView(View):
    ''' ::version(v14.13.0)

    Function decorator to instruct the controller method to return an TableView.

    Example usage:

    .. code-block:: python

        @TableView("Table view")
        def get_table_view(self, params, **kwargs):
            data = [
                [2.5, 7, "Square"],
                [1.5, 8, "Circle"],
            ]
            return TableResult(data, column_headers=["Width", "Height", "Shape"])

    **(new in v14.15.0)** The \'duration_guess\' argument is now optional.
    '''

class InteractionEvent:
    """ Event triggered by the user as a consequence of an :class:`viktor.parametrization.Interaction`.

    .. warning:: Do not instantiate this class directly, it is returned as 'event' in the method of the button with the
        corresponding interaction.
    """
    type: Incomplete
    value: Incomplete
    def __init__(self, event_type: str, value: Any) -> None:
        """
        :param event_type: type of the event ('map_select')
        :param value: value of the user performed interaction. Type depends on event_type:

            - map_select: List[Union[str, int]] = identifier of selected features
        """

class AutodeskView(View):
    ''' ::version(v14.25.0)

    A decorator class that configures a controller method to return an Autodesk-specific view, utilizing the Autodesk
    API for content display.

    Example usage:

    .. code-block:: python

        @vkt.AutodeskView("Autodesk View")
        def get_autodesk_view(self, params, **kwargs):
            integration = vkt.external.OAuth2Integration("autodesk-integration")
            token = integration.get_access_token()
            autodesk_file = params.autodesk_file  # value of AutodeskFileField

            if autodesk_file is None:
                raise vkt.UserError("Please select an Autodesk file")

            return vkt.AutodeskResult(autodesk_file, access_token=token)

    '''
