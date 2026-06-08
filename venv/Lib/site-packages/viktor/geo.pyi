import abc
import matplotlib.pyplot as plt
import os
import pandas as pd
from .core import Color as Color, File as File, ISCLOSE_ATOL as ISCLOSE_ATOL, ISCLOSE_RTOL as ISCLOSE_RTOL
from .errors import GEFClassificationError as GEFClassificationError, GEFParsingError as GEFParsingError
from .geometry import CircularExtrusion as CircularExtrusion, Group as Group, Line as Line, Material as Material, Point as Point, Polygon as Polygon, Polyline as Polyline, TransformableObject as TransformableObject
from .views import Label as Label
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from io import BytesIO, StringIO
from munch import Munch as Munch

GEFParsingException = GEFParsingError

class _ClassificationMethod(ABC, metaclass=abc.ABCMeta):
    """
    Abstract class to allow new classification methods to be added
    """
    @abstractmethod
    def get_method_params(self) -> dict: ...

class RobertsonMethod(_ClassificationMethod):
    """
    Class to pass Robertson specific properties such as soil_properties. Every list element at least requires a
    'name' key that specifies the RobertsonZone. It is important that 'name' key matches with hardcoded
    RobertsonZone.name property. There are 9 Robertson zones and 1 Robertson zone unknown that can be specified

    By default, the colors as defined in (red, green, blue) for each zone are as shown in this figure:

    .. figure:: ../_static/robertson_colors.png
        :width: 300px
        :align: center

    Example:

    .. code-block:: python

        soil_properties = [
           {'name': 'Robertson zone unknown', 'extra_property1': 1, 'extra_property2': 2},
           {'name': 'Robertson zone 1', 'extra_property1': 3, 'extra_property2': 4},
        ]
        method = RobertsonMethod(soil_properties)
    """
    soil_properties: Incomplete
    def __init__(self, soil_properties: list[dict]) -> None:
        """
        :param soil_properties: dictionary with soil properties
        """
    def get_method_params(self) -> dict: ...

class TableMethod(_ClassificationMethod):
    """
    Class to pass TableMethod specific properties, such as a qualification_table and ground_water_level. The
    qualification_table is a list of dictionaries, containing for each user-specified soil type the accompanying
    qualification parameters (and possibly additional material properties). The required fields for each row are:

        - name
        - color in r, g, b

    Also required fields, but can also be (partly) empty:

        - qc_min
        - qc_max
        - qc_norm_min
        - qc_norm_max
        - rf_min
        - rf_max
        - gamma_dry_min
        - gamma_dry_max
        - gamma_wet_min
        - gamma_wet_max

    For more information about qc_norm (qc_normalized), see table 2.b in in NEN 9997-1+C1:2012, point g specifically.
    Besides the qualification table, a ground_water_level has to be provided as well, which is used to determine if
    gamma_dry or gamma_wet should be used to calculate qc_norm for each entry in the GEF file.

    Example:

    .. code-block:: python

        qualification_table = [
            {'name': 'Peat', 'color': '166,42,42', 'qc_min': 0, 'qc_max': '', 'qc_norm_min': '',
                'qc_norm_max': '', 'rf_min': 8, 'rf_max': '', 'gamma_dry_min': 10, 'gamma_wet_min': 10, <OTHER>},
            {'name': 'Clay', 'color': '125,180,116', 'qc_min': '', 'qc_max': 2, 'qc_norm_min': '',
                'qc_norm_max': '', 'rf_min': 1, 'rf_max': 8, 'gamma_dry_min': 20, 'gamma_wet_min': 22, <OTHER>},
            {'name': 'Loam', 'color': '125,150,116', 'qc_min': 2, 'qc_max': '', 'qc_norm_min': '',
                'qc_norm_max': '', 'rf_min': 1, 'rf_max': 8, 'gamma_dry_min': 20, 'gamma_wet_min': 22, <OTHER>},
            {'name': 'Sand', 'color': '239,255,12', 'qc_min': '', 'qc_max': '', 'qc_norm_min': 22,
                'qc_norm_max': '', 'rf_min': 0, 'rf_max': 1, 'gamma_dry_min': 24, 'gamma_wet_min': 26, <OTHER>},
            {'name': 'Gravel', 'color': '255,255,128', 'qc_min': '', 'qc_max': '', 'qc_norm_min': '',
                'qc_norm_max': 22, 'rf_min': 0, 'rf_max': 1, 'gamma_dry_min': 24, 'gamma_wet_min': 26, <OTHER>}
        ]
        ground_water_level = -4.63
        method = TableMethod(qualification_table, ground_water_level)
    """
    qualification_table: Incomplete
    ground_water_level: Incomplete
    def __init__(self, qualification_table: list[dict], ground_water_level: float) -> None:
        """
        :param ground_water_level: Ground water level is used to compute qc_norm using either gamma_dry or gamma_wet
        :param qualification_table: List containing rows defining a soil
        """
    def get_qualification_table_plot(self, fileformat: str) -> BytesIO | StringIO:
        """
        Use this method to obtain a plot of the qualification table. On the x axis the Rf values are plotted, on the
        y axis Qc values are shown. Each line, representing a soil, is shown as an area in this plot. This allows for
        easy inspection of the qualification rules, showing areas of the plot that might still be empty, or soil areas
        that overlap (in which case the area on top will be chosen). Use the fileformat argument  to specify if
        the result should be a BytesIO containing pdf or png bytes or a StringIO containing svg data

        :param fileformat: specify if required fileformat is pdf, png or svg

        :return: qualification table plot as either BytesIO ('pdf' or 'png') or StringIO ('svg') object
        """
    def get_method_params(self) -> dict: ...

class NormalizedSoilBehaviourTypeIndexMethod(_ClassificationMethod):
    """
    Class to classify soil based on the normalized soil behaviour type index

    Example:

    .. code-block:: python

        ic_table = [
           {'name': 'Zand', 'color': '0, 50, 255', 'ic_min': 0, 'ic_max': 3.5},
           {'name': 'Klei', 'color': '80, 70, 25', 'ic_min': 3.5, 'cone_factor': 20},
        ]
        
        ground_water_level = 0
        specific_weight_soil = 17
        method = NormalizedSoilBehaviourTypeIndexMethod(ic_table, ground_water_level, specific_weight_soil)

    This method uses the assumption that the specific weight of all the soil layers is the same, this is a
    simplification. It is possible to calculate the specific weight from qc values.
    """
    ic_table: Incomplete
    ground_water_level: Incomplete
    specific_weight_soil: Incomplete
    resolution: Incomplete
    def __init__(self, ic_table: list[dict], ground_water_level: float, specific_weight_soil: float, resolution: float = None) -> None:
        """
        :param ic_table: Table with soil types that correspond to Ic values. Keys: name, ic_min, ic_max, color,
            cone_factor
        :param ground_water_level: Ground water level used to compute qc_norm
        :param specific_weight_soil: Specific weight of soil in kN/m^3 used to calculate sigma'
        :param resolution: Resolution of the classification in m; if None classify each line of data
        """
    def get_method_params(self) -> dict: ...

class _QualificationTablePlot:
    """
    Class to generate a plot of a qualification table used in the TableMethod. Each row in the qualification table
    specifies a soil by it's lower- and upper-bounds in terms of Rf (friction number) and Qc (Cone pressure). These
    rows can be plotted as a rectangle, giving insight into which soil area overlap or where in the spectrum of Rf
    vs Qc there are still gaps.
    """
    filename: Incomplete
    qualification_table: Incomplete
    def __init__(self, filename: str, qualification_table: list) -> None:
        """
        :param filename: name of the plot
        :param qualification_table: rows defining a soil
        """
    @property
    def body(self) -> bytes: ...

class GEFData:
    '''
    Initialize GEFData object to simplify working with GEF data. Every GEF has different header fields, and
    therefore only a limited amount of fields is compulsory. All other header fields are also added as attribute.
    Compulsory header fields are:

        - name
        - ground_level_wrt_reference

    Other header fields might be compulsory for methods on the object (e.g. `get_cone_visualization`).
    See docstring of the specific method for needed headers.

    The following measurement_data fields are also compulsory and are implicitly parsed from the file (do NOT need
    to be specified explicitly):

        - elevation
        - qc
        - Rf

    Examples of optional attributes from header are:

        - height_system
        - project_name
        - project_id
        - gef_file_date
        - gef_version_number
        - x_y_coordinates
        - coordinate_system
        - excavation_depth
        - measurement_standard
        - surface_area_quotient_tip
        - water_level
        - cone_tip_area
        - cone_type

    Measurement_data fields that are optional are:

        - u2
        - fs
        - penetration_length
        - corrected_depth
        - inclination
        - inclination_n_s
        - inclination_e_w

    Example implementation to create GEFData object:

    .. code-block:: python

        import viktor as vkt


        class GEFFileController(vkt.Controller):
            ...

            @vkt.ParamsFromFile(file_types=[\'.gef\'])
            def process_file(self, file, **kwargs) -> dict:
                file_content = file.getvalue(encoding="ISO-8859-1")
                gef_file = vkt.geo.GEFFile(file_content)
                gef_data_object = gef_file.parse(additional_columns=[\'elevation\', \'qc\', \'Rf\', \'fs\', \'u2\'],
                                                 return_gef_data_obj=True)
                gef_dict = gef_data_object.serialize()
                return {\'gef_dict\': gef_dict}

            def get_gef_content_from_database(self) -> vkt.geo.GEFData:
                # API call to right entity
                return vkt.geo.GEFData(gef_file_entity.last_saved_params[\'gef_dict\'])
    '''
    classification_data: Incomplete
    name: Incomplete
    Rf: Incomplete
    qc: Incomplete
    elevation: Incomplete
    num_of_measurements: Incomplete
    max_measurement_depth_wrt_reference: Incomplete
    ground_level_wrt_reference: Incomplete
    height_system: Incomplete
    def __init__(self, gef_dict: dict | Munch) -> None:
        """
        :param gef_dict: dictionary with ['headers'] and ['measurement_data'] keys
        """
    def classify(self, method: _ClassificationMethod, return_soil_layout_obj: bool = True) -> dict | SoilLayout:
        """
        Create SoilLayout object or dictionary by classifying the GEF measurement data, using either the Robertson
        method or a qualification table method.

        **RobertsonMethod**

        This method requires the GEFData object to at least contain the measurement data 'corrected_depth'. See
        :class:`GEFData` for all possible measurement data columns.

        .. code-block:: python

            from viktor.geo import RobertsonMethod


            soil_properties = [
                {'name': 'Robertson zone unknown', 'extra_property1': 1, 'extra_property2': 2},
                {'name': 'Robertson zone 1', 'extra_property1': 3, 'extra_property2': 4},
            ]
            classification_method = RobertsonMethod(soil_properties)
            soil_layout_dict = gef_data.classify(method=classification_method, return_soil_layout_obj=False)

        **TableMethod**

        For this method a qualification table has to be provided by the user, for example through a VIKTOR editor.
        Please refer to the docstring of :class:`TableMethod` for the structure of this table.

        This table is usually controlled on a project-wide level, so in a parent entity. On the controller of the GEF
        file, you can use the API to retrieve the table content and pass it to the TableMethod:

        .. code-block:: python

            import viktor as vkt

            api = vkt.api_v1.API()
            parent_entity = api.get_entity(entity_id).parent()
            parent_params = parent.last_saved_params
            qualification_table = parent_params['material_properties']
            ground_water_level = parent_params['ground_water_level']

            classification_method = vkt.geo.TableMethod(qualification_table, ground_water_level)
            soil_layout_obj = gef_data.classify(method=classification_method, return_soil_layout_obj=False)

        .. note:: This method needs to be mocked in (automated) unit and integration tests.

        :param method: Specifies which method should be used for qualification:
                       TableMethod | RobertsonMethod | NormalizedSoilBehaviourTypeIndexMethod.
        :param return_soil_layout_obj: Flag to return SoilLayout object or dictionary
        :return: SoilLayout object or dictionary (=SoilLayout.serialize())
        """
    def serialize(self) -> dict | Munch: ...
    def get_cone_visualization(self, axes: plt.Axes) -> None:
        """
        Modify (clean/empty) 'axes' input argument to plot cone resistance (with pore pressure if present in GEF data).

        :param axes: Axes object that will be modified.

        The following header fields are compulsory and need to be specified when the GEFData object is created:

            - max_measurement_depth_wrt_reference
            - ground_level_wrt_reference
            - height_system

        Example usage:

        .. code-block:: python

            import matplotlib.pyplot as plt

            # Create main figure
            fig = plt.figure(figsize=(8.27, 11.69))

            # Define contour (rectangle) for cone visualization, and create Axes object that can be modified by
            # functions
            rect_cone = [0.1, 0.1, 0.4, 0.9]  # [left, bottom, width, height]
            cone_axes = plt.axes(rect_cone)
            # Modify created Axes objects
            self.gef_data.get_cone_visualization(cone_axes)

            # Convert to SVG for visualization
            svg_data = StringIO()
            fig.savefig(svg_data, format='svg', bbox_inches='tight', pad_inches=0.8)
            plt.close()
            gef_visualisation_data = svg_data.getvalue()
        """
    def get_resistance_visualization(self, axes: plt.Axes) -> None:
        """
        Modify (clean/empty) 'axes' input argument to plot resistance number.

        :param axes: Axes object that will be modified.

        The following header fields are compulsory and need to be specified when the GEFData object is created:

            - max_measurement_depth_wrt_reference
            - ground_level_wrt_reference

        Example usage:

        .. code-block:: python

            import matplotlib.pyplot as plt

            # Create main figure
            fig = plt.figure(figsize=(8.27, 11.69))

            # Define contour (rectangle) for resistance number visualization, and create Axes object that can be
            # modified by functions
            rect_resistance = [0.1, 0.1, 0.4, 0.9]  # [left, bottom, width, height]
            resistance_axes = plt.axes(rect_resistance)
            # Modify created Axes objects
            self.gef_data.get_resistance_visualization(resistance_axes)

            # Convert to SVG for visualization
            svg_data = StringIO()
            fig.savefig(svg_data, format='svg', bbox_inches='tight', pad_inches=0.8)
            plt.close()
            gef_visualisation_data = svg_data.getvalue()
        """
    def get_plotted_denotation_large_qc_values(self, axes: plt.Axes, x_loc_text: float) -> None:
        """
        Can be used to add text labels with the maximum qc value of a layer that exceeds the maximum value of the
        x-axis.

        :param axes: Axes object that will be modified.
        :param x_loc_text: Maximum qc value.

        The following header fields are compulsory and need to be specified when the GEFData object is created:

            - max_measurement_depth_wrt_reference

        An example is shown below where the figure is capped at a maximum qc of 30 MPa (hence x_loc_text=30).

        .. figure:: ../_static/gefdata_plot_large_qc.svg
            :width: 600px
            :align: center

        """

class GEFFile:
    file_content: Incomplete
    def __init__(self, file_content: str) -> None: ...
    @classmethod
    def from_file(cls, file_path: str | bytes | os.PathLike, encoding: str = 'ISO-8859-1') -> GEFFile: ...
    def parse(self, additional_columns: list[str] = None, verbose: bool = True, return_gef_data_obj: bool = True) -> dict | GEFData:
        '''
        Parse GEFFile, and return information from GEF in dict with [\'headers\'] and [\'measurement data\'] sub-dicts or
        a GEFData object.

        Example implementation:

        .. code-block:: python

            import viktor as vkt


            class GEFFileController(vkt.Controller):
                ...

                @vkt.ParamsFromFile(file_types=[\'.gef\'])
                def process_file(self, file, **kwargs) -> dict:
                    file_content = file.getvalue(encoding="ISO-8859-1")
                    gef_file = vkt.geo.GEFFile(file_content)
                    gef_data_obj = gef_file.parse(additional_columns=[\'fs\', \'u2\'], return_gef_data_obj=True)

                    soil_properties = [
                        {\'name\': Robertson zone unknown, \'extra_property1\': 1, \'extra_property2\': 2},
                        {\'name\': Robertson zone 1, \'extra_property1\': 3, \'extra_property2\': 4},
                    ]

                    soil_layout_dict = gef_data_obj.classify(method=vkt.geo.RobertsonMethod(soil_properties), return_soil_layout_obj=False)
                    parsed_dict = gef_data_obj.serialize()
                    parsed_dict[\'soils\'] = soil_layout_dict
                    return parsed_dict

        .. note:: This method needs to be mocked in (automated) unit and integration tests.

        :param additional_columns: In order for a GEF file to be of use in VIKTOR, three columns are required:

            - elevation (corrected depth with respect to a specified datum)
            - qc (tip pressure as measured)
            - Rf (friction number, either measured or computed using qc and fs)

            These three columns will always be parsed and returned, additional columns can be parsed as well. Possible
            columns to request are:

            - "penetration_length"
            - "corrected_depth"
            - "fs"
            - "u2" (for more accuracy when qualifying layers using Robertson method)
            - "inclination"
            - "inclination_n_s"
            - "inclination_e_w"

        :param verbose: Boolean specifying if parsing should output warnings or work in silence
        :param return_gef_data_obj: Boolean to return GEFData or dictionary
        :return: dictionary with GEF parameters or GEFData object with GEF parameters as attributes
        '''

def gef_visualization(gef_data: GEFData, soil_layout_original: SoilLayout, soil_layout_user: SoilLayout, *, as_file: bool = False) -> str | File:
    ''' Standard visualization for GEF File.

    Example usage:

    .. code-block:: python

        class Controller(vkt.Controller):
           ...

            @vkt.ImageView("GEF plot", duration_guess=2)
            def visualize(self, params, **kwargs):
                gef_data = ...
                soil_layout_original = ...
                soil_layout_user = ...
                svg_image = vkt.geo.gef_visualization(gef_data, soil_layout_original, soil_layout_user)
                return vkt.ImageResult(svg_image)

    :param gef_data: GEFData object to be visualized
    :param soil_layout_original: SoilLayout from GEFData. Layers must be sorted from top to bottom.
    :param soil_layout_user: SoilLayout that is filtered/modified by user. Layers must be sorted from top to bottom.
    :param as_file: return as str (default) or File ::version(v13.5.0)

    :return: SVG image file
    '''

class Soil:
    name: Incomplete
    properties: Incomplete
    def __init__(self, name: str, color: Color, properties: dict | Munch = None) -> None:
        """
        Set name and color of Soil material. Extra properties can be added with dictionary, and keys are added as
        attribute via 'munchify'. They are accessible as self.properties.{extra_property_name}

        :param name:
        :param color: color of soil used in plots
        :param properties: dict with optional extra parameters to be added to Soil
        """
    @classmethod
    def from_dict(cls, d: dict | Munch) -> Soil: ...
    def __eq__(self, other) -> bool:
        """See if two soil types are the same with soil_type_1 == soil_type_2"""
    @property
    def color(self) -> Color: ...
    def update_properties(self, properties: dict | Munch) -> None:
        """
        Replace the current properties dict with the provided new one.

        For backwards compatibility, this function is kept with this functionality.
        In order to be able to update the existing properties dict, the properties property is public and mutable.

        :param properties: dictionary with all SoilLayer properties
        """
    def serialize(self) -> dict:
        """
        Serialize Soil in following dictionary structure:

        .. code-block::

            {
                'name',
                'color',
                'properties': {
                    (..extra_properties..)
                },
            }

        :return: dictionary with all properties of Soil
        """

class UndefinedSoil(Soil):
    def __init__(self) -> None: ...

class PiezoLine(Polyline):
    """
    Class to represent a Piezo line.

    Essentially, this is a polyline with a flag added to mark the phreatic polyline.

    """
    phreatic: Incomplete
    def __init__(self, points: list[Point], phreatic: bool = False) -> None:
        """

        :param points: points of the polyline
        :param phreatic: mark the phreatic waterline
        """
    def serialize(self) -> dict: ...
    @classmethod
    def from_dict(cls, piezo_line_dict: dict | Munch) -> PiezoLine: ...
    @classmethod
    def from_lines(cls, lines: list[Line | Polyline], phreatic: bool = False) -> PiezoLine:
        """
        create a polyline object from a list of lines
        the end of one line must always coincide with the start of the next

        :param lines:
        :param phreatic:
        """

class SoilLayer:
    soil: Incomplete
    top_of_layer: Incomplete
    bottom_of_layer: Incomplete
    properties: Incomplete
    def __init__(self, soil: Soil, top_of_layer: float, bottom_of_layer: float, properties: dict | Munch = None) -> None:
        """
        Create a SoilLayer to be used in SoilLayout

        :param soil: Type of soil
        :param top_of_layer: Top of layer
        :param bottom_of_layer: Bottom of layer
        :param properties: dict with optional extra parameters to be added to SoilLayer
        """
    @classmethod
    def from_dict(cls, soil_layer_dict: dict | Munch) -> SoilLayer: ...
    @property
    def thickness(self) -> float: ...
    def serialize(self) -> dict:
        """
        Serialize SoilLayer in following dictionary structure:

        .. code-block:: python

            {
                'soil',
                'top_of_layer',
                'bottom_of_layer',
            }

        :return: dictionary with properties of SoilLayer
        """
    def update_soil_properties(self, properties: dict | Munch) -> None: ...
    def update_properties(self, properties: dict | Munch) -> None:
        """
        Replace the current properties dict with the provided new one.

        For backwards compatibility, this function is kept with this functionality.
        In order to be able to update the existing properties dict, the properties property is public and mutable.

        :param properties: dictionary with all SoilLayer properties
        """

class SoilLayer2D:
    soil: Incomplete
    top_profile: Incomplete
    bottom_profile: Incomplete
    piezo_line_top: Incomplete
    piezo_line_bottom: Incomplete
    properties: Incomplete
    def __init__(self, soil: Soil, top_profile: Polyline, bottom_profile: Polyline, properties: dict | Munch = None, piezo_line_top: PiezoLine = None, piezo_line_bottom: PiezoLine = None) -> None:
        """
        A 2D representation of a soil layer

        A Soil layer 2d always consists of a soil and a top and bottom profile
        Optionally, properties and top and bottom pl lines can be added

        Top and bottom profiles need to be monotonic ascending in x-direction
        Top and bottom profiles need to have identical start x and end x coordinates. These will become the left and right boundaries

        Top and bottom profiles can overlap, but not intersect. The layer can have one or multiple ranges with zero thickness,
        but the top profile may never lie below the bottom profile

        :param soil:
        :param top_profile:
        :param bottom_profile:
        :param properties:
        :param piezo_line_top:
        :param piezo_line_bottom:
        """
    def serialize(self) -> dict:
        """
        Serialize SoilLayer in following dictionary structure:

        .. code-block::

            {
                'soil': Soil
                'top_profile': Polyline
                'bottom_profile': Polyline
                'piezo_line_top': serialized PiezoLine
                'piezo_line_bottom': serialized PiezoLine
                'properties': Dict
            }

        :return: dictionary with properties of SoilLayer
        """
    @classmethod
    def from_dict(cls, soil_layer_dict: dict | Munch) -> SoilLayer2D:
        """ Instantiates a SoilLayer2D from the provided soil layer data.

        dict structure:

        .. code-block::

            {
                'soil': serialized Soil
                'top_profile': serialized Polyline
                'bottom_profile': serialized Polyline
                'piezo_line_top': serialized PiezoLine
                'piezo_line_bottom': serialized PiezoLine
                'properties': Dict
            }

        :param soil_layer_dict: Soil layer data.
        """
    @property
    def left_boundary(self) -> float: ...
    @property
    def right_boundary(self) -> float: ...
    def update_soil_properties(self, properties: dict | Munch) -> None:
        """
        Replace the current soil properties dict with a new one

        :param properties:
        :return:
        """
    def update_properties(self, properties: dict | Munch) -> None:
        """
        Replace the current properties dict with the provided new one.

        For backwards compatibility, this function is kept with this functionality.
        In order to be able to update the existing properties dict, the properties property is public and mutable.

        :param properties: dictionary with all SoilLayer properties
        :return:
        """
    def polygons(self) -> list[Polygon]:
        """ Generate a list of polygons representing this soil layer.

        For every region of this soil layout that has a non-zero thickness, a polygon is generated.
        """
    def visualize_geometry(self, visualize_border: bool = False, opacity: float = 1, material: Material = None) -> tuple[Group, list[Label]]:
        """ Returns the visualization elements (group, labels) of the SoilLayer2D which can be used in a GeometryView.

        :param visualize_border: visualize the border surrounding this soil layout with an extra line.
        :param opacity: float between 0 (transparent) - 1 (opaque)
        :param material: optional material to be applied on the geometry.
        """
    def height_at_x(self, x: float) -> float:
        """
        Returns the height at a specific x location.

        If a profile has a vertical section on the given x-location,
        this method will return the first touching point of the polyline with the vertical line

        :param x: The x-coordinate where the height is requested.
        :return: The height at the x-coordinate location.
        """
    def top_y_coordinate(self, x: float) -> float:
        """
        Determine the y-coordinate along the top boundary, belonging to the x value used as input

        If a profile has a vertical section on the given x-location,
        this method will return the first touching point of the polyline with the vertical line

        :param x: The x-coordinate where the height is requested.
        :return: The y-coordinate of the top at the x-coordinate location.
        """
    def bottom_y_coordinate(self, x: float) -> float:
        """
        Determine the y-coordinate along the bottom boundary, belonging to the x value used as input

        If a profile has a vertical section on the given x-location,
        this method will return the first touching point of the polyline with the vertical line

        :param x: The x-coordinate where the height is requested.
        :return: The y-coordinate of the top at the x-coordinate location.
        """

class SoilLayout:
    layers: Incomplete
    def __init__(self, soil_layers: list[SoilLayer]) -> None:
        """
        Aggregation object of SoilLayer

        :param soil_layers: list of SoilLayer objects
        """
    @classmethod
    def from_dict(cls, soil_layout_dict: dict[str, list] | Munch) -> SoilLayout:
        """
        Create SoilLayout with dictionary from SoilLayout.serialize(). Useful when SoilLayout needs to be created from
        dictionary from the database.

        Example usage:

        .. code-block:: python

            class Controller(vkt.Controller):
                ...

                def get_soil_layout_from_database(self) -> vkt.geo.SoilLayout:
                    # API call to entity that stores complete SoilLayout
                    layout_dict = entity.last_saved_params['layout_dict']
                    soil_layout = vkt.geo.SoilLayout.from_dict(layout_dict)
                    return soil_layout

        :param soil_layout_dict: dictionary with same structure as SoilLayout.serialize()
        """
    def update_soil_properties(self, df: pd.DataFrame) -> None:
        """
        Update SoilLayout with Soil properties

        :param df: dataframe with soil properties by name (must at least have column 'name').
        :return:
        """
    def serialize(self) -> dict:
        """
        Serialize SoilLayout to dict (e.g. to store in database). The structure of dict is:

        .. code-block::

            {
               'layers': [...]
            }

        """
    def get_visualization(self, axes: plt.Axes) -> None:
        """
        Modify (clean/empty) 'axes' input argument to plot SoilLayout structure. Layers must be sorted from top to
        bottom.

        :param axes: Axes object that will be modified
        """
    @property
    def top(self) -> float:
        """ Height level of the top of the layout. """
    @property
    def bottom(self) -> float:
        """ Height level of the bottom of the layout. """
    @property
    def number_of_layers(self) -> int:
        """Number of layers"""
    def update_layers(self) -> None:
        """
        Merges adjacent layers that have the same soil type. The merged layer is assigned the average value
        of each SoilLayer's individual properties. This average is calculated in ratio to the thickness of the layers.
        After merging layer depths are corrected by going from top to bottom and setting each bottom_of_layer equal to
        top_of_layer of next SoilLayer

        Example:
            layer 1 has thickness 10 and for property A a value of 5
            layer 2 has thickness 40 and for property A a value of 2
            Resulting layer will have thickness 50, and property A = (10 * 5 + 40 * 2) / (10 + 40) = 2.6
        """
    def append(self, layer: SoilLayer) -> None:
        """ Add a layer to the bottom of the classification

        :param layer: SoilLayer instance
        """
    def filter_layers_on_thickness(self, min_layer_thickness: float, merge_adjacent_same_soil_layers: bool = False) -> SoilLayout:
        """
        Collects layers that are thinner than min_layer_thickness in groups, and replaces them by one of two things:

          - If the group is thinner than `min_layer_thickness`, it is removed from the soil layout and the layer
            above it is elongated to fill the gap. See explanation figure, situation A.
          - If the group is equal to or thicker than `min_layer_thickness`, a new layer with `Soil` and properties of the
            most dominant (based cumulative thickness) soiltype occurring within this block of layers that was replaced
            by the new layer. See explanation figure, situation B.

        After all replacements have been made, if `merge_adjacent_same_soil_layers` is specified as `True`
        (default is `False`), :meth:`~.geo.SoilLayout._merge_adjacent_same_soil_layers` is called,
        which merges adjacent soil layers that have the same soiltype and have the same set of parameters. Note that this
        merging results in a new layer that has the average value for all soil layer properties present in the layers that
        were merged. See the docstring of :meth:`~.geo.SoilLayout._merge_adjacent_same_soil_layers` for more detailed
        information about how this is done.

        :param min_layer_thickness: Minimum thickness
        :param merge_adjacent_same_soil_layers: Try to merge adjacent layers that have the same soil type

        Note: this method alters the instance!

        .. figure:: ../_static/soil_layout_filtering_explanation.svg
            :width: 800px
            :align: center
        """
    def filter_unique_soils(self) -> list[Soil]: ...

class PositionalSoilLayout(SoilLayout):
    """
    A subclass of SoilLayout that adds an x location.
    This can be useful to generate a Soil Layout 2D
    """
    x: Incomplete
    def __init__(self, x: float, soil_layers: list[SoilLayer]) -> None:
        """
        Generate a positional soil layout from an x location and a list of soil layers

        :param x:
        :param soil_layers:
        """
    @classmethod
    def from_dict(cls, positional_soil_layout_dict: dict | Munch) -> PositionalSoilLayout:
        """ Instantiates a PositionalSoilLayout from the provided soil layout data.

        :param positional_soil_layout_dict: Soil layout data.
        """
    def serialize(self) -> dict:
        """ Generate a JSON serializable dict from this positional soil layout. """

class SoilLayout2D:
    left_boundary: Incomplete
    right_boundary: Incomplete
    piezo_lines: Incomplete
    layers: Incomplete
    def __init__(self, soil_layers: list[SoilLayer2D], piezo_lines: list[PiezoLine] = None) -> None:
        """
        A 2D representation of a soil body build up from layers.

        A Soil Layout 2D basically consists of the following elements:

        - A list of soil layers: objects of the class SoilLayer2D
        - A list of piezo lines
        - A left and right boundary
        - A top and bottom profile

        Left and right boundaries, as well as top and bottom profiles, are automatically taken from the given soil layers

        The following requirements are to be met:

        - Each soil layer has to stretch all the way from the left boundary to the right boundary
        - The layers have to be stacked starting from bottom to top
        - There can be no holes in the soil layout 2d, meaning that the top profile of a previous layer
          always has to be identical to the bottom profile of the next layer
        - A layer can have zero thickness over (part of) the width of the soil layout 2d
        - All soil layers and piezo lines have to exactly identical ranges in x direction, meaning that they all range
          exactly from left boundary to right boundary

        A SoilLayout2D will have roughly the following shape, with each layer containing it's own soil and soil
        properties:

        .. code-block::

             |                       xxxxxxxxxx                                |
             |xxxxxxxxxxxxxxxxxxxxxxx          xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|
             |                                                                 |
             |                                                                 |
             |                                         xxxxxxxx                |
             |xxxxxxxxxxxxxx              xxxxxxxxxxxxx        xxxxxxxxxxxxxxxx|
             |              xxx     xxxxxx                                     |
             |                  xxx                                            |
             |                                                                 |
             |                                                                 |
             |xxxxxxxxxxxxxxxxxxxxxxx                  xxxxxxxxxxxxxxxxxxxxxxxx|
             |                       xxxxxxxxxxxxxxxxxx                        |
             |                                                                 |
             |                  xxxxxxxxxxxxxxx                                |
             |xxxxxxxxxxxxxxxxxx               xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|


        The SoilLayout2D class is immutable. Any methods that alter or change properties of the class will return a
        new instance.

        :param soil_layers: an ordered dict of 2D soil layers. Starting from the bottom layer
        :param piezo_lines: list of piezo lines
        """
    @classmethod
    def from_positional_soil_layouts(cls, positional_soil_layouts: list[PositionalSoilLayout], top_profile: Polyline, piezo_lines: list[PiezoLine] = None) -> SoilLayout2D:
        """
        Instantiate a soil layout 2d from multiple 1d soil layouts combined with x locations and a ground profile

        all 1d soil layouts should have the same layers in the same order. Variation in height and thickness are possible

        the top profile has to be monotonic ascending in x direction

        :param positional_soil_layouts: 1d soil layouts with x locations
        :param top_profile: a polyline representing the ground level
        :param piezo_lines: list of piezo lines
        """
    @classmethod
    def from_single_soil_layout(cls, soil_layout: SoilLayout, left_boundary: float, right_boundary: float, top_profile: Polyline, piezo_lines: list[PiezoLine] = None) -> SoilLayout2D:
        """
        A special case when a 1D soil layout is stretched in the 2D plane.

        This class method will create a 2D layout with horizontal layers and a top_profile.

        :param soil_layout:
        :param top_profile:
        :param left_boundary:
        :param right_boundary:
        :param piezo_lines:
        """
    @classmethod
    def combine_soil_layouts_2d(cls, *soil_layouts_2d: SoilLayout2D) -> SoilLayout2D:
        """
        Combine multiple SoilLayout2D's in into one big SoilLayout2D

        All given soil layouts need to connect seemlessly, so that the resulting SoilLayout2D fullfills the requirement
        that it has got no holes and the top and bottom profile are monotonic ascending in x direction

        All layers will be continued (with zero thickness) to the new right and left boundaries

        :param soil_layouts_2d:
        :return:


        POSSIBLE COMBINATIONS:

        combining a left and a right soil layout 2d

        .. code-block::

            _____________________
            |                   |_______________________
            |                   |                      |
            |-------------------|----------------------|
            |                   |                      |
            |___________________|----------------------|
                                |                      |
                                |______________________|


        combining a top and bottom soil layout 2d

        .. code-block::

            _____________________
            |                   |
            |-------------------|
            |                   |
            |___________________|______________
                   |                          |
                   |--------------------------|
                   |__________________________|


        combining n soil layouts, as long as there are no holes in the resulting soil layout, and it is possible to keep all
        layer profiles monotonic ascending in x-directions

        .. code-block::

            _____________________
            |                   |_______________________
            |                   |                      |
            |-------------------|----------------------|
            |                   |                      |
            |___________________|______________________|
                        |                   |
                        |-------------------|
                        |___________________|




        IMPOSSIBLE COMBINATIONS:

        soillayouts without seem

        .. code-block::

            _____________________
            |                   |   ________________________
            |                   |   |                      |
            |-------------------|   |----------------------|
            |                   |   |                      |
            |___________________|   |----------------------|
                                    |                      |
                                    |______________________|


        overlapping soil layouts

        .. code-block::

            _____________________
            |           ________|_______________
            |           |       |              |
            |-----------|-------|              |
            |           |-------|--------------|
            |___________|_______|              |
                        |                      |
                        |______________________|


        the resulting soil layout does contain layers with profiles that are not monotonic ascending in x-direction

        .. code-block::

            _____________________
            |                   |_______________________
            |                   |                      |
            |-------------------|                      |
            |                   |----------------------|
            |___________________|                      |
                                |                      |
                        ________|______________________|
                        |                   |
                        |-------------------|
                        |___________________|

        """
    @classmethod
    def from_dict(cls, soil_layout_2d_dict: dict | Munch) -> SoilLayout2D:
        """
        Create SoilLayout2D with dictionary from SoilLayout2D.serialize(). Useful when SoilLayout2D needs to be
        created from dictionary from the database.

        Example usage:

        .. code-block:: python

            class Controller(vkt.Controller):
                ...

                def get_interpolated_soil_layout_from_database(self) -> vkt.geo.SoilLayout2D:
                    # API call to entity that stores complete SoilLayout2D
                    layout_dict = entity.last_saved_params['layout_dict']
                    interpolated_soil_layout = vkt.geo.SoilLayout2D.from_dict(layout_dict)
                    return interpolated_soil_layout

        :param soil_layout_2d_dict: dictionary with same structure as SoilLayout2D.serialize()
        """
    def serialize(self) -> dict:
        """
        Serialize to dict (e.g. to store in database). The structure of dict is:

        .. code-block::

           {'layers': [layer.serialize} for layer in self.layers,
            'piezo_lines': [line.serialize() for line in self.piezo_lines]}

        :return: dictionary with structure above
        """
    @property
    def top_profile(self) -> Polyline:
        """
        :return: top profile of the soil layout: Polyline
        """
    @property
    def bottom_profile(self) -> Polyline:
        """
        :return: bottom profile of the soil layout: Polyline
        """
    def visualize_geometry(self, visualize_border: bool = False, opacity: float = 1) -> tuple[Group, list[Label]]:
        """ Returns the visualization elements (group, labels) of the SoilLayout2D which can be used in a GeometryView.

        :param visualize_border: visualize the border surrounding this soil layout with an extra line.
        :param opacity: float between 0 (transparent) - 1 (opaque)
        """
    def split(self, *split_lines: Polyline) -> list['SoilLayout2D']:
        """
        Split the soil layout by given polylines.

        Each split line has to:

         - have a start and end point that lies outside of this soil layout
         - intersect the soil layout in at least one region
         - be monotonic ascending in x-direction

        Split lines are allowed to cross each other one or multiple times.

        Examples:

        Single split line

        .. code-block::

           ___________ ___________          ___________     ____________
           |         /           |          |         /    /           |
           |        /            |   ==>    |        /    /            |
           |-------/-------------|          |-------/    /-------------|
           |______/______________|          |______/    /______________|


        Single split line with multiple intersections

        .. code-block::

                        /\\\n            ___________/__\\________          _______________________
            |         /    \\      |          |         /    \\      |
            |        /      \\     |   ==>    |        /      \\     |
            |-------/--------\\----|          |-------/  ____  \\----|
            |______/__________\\___|          |______/  /    \\  \\___|
                  /            \\                      /      \\\n                                                     /--------\\\n                                                    /__________\\\n
        Two crossing split lines

        .. code-block::

                                                         ____
            ______ ____ ___________          _______     \\  /   ____________
            |      \\  /           |          |      \\     \\/   /           |
            |       \\/            |   ==>    |       \\        /            |
            |-------/\\------------|          |-------/        \\------------|
            |______/__\\___________|          |______/    /\\    \\___________|
                                                        /__\\\n

        :param split_lines: a list of polylines
        """
    def get_left_boundary_polyline(self) -> Polyline:
        """
        Get the polyline describing the left boundary
        This will always be a straight boundary
        This will contain a point on every boundary between layers

        :return: Polyline
        """
    def get_right_boundary_polyline(self) -> Polyline:
        """
        Get the polyline describing the right boundary
        This will always be a straight boundary
        This will contain a point on every boundary between layers

        :return: Polyline
        """
