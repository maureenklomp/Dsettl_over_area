from ...core import File
from ...geometry import Vector
from ..external_program import ExternalProgram
from .object import ArbitraryProfile, ArbitraryProfileSpan, AveragingStrip, Beam, CircularComposedCrossSection, CircularCrossSection, CircularHollowCrossSection, Concrete, CrossLink, CrossSection, FreeLineLoad, FreePointLoad, FreeSurfaceLoad, GeneralCrossSection, GeneralCrossSectionElement, HingeOnBeam, HingeOnPlane, IntegrationStrip, InternalEdge, Layer, LibraryCrossSection, LineForceSurface, LineLoad, LineMomentOnBeam, LineMomentOnPlane, LineSupportLine, LineSupportSurface, LoadCase, LoadCombination, LoadGroup, Material, MeshSetup, Node, NonLinearFunction, NonLinearLoadCombination, NumericalCrossSection, OpenSlab, Orthotropy, PermanentLoadCase, Plane, PointLoad, PointLoadNode, PointMomentNode, PointSupport, PointSupportLine, ProjectData, RectangularCrossSection, ResultClass, RigidArm, SciaObject, SectionOnBeam, SectionOnPlane, Selection, SolverSetup, Subsoil, SurfaceLoad, SurfaceSupportSurface, ThermalLoad, ThermalSurfaceLoad, VariableLoadCase
from _typeshed import Incomplete
from enum import Enum
from io import BytesIO
from typing import BinaryIO, Sequence

__all__ = ['CalcSetting', 'Model', 'OutputFileParser', 'ResultType', 'SciaAnalysis']

class CalcSetting(Enum):
    """Enumeration of calculation settings:"""
    NONE: CalcSetting
    NOC: CalcSetting
    LIN: CalcSetting
    NEL: CalcSetting
    EIG: CalcSetting
    STB: CalcSetting
    INF: CalcSetting
    MOB: CalcSetting
    TDA: CalcSetting
    SLN: CalcSetting
    PHA: CalcSetting
    NPH: CalcSetting
    CSS: CalcSetting
    NST: CalcSetting
    TID: CalcSetting

class ResultType(Enum):
    """Enumeration of result types:"""
    NONE: ResultType
    MODEL: ResultType
    ENGINEERING_REPORT: ResultType

class SciaAnalysis(ExternalProgram):
    '''
    SciaAnalysis can be used to perform an analysis using SCIA on a third-party worker. To start an analysis call
    the method :meth:`~.ExternalProgram.execute`, with an appropriate timeout (in seconds). To retrieve
    the output file call the method :meth:`get_xml_output_file` after :meth:`~.ExternalProgram.execute`.

    Usage:

    .. code-block:: python

        input_file = BytesIO("scia input file content".encode())
        xml_def_file = BytesIO("scia xml def file content".encode())
        scia_model = BytesIO("scia model content".encode())
        scia_analysis = SciaAnalysis(input_file=input_file, xml_def_file=xml_def_file, scia_model=scia_model)
        scia_analysis.execute(timeout=600)
        xml_output_file = scia_analysis.get_xml_output_file()

    Besides the output XML file, you can also retrieve the updated SCIA model. This is achieved using the `result_type`:

    .. code-block:: python

        scia_analysis = SciaAnalysis(input_file=input_file, xml_def_file=xml_def_file, scia_model=scia_model,
                                     result_type=ResultType.MODEL)
        scia_analysis.execute(timeout=600)
        updated_esa_file = scia_analysis.get_updated_esa_model()

    or the Engineering Report:

    .. code-block:: python

        scia_analysis = SciaAnalysis(input_file=input_file, xml_def_file=xml_def_file, scia_model=scia_model,
                                     result_type=ResultType.ENGINEERING_REPORT, output_document=\'report1\')
        scia_analysis.execute(timeout=600)
        engineering_report = scia_analysis.get_engineering_report()

    Exceptions which can be raised during calculation:

        - :class:`viktor.errors.LicenseError`: no license available
        - :class:`viktor.errors.ExecutionError`: generic error. Error message provides more information
    '''
    input_file: Incomplete
    xml_def_file: Incomplete
    scia_model: Incomplete
    calculation_setting: Incomplete
    xml_doc_name: Incomplete
    def __init__(self, input_file: BytesIO | File, xml_def_file: BytesIO | File, scia_model: BytesIO | File, calculation_setting: CalcSetting = ..., xml_doc_name: str = 'output', *, result_type: ResultType = ..., output_document: str = '') -> None:
        """
        :param input_file: SCIA input .xml file.
        :param xml_def_file: SCIA input .def file.
        :param scia_model: SCIA .esa model.
        :param calculation_setting: Available calculation settings according to the documentation of ESA_XML.exe:

            - NONE = without any recalculations
            - NOC = No calculation
            - LIN = Linear calculation (Delete all calculated results when exists)
            - NEL = Nonlinear calculation
            - CON = Nonlinear concrete calculation
            - EIG = Eigen frequencies calculation
            - STB = Stability calculation
            - INF = Influence lines calculation
            - MOB = Mobile loads calculation
            - TDA = TDA calculation
            - SLN = Soilin calculation
            - PHA = Phases calculation
            - NPH = Nonlinear phases
            - CSS = Recalculation of cross sections
            - NST = Nonlinear stability
            - TID = Test of input data - solver link only

        :param xml_doc_name: Name of XML IO document for export.
        :param result_type: Type of output which should be returned besides the output.xml:

            - ResultType.NONE returns nothing
            - ResultType.MODEL returns the updated SCIA model (.esa) after calculation
            - ResultType.ENGINEERING_REPORT returns the specified engineering report

        :param output_document: Document name of the report which should be returned. This name should match the exact
          name of the report as defined in the .esa model.

        :raises ValueError: if Engineering Report is selected as result_type, but no output_document is specified.
        """
    @staticmethod
    def get_xml_def_name(input_file: BinaryIO) -> str: ...
    def get_xml_output_file(self, as_file: bool = False) -> BytesIO | File | None:
        """
        Method can be used to retrieve the results generated by running an external analysis. This method returns the
        output XML file that is generated by SCIA. Make sure to call method :meth:`~.ExternalProgram.execute` first
        and :meth:`get_xml_output_file` afterwards.

        :returns:

            - File, if as_file = True
            - BytesIO, if as_file = False (default)

        """
    def get_updated_esa_model(self, as_file: bool = False) -> BytesIO | File | None:
        """
        Method can be used to retrieve the updated SCIA model file (.esa), which contains the data that is read into
        the model while calling ESA_XML.exe. Make sure to call method :meth:`~.ExternalProgram.execute`
        first and :meth:`get_updated_esa_model` afterwards.

        :returns:

            - File, if as_file = True
            - BytesIO, if as_file = False (default)

        """
    def get_engineering_report(self, as_file: bool = False) -> BytesIO | File | None:
        """
        Method can be used to retrieve the Engineering Report (.pdf). Make sure to call method
        :meth:`~.ExternalProgram.execute` first and :meth:`get_engineering_report` afterwards.

        :returns:

            - File, if as_file = True
            - BytesIO, if as_file = False (default)

        """

class Model:
    """
    This Model can be used to construct a SCIA model and generate its corresponding input XML file. This file can in
    turn be used as input of :class:`~.SciaAnalysis`. For a more detailed elaboration, please see the tutorial.

    Example usage:

    .. code-block:: python

        # Initialize the model
        model = Model()

        # Construct the geometry
        n1 = model.create_node('K:1', 0, 0, 0)
        n2 = model.create_node('K:2', 1, 0, 0)
        css = model.create_circular_cross_section('css', Material(123, 'some_material'), 100)
        beam = model.create_beam(n1, n2, css)

        #Construct the boundary conditions
        freedom = (PointSupport.Freedom.RIGID, PointSupport.Freedom.RIGID, PointSupport.Freedom.RIGID,
            PointSupport.Freedom.RIGID, PointSupport.Freedom.RIGID, PointSupport.Freedom.RIGID)
        model.create_point_support('Sn1', n1, PointSupport.Type.STANDARD, freedom, (0, 0, 0, 0, 0, 0),
            PointSupport.CSys.GLOBAL)

        # Construct a load combination
        load_group = model.create_load_group('LG1', LoadGroup.LoadOption.VARIABLE, LoadGroup.RelationOption.STANDARD,
            LoadGroup.LoadTypeOption.CAT_A)
        load_case = model.create_variable_load_case('LC1', 'My first load case', load_group,
            LoadCase.VariableLoadType.STATIC, LoadCase.Specification.STANDARD, LoadCase.Duration.SHORT)
        model.create_load_combination('C1', LoadCombination.Type.ENVELOPE_ULTIMATE, {load_case: 1})

        # Generate the input XML file
        input_xml = model.generate_xml_input()

    """
    def __init__(self, *, mesh_setup: MeshSetup = None, solver_setup: SolverSetup = None, project_data: ProjectData = None) -> None:
        """

        :param mesh_setup: Optional mesh settings.
        :param solver_setup: Optional solver settings ::version(v13.1.0).
        :param project_data: Optional project settings ::version(v13.1.0).
        """
    @property
    def layers(self) -> tuple[Layer, ...]: ...
    @property
    def concrete_materials(self) -> tuple[Concrete, ...]: ...
    @property
    def nonlinear_functions(self) -> tuple[NonLinearFunction, ...]: ...
    @property
    def subsoils(self) -> tuple[Subsoil, ...]: ...
    @property
    def orthotropy_objects(self) -> tuple[Orthotropy, ...]: ...
    @property
    def selections(self) -> tuple[Selection, ...]: ...
    @property
    def cross_sections(self) -> tuple[CrossSection, ...]: ...
    @property
    def nodes(self) -> tuple[Node, ...]: ...
    @property
    def beams(self) -> tuple[Beam, ...]: ...
    @property
    def cross_links(self) -> tuple[CrossLink, ...]:
        """ ::version(v13.1.0) """
    @property
    def arbitrary_profiles(self) -> tuple[ArbitraryProfile, ...]: ...
    @property
    def hinges_on_beam(self) -> tuple[HingeOnBeam, ...]: ...
    @property
    def hinges_on_plane(self) -> tuple[HingeOnPlane, ...]: ...
    @property
    def sections_on_beam(self) -> tuple[SectionOnBeam, ...]: ...
    @property
    def sections_on_plane(self) -> tuple[SectionOnPlane, ...]: ...
    @property
    def planes(self) -> tuple[Plane, ...]: ...
    @property
    def open_slabs(self) -> tuple[OpenSlab, ...]: ...
    @property
    def internal_edges(self) -> tuple[InternalEdge, ...]: ...
    @property
    def rigid_arms(self) -> tuple[RigidArm, ...]: ...
    @property
    def point_supports(self) -> tuple[PointSupport, ...]: ...
    @property
    def point_supports_line(self) -> tuple[PointSupportLine, ...]: ...
    @property
    def line_supports_line(self) -> tuple[LineSupportLine, ...]: ...
    @property
    def line_supports_surface(self) -> tuple[LineSupportSurface, ...]: ...
    @property
    def surface_supports(self) -> tuple[SurfaceSupportSurface, ...]: ...
    @property
    def load_cases(self) -> tuple[LoadCase, ...]: ...
    @property
    def load_groups(self) -> tuple[LoadGroup, ...]: ...
    @property
    def load_combinations(self) -> tuple[LoadCombination, ...]: ...
    @property
    def nonlinear_load_combinations(self) -> tuple[NonLinearLoadCombination, ...]: ...
    @property
    def result_classes(self) -> tuple[ResultClass, ...]: ...
    @property
    def point_loads_node(self) -> tuple[PointLoadNode, ...]: ...
    @property
    def point_loads(self) -> tuple[PointLoad, ...]: ...
    @property
    def point_moments_node(self) -> tuple[PointMomentNode, ...]: ...
    @property
    def line_loads(self) -> tuple[LineLoad, ...]: ...
    @property
    def line_moments_on_beam(self) -> tuple[LineMomentOnBeam, ...]: ...
    @property
    def line_moments_on_plane(self) -> tuple[LineMomentOnPlane, ...]: ...
    @property
    def line_force_surface_list(self) -> tuple[LineForceSurface, ...]: ...
    @property
    def surface_loads(self) -> tuple[SurfaceLoad, ...]: ...
    @property
    def thermal_loads(self) -> tuple[ThermalLoad, ...]: ...
    @property
    def thermal_surface_loads(self) -> tuple[ThermalSurfaceLoad, ...]: ...
    @property
    def free_surface_loads(self) -> tuple[FreeSurfaceLoad, ...]: ...
    @property
    def free_line_loads(self) -> tuple[FreeLineLoad, ...]: ...
    @property
    def free_point_loads(self) -> tuple[FreePointLoad, ...]: ...
    @property
    def integration_strips(self) -> tuple[IntegrationStrip, ...]: ...
    @property
    def averaging_strips(self) -> tuple[AveragingStrip, ...]: ...
    @property
    def mesh_setup(self) -> MeshSetup: ...
    @property
    def solver_setup(self) -> SolverSetup:
        """ ::version(v13.1.0) """
    @property
    def project_data(self) -> ProjectData:
        """ ::version(v13.1.0) """
    def create_layer(self, name: str = None, *, comment: str = None, structural_model_only: bool = None, current_used_activity: bool = None) -> Layer:
        """ Method to construct a layer.

        Duplicate layer names are not allowed.

        :param name: name of the layer (default: 'Layer{i}')
        :param comment: optional comment
        :param structural_model_only: when 'True', the layer is NOT taken into account for the calculation
         (default: False)
        :param current_used_activity: defines if the layer is visible or not on the screen (default: True)
        """
    def update_concrete_material(self, object_id: int, name: str, part: Concrete.ECPart, thermal_expansion: float = None, unit_mass: float = None, wet_density: float = None, e_modulus: float = None, poisson: float = None, g_modulus: float = None, log_decrement: float = None, specific_heat: float = None, thermal_conductivity: float = None, *, fck: float = None) -> Concrete:
        """
        This method can update specific properties of an already existing concrete material in the \\*.esa model.

        :param object_id: id of the material in SCIA
        :param name: name which will be shown in SCIA
        :param part: enumeration of concrete types
        :param thermal_expansion: thermal expansion in [m/mK]
        :param unit_mass: density in [kg/m\\ :sup:`3`]
        :param wet_density: wet density in [kg/m\\ :sup:`3`]
        :param e_modulus: Young's modulus in [Pa]
        :param poisson: Poisson ratio
        :param g_modulus: shear modulus in [Pa]
        :param log_decrement: log. decrement
        :param specific_heat: specific heat in [J/kgK]
        :param thermal_conductivity: thermal conductivity in [W/mK]
        :param fck: characteristic compressive cylinder strength [Pa]
        """
    def create_nonlinear_function(self, name: str, function_type: NonLinearFunction.Type, positive_end: NonLinearFunction.Support, negative_end: NonLinearFunction.Support, impulse: list[tuple[float, float]]) -> NonLinearFunction:
        """ Method to construct a non-linear function.

        :param name: name of the function
        :param function_type: type of function
        :param positive_end: type of support at positive end
        :param negative_end: type of support at negative end
        :param impulse: impulse function X-Y values in [m, N] (if function_type = TRANSLATION), [rad, Nm] (if
         function_type = ROTATION), or [m, Pa] (if function_type = NONLINEAR_SUBSOIL)
        """
    def create_subsoil(self, name: str, *, stiffness: float, c1x: float = None, c1y: float = None, c1z: Subsoil.C1z = None, nonlinear_function: NonLinearFunction = None, c2x: float = None, c2y: float = None, is_drained: bool = None, water_air_in_clay_subgrade: bool = None, specific_weight: float = None, fi: float = None, sigma_oc: float = None, c: float = None, cu: float = None) -> Subsoil:
        """ Method to construct a subsoil.

        :param name: name of the subsoil
        :param stiffness: stiffness c1z [N/m3]
        :param c1x: stiffness c1x [N/m3] (default: 50000000)
        :param c1y: stiffness c1y [N/m3] (default: 50000000)
        :param c1z: type for c1z (default: FLEXIBLE)
        :param nonlinear_function: nonlinear function (:meth:`~.create_nonlinear_function`)
         (c1z = NONLINEAR_FUNCTION only)
        :param c2x: [N/m]
        :param c2y: [N/m]
        :param is_drained: True for 'drained', False for 'undrained' (default: False)
        :param water_air_in_clay_subgrade: (default: False)
        :param specific_weight: specific weight [kg/m3] (default: 0.0)
        :param fi: fi' [deg] (default: 0.0)
        :param sigma_oc: sigma oc [Pa] (default: 0.0)
        :param c: c' [Pa] (default: 0.0)
        :param cu: [Pa] (default: 0.0)
        """
    def create_orthotropy(self, name: str, material: Material, thickness: float, D11: float = None, D22: float = None, D12: float = None, D33: float = None, D44: float = None, D55: float = None, d11: float = None, d22: float = None, d12: float = None, d33: float = None, kxy: float = None, kyx: float = None) -> Orthotropy:
        """ Method to construct a type of orthotropy.

        :param name: name of the orthotropy
        :param material: material
        :param thickness: thickness of the plate / wall [m]
        :param D11: (plate) stiffness matrix parameter [Nm]
        :param D22: (plate) stiffness matrix parameter [Nm]
        :param D12: (plate) stiffness matrix parameter [Nm]
        :param D33: (plate) stiffness matrix parameter [Nm]
        :param D44: (plate) stiffness matrix parameter [N/m]
        :param D55: (plate) stiffness matrix parameter [N/m]
        :param d11: (membrane) stiffness matrix parameter [N/m]
        :param d22: (membrane) stiffness matrix parameter [N/m]
        :param d12: (membrane) stiffness matrix parameter [N/m]
        :param d33: (membrane) stiffness matrix parameter [N/m]
        :param kxy: stiffness coefficient [N/m]
        :param kyx: stiffness coefficient [N/m]
        """
    def create_selection(self, name: str, objects: list[SciaObject]) -> Selection:
        """ ::version(v14.1.0)

        Method to construct a named selection.

        :param name: name which will be shown in SCIA
        :param objects: object(s) created within this model
        """
    def create_arbitrary_profile_span(self, length: float, type_of_css: ArbitraryProfileSpan.TypeOfCss, cross_section_start: CrossSection, cross_section_end: CrossSection, alignment: ArbitraryProfileSpan.Alignment) -> ArbitraryProfileSpan:
        """ Method to construct an arbitrary profile span, which is necessary to construct an arbitrary profile.

        :param length: length of the span
        :param type_of_css: enumeration of cross-section types
        :param cross_section_start: previously created cross-section object at the start point
        :param cross_section_end: previously created cross-section object at the end point
        :param alignment: enumeration of alignment types
        """
    def create_rectangular_cross_section(self, name: str, material: Material, width: float, height: float) -> RectangularCrossSection:
        """ Method to construct a rectangular cross-section.

        :param name: name which will be shown in SCIA
        :param material: material of the cross-section
        :param width: width of the cross-section in [m]
        :param height: height of the cross-section in [m]
        """
    def create_circular_cross_section(self, name: str, material: Material, diameter: float) -> CircularCrossSection:
        """ Method to construct a circular cross-section.

        :param name: name which will be shown in SCIA
        :param material: material of the cross-section
        :param diameter: diameter of the cross-section in [m]
        """
    def create_circular_hollow_cross_section(self, name: str, material: Material, diameter: float, thickness: float) -> CircularHollowCrossSection:
        """ Method to construct a circular hollow cross-section.

        :param name: name which will be shown in SCIA
        :param material: material of the cross-section
        :param diameter: diameter of the cross-section in [m]
        :param thickness: thickness in [m]
        """
    def create_circular_composed_cross_section(self, name: str, material: Material, material_2: Material, diameter: float, thickness: float) -> CircularComposedCrossSection:
        """ Method to construct a circular cross-section, composed of two materials.

        :param name: name which will be shown in SCIA
        :param material: outer material of the cross-section
        :param material_2: inner material of the cross-section
        :param diameter: diameter of the cross-section in [m]
        :param thickness: thickness in [m]
        """
    def create_numerical_cross_section(self, name: str, material: Material, *, A: float = None, Ay: float = None, Az: float = None, AL: float = None, AD: float = None, cYUCS: float = None, cZUCS: float = None, alpha: float = None, Iy: float = None, Iz: float = None, Wely: float = None, Welz: float = None, Wply: float = None, Wplz: float = None, Mply_plus: float = None, Mply_min: float = None, Mplz_plus: float = None, Mplz_min: float = None, dy: float = None, dz: float = None, It: float = None, Iw: float = None, beta_y: float = None, beta_z: float = None) -> NumericalCrossSection:
        """ Method to construct a numerical cross-section.

        :param name: name which will be shown in SCIA
        :param material: material of the cross-section
        :param A: cross-sectional area [m²]
        :param Ay: shear area in y-direction [m²]
        :param Az: shear area in z-direction [m²]
        :param AL: circumference per unit length [m²/m]
        :param AD: drying surface per unit length [m²/m]
        :param cYUCS: centroid in y-direction of input axis system [mm]
        :param cZUCS: centroid in z-direction of input axis system [mm]
        :param alpha: rotation angle of axis system [deg]
        :param Iy: moment of inertia about the y-axis [m⁴]
        :param Iz: moment of inertia about the z-axis [m⁴]
        :param Wely: elastic section modulus about the y-axis [m³]
        :param Welz: elastic section modulus about the z-axis [m³]
        :param Wply: plastic section modulus about the y-axis [m³]
        :param Wplz: plastic section modulus about the z-axis [m³]
        :param Mply_plus: plastic moment about the y-axis for positive My moment [Nm]
        :param Mply_min: plastic moment about the y-axis for negative My moment [Nm]
        :param Mplz_plus: plastic moment about the z-axis for positive My moment [Nm]
        :param Mplz_min: plastic moment about the z-axis for negative My moment [Nm]
        :param dy: shear center coordinate in y-axis, measured from centroid [mm]
        :param dz: shear center coordinate in z-axis, measured from centroid [mm]
        :param It: torsional constant [m⁴]
        :param Iw: warping constant [m⁶]
        :param beta_y: mono-symmetry constant about the y-axis [mm]
        :param beta_z: mono-symmetry constant about the z-axis [mm]
        """
    def create_library_cross_section(self, section: LibraryCrossSection.Section, profile: str, material: Material, *, name: str = None) -> LibraryCrossSection:
        ''' ::version(v13.1.0)

        Method to construct a cross-section that is part of the cross-section library.

        :param section: section type (e.g. LibraryCrossSection.Section.I)
        :param profile: profile name including dimensions (e.g. "SHS30/30/2.0")
        :param material: material of the cross-section
        :param name: name of the cross-section (default: \'CS{i}\')
        '''
    def create_general_cross_section_element(self, name: str, element_type: GeneralCrossSectionElement.Type, points: Sequence[tuple[float, float]], *, material: Material = None) -> GeneralCrossSectionElement:
        """ ::version(v14.7.0)

        Construct a general cross-section element, which is necessary to construct a general cross-section.

        :param name: name of the element
        :param element_type: element type
        :param points: outline of the element
        :param material: material of the element
        """
    def create_general_cross_section(self, elements: Sequence[GeneralCrossSectionElement], *, name: str = None) -> GeneralCrossSection:
        """ ::version(v14.7.0)

        Construct a general cross-section.

        :param name: name of the cross-section (default: 'CS{i}')
        :param elements: elements (polygon + openings) that build up the cross-section
        """
    def create_node(self, name: str, x: float, y: float, z: float) -> Node:
        """ Method to construct a node.

        :param name: name which will be shown in SCIA
        :param x: X-coordinate in [m]
        :param y: Y-coordinate in [m]
        :param z: Z-coordinate in [m]
        """
    def create_beam(self, begin_node: Node, end_node: Node, cross_section: CrossSection, *, name: str = None, ez: float = None, lcs_rotation: float = None, layer: Layer = None) -> Beam:
        """ Method to construct a beam.

        :param begin_node: node object (:meth:`~.create_node`) at the start of the beam.
        :param end_node: node object (:meth:`~.create_node`) at the end of the beam.
        :param cross_section: previously created cross-section object
        :param name: name which will be shown in SCIA (default: 'B{i}')
        :param ez: eccentricity in Z-direction w.r.t. the beam's center line in [m] (default: 0)
        :param lcs_rotation: rotation of local coordinate system [deg] (default: 0)
        :param layer: layer object (:meth:`~.create_layer`) to which the beam will be added
        """
    def create_cross_link(self, beam_1: Beam, beam_2: Beam, *, name: str = None) -> CrossLink:
        """ ::version(v13.1.0)

        Method to construct a cross-link, connecting two beams.

        :param beam_1: first beam (:meth:`~.create_beam`)
        :param beam_2: second beam (:meth:`~.create_beam`)
        :param name: name which will be shown in SCIA (default: 'CL{i}')
        """
    def create_arbitrary_profile(self, name: str, beam: Beam, c_def: ArbitraryProfile.CDef, cross_section: CrossSection, spans: list[ArbitraryProfileSpan]) -> ArbitraryProfile:
        """ Method to construct an arbitrary profile.

        :param name: name which will be shown in SCIA
        :param beam: beam object (:meth:`~.create_beam`).
        :param c_def: enumeration of coordinate definition types
        :param cross_section: previously created cross-section object
        :param spans: list of arbitrary profile span objects (:meth:`~.create_arbitrary_profile_span`).
        """
    def create_hinge_on_beam(self, beam: Beam, position: HingeOnBeam.Position, *, name: str = None, freedom_ux: HingeOnBeam.Freedom = ..., freedom_uy: HingeOnBeam.Freedom = ..., freedom_uz: HingeOnBeam.Freedom = ..., freedom_fix: HingeOnBeam.Freedom = ..., freedom_fiy: HingeOnBeam.Freedom = ..., freedom_fiz: HingeOnBeam.Freedom = ..., stiffness_ux: float = 0, stiffness_uy: float = 0, stiffness_uz: float = 0, stiffness_fix: float = 0, stiffness_fiy: float = 0, stiffness_fiz: float = 0) -> HingeOnBeam:
        """ Create a hinge on a beam.

        :param beam: Beam of appliance (:meth:`~.create_beam`).
        :param position: Position of appliance.
        :param name: Name of the hinge (default: 'H{i}').
        :param freedom_ux: Freedom in ux (default: rigid).
        :param freedom_uy: Freedom in uy (default: rigid).
        :param freedom_uz: Freedom in uz (default: rigid).
        :param freedom_fix: Freedom in fix (default: rigid).
        :param freedom_fiy: Freedom in fiy (default: free).
        :param freedom_fiz: Freedom in fiz (default: rigid).
        :param stiffness_ux: Stiffness in ux [N/m], only used if freedom in ux = flexible (default: 0.0).
        :param stiffness_uy: Stiffness in uy [N/m], only used if freedom in uy = flexible (default: 0.0).
        :param stiffness_uz: Stiffness in uz [N/m], only used if freedom in uz = flexible (default: 0.0).
        :param stiffness_fix: Stiffness in fix [Nm/rad], only used if freedom in fix = flexible (default: 0.0).
        :param stiffness_fiy: Stiffness in fiy [Nm/rad], only used if freedom in fiy = flexible (default: 0.0).
        :param stiffness_fiz: Stiffness in fiz [Nm/rad], only used if freedom in fiz = flexible (default: 0.0).
        """
    def create_section_on_beam(self, name: str, beam: Beam, c_def: SectionOnBeam.CDef, position_x: float, origin: SectionOnBeam.Origin, repeat: int, delta_x: float) -> SectionOnBeam:
        """ Method to construct a section on a beam, which can be used to receive calculation results on its position.

        :param name: name which will be shown in SCIA
        :param beam: beam object (:meth:`~.create_beam`).
        :param c_def: enumeration of coordinate definition types
        :param position_x: position of the section on the beam
        :param origin: enumeration of origin types
        :param repeat: number of section defined at the same time
        :param delta_x: if repeat is greater than 1, this value defines the distance between individual sections
        """
    def create_section_on_plane(self, point_1: tuple[float, float, float], point_2: tuple[float, float, float], *, name: str, draw: SectionOnPlane.Draw = None, direction_of_cut: tuple[float, float, float] = None) -> SectionOnPlane:
        """ Method to construct a section on a plane, which can be used to receive calculation results on its position.

        :param point_1: tuple of coordinates (x, y, z) of the start position in [m]
        :param point_2: tuple of coordinates (x, y, z) of the end position in [m]
        :param name: name which will be shown in SCIA (default: SE{i})
        :param draw: defines the plane in which the section is drawn (default: Z_DIRECTION)
        :param direction_of_cut: in-plane vector (x, y, z) which defines the direction of cut in [m] (default: (0, 0, 1))
        """
    def create_rigid_arm(self, name: str, master_node: Node, slave_node: Node, hinge_on_master: bool, hinge_on_slave: bool) -> RigidArm:
        """
        Method to construct a rigid arm.

        :param name: name which will be shown in SCIA
        :param master_node: node object (:meth:`~.create_node`).
        :param slave_node: node object (:meth:`~.create_node`).
        :param hinge_on_master: True to insert a hinge on the master node
        :param hinge_on_slave: True to insert a hinge on the slave node
        """
    def create_plane(self, corner_nodes: list[Node], thickness: float, *, material: Material, name: str = None, plane_type: Plane.Type = None, layer: Layer = None, internal_nodes: list[Node] = None, swap_orientation: bool = None, lcs_rotation: float = None, fem_model: Plane.FEMModel = None, orthotropy: Orthotropy = None) -> Plane:
        """ Method to construct a 2D member.

        :param corner_nodes: list of node objects located at the corners
        :param thickness: thickness of the plane in [m]
        :param material: :class:`~.scia.material.Material` of the plane
        :param name: name which will be shown in SCIA (default: 'S{i}')
        :param plane_type: enumeration of plane types (default: PLATE)
        :param layer: layer object (:meth:`~.create_layer`) to which the plane will be added
        :param internal_nodes: list of internal node objects (default: None)
        :param swap_orientation: whereas to swap the plate orientation (default: False)
        :param lcs_rotation: rotation of the local coordinate system [deg] (default: 0.0)
        :param fem_model: FEM model to be used in the calculation (default: isotropic)
        :param orthotropy: type of orthotropy (only for fem_model = ORTHOTROPIC)
        """
    def create_circular_plane(self, center_node: Node, diameter: float, thickness: float, *, material: Material, axis: Vector | tuple[float, float, float] = None, name: str = None, plane_type: Plane.Type = None, layer: Layer = None, internal_nodes: list[Node] = None, swap_orientation: bool = None, lcs_rotation: float = None, fem_model: Plane.FEMModel = None, orthotropy: Orthotropy = None) -> Plane:
        """ Method to construct a circular 2D member.

        :param center_node: node object (:meth:`~.create_node`) located at the center of the plane
        :param diameter: diameter of the plane [m]
        :param thickness: thickness of the plane [m]
        :param material: :class:`~.scia.material.Material` of the plane
        :param axis: axis direction (default: (0, 0, 1))
        :param name: name which will be shown in SCIA (default: 'S{i}')
        :param plane_type: enumeration of plane types (default: PLATE)
        :param layer: layer object (:meth:`~.create_layer`) to which the plane will be added
        :param internal_nodes: list of internal node objects (default: None)
        :param swap_orientation: whereas to swap the plate orientation (default: False)
        :param lcs_rotation: rotation of the local coordinate system [deg] (default: 0.0)
        :param fem_model: FEM model to be used in the calculation (default: isotropic)
        :param orthotropy: type of orthotropy (only for fem_model = ORTHOTROPIC)
        """
    def create_open_slab(self, name: str, plane: Plane, corner_nodes: list[Node]) -> OpenSlab:
        """ Method to construct an open slab in a 2D member.

        :param name: name which will be shown in SCIA
        :param plane: plane object (:meth:`~.create_plane`).
        :param corner_nodes: list of node objects located at the corners
        """
    def create_internal_edge(self, plane: Plane, node_1: Node, node_2: Node, *, name: str = None) -> InternalEdge:
        """ Method to construct an internal edge in a 2D member.

        :param plane: plane object (:meth:`~.create_plane`)
        :param node_1: node object (:meth:`~.create_node`) at the start of the edge
        :param node_2: node object (:meth:`~.create_node`) at the end of the edge
        :param name: name which will be shown in SCIA (default: 'ES{i}')
        """
    def create_integration_strip(self, plane: Plane, point_1: tuple[float, float, float], point_2: tuple[float, float, float], width: float) -> IntegrationStrip:
        """
        Method to construct an integration strip, which can be used to receive calculation results on its position.

        :param plane: plane object (:meth:`~.create_plane`).
        :param point_1: tuple of coordinates (x, y, z) of the start position in [m]
        :param point_2: tuple of coordinates (x, y, z) of the end position in [m]
        :param width: width of the strip in [m]
        """
    def create_averaging_strip(self, plane: Plane, *, strip_type: AveragingStrip.Type, point_1: tuple[float, float, float], width: float, length: float, angle: float, direction: AveragingStrip.Direction, name: str = None) -> AveragingStrip:
        """ ::version(v14.3.0)

        Method to construct an averaging strip, which can be used for the automatic averaging of peak results.

        :param plane: plane object (:meth:`~.create_plane`).
        :param strip_type: Currently only Point type is supported
        :param point_1: tuple of coordinates (x, y, z) of the center position in [m]
        :param width: width of the strip in [m]
        :param length: length of the strip in [m]
        :param angle: defines the direction of the strip [deg]
        :param direction: direction in which the averaging is to be calculated
        :param name: name which will be shown in SCIA (default: 'RS{i}')
        """
    def create_point_support(self, name: str, node: Node, spring_type: PointSupport.Type, freedom: tuple[PointSupport.Freedom, PointSupport.Freedom, PointSupport.Freedom, PointSupport.Freedom, PointSupport.Freedom, PointSupport.Freedom], stiffness: tuple[float, float, float, float, float, float], c_sys: PointSupport.CSys, default_size: float = 0.2, *, angle: tuple[float, float, float] = None) -> PointSupport:
        """ Method to construct a point support.

        :param name: name which will be shown in SCIA
        :param node: node object (:meth:`~.create_node`) to which the support will be attached.
        :param spring_type: enumeration of spring types
        :param freedom: tuple of component constraints in the order (X, Y, Z, Rx, Ry, Rz)
        :param stiffness: tuple of component stiffness in the order (X, Y, Z, Rx, Ry, Rz) in [N/m]
        :param c_sys: enumeration of coordinate system types
        :param default_size: default size in [m]
        :param angle: angle (Rx, Ry, Rz) [deg] of the support around the respective global X-, Y- and Z-axis
        """
    def create_point_support_on_beam(self, beam: Beam, *, name: str = None, x: PointSupportLine.Freedom = None, stiffness_x: float = None, y: PointSupportLine.Freedom = None, stiffness_y: float = None, z: PointSupportLine.Freedom = None, stiffness_z: float = None, rx: PointSupportLine.Freedom = None, stiffness_rx: float = None, ry: PointSupportLine.Freedom = None, stiffness_ry: float = None, rz: PointSupportLine.Freedom = None, stiffness_rz: float = None, default_size: float = None, c_sys: PointSupportLine.CSys = None, c_def: PointSupportLine.CDef = None, position_x: float = None, origin: PointSupportLine.Origin = None, repeat: int = None, delta_x: float = None) -> PointSupportLine:
        """ Method to construct a point support on a beam.

        :param beam: beam object (:meth:`~.create_beam`) to which the line support will be applied
        :param name: name which will be shown in SCIA (default: 'Sb{i}')
        :param x: constraint type in X-direction (default: RIGID)
        :param stiffness_x: stiffness in X-direction [N/m] (only for x = FLEXIBLE)
        :param y: constraint type in Y-direction (default: RIGID)
        :param stiffness_y: stiffness in Y-direction [N/m] (only for y = FLEXIBLE)
        :param z: constraint type in Z-direction (default: RIGID)
        :param stiffness_z: stiffness in Z-direction [N/m] (only for z = FLEXIBLE)
        :param rx: constraint type in X-rotation (default: RIGID)
        :param stiffness_rx: stiffness in X-rotation [Nm/rad] (only for rx = FLEXIBLE)
        :param ry: constraint type in Y-rotation (default: RIGID)
        :param stiffness_ry: stiffness in Y-rotation [Nm/rad] (only for ry = FLEXIBLE)
        :param rz: constraint type in Z-rotation (default: RIGID)
        :param stiffness_rz: stiffness in Z-rotation [Nm/rad] (only for rz = FLEXIBLE)
        :param default_size: size of the support [m] (default: 0.2)
        :param c_sys: coordinate system (default: GLOBAL)
        :param c_def: c_def: coordinate definition (default: RELATIVE)
        :param position_x: position of the load ([m] if c_def = ABSOLUTE, else [-]) (default: 0)
        :param origin: reference for position_x (default: FROM_START)
        :param repeat: number of uniformly distributed supports (default: 1)
        :param delta_x: distance between supports ([m] if c_def = ABSOLUTE, else [-]) (only for repeat > 1)
        """
    def create_line_support_on_beam(self, beam: Beam, *, name: str = None, x: LineSupportLine.Freedom = None, stiffness_x: float = None, function_x: NonLinearFunction = None, y: LineSupportLine.Freedom = None, stiffness_y: float = None, function_y: NonLinearFunction = None, z: LineSupportLine.Freedom = None, stiffness_z: float = None, function_z: NonLinearFunction = None, rx: LineSupportLine.Freedom = None, stiffness_rx: float = None, function_rx: NonLinearFunction = None, ry: LineSupportLine.Freedom = None, stiffness_ry: float = None, function_ry: NonLinearFunction = None, rz: LineSupportLine.Freedom = None, stiffness_rz: float = None, function_rz: NonLinearFunction = None, c_sys: LineSupportLine.CSys = None, extent: LineSupportLine.Extent = None, c_def: LineSupportLine.CDef = None, position_x1: float = None, position_x2: float = None, origin: LineSupportLine.Origin = None) -> LineSupportLine:
        """ Method to construct a line support on a beam.

        :param beam: beam object (:meth:`~.create_beam`) to which the line support will be applied
        :param name: name which will be shown in SCIA (default: 'Slb{i}')
        :param x: constraint type in X-direction (default: RIGID)
        :param stiffness_x: stiffness in X-direction [N/m2] (only for x = FLEXIBLE | FLEXIBLE_PRESS_ONLY |
         FLEXIBLE_TENSION_ONLY | NONLINEAR)
        :param function_x: non-linear function in X-direction (only for x = NONLINEAR)
        :param y: constraint type in Y-direction (default: RIGID)
        :param stiffness_y: stiffness in Y-direction [N/m2] (only for y = FLEXIBLE | FLEXIBLE_PRESS_ONLY |
         FLEXIBLE_TENSION_ONLY | NONLINEAR)
        :param function_y: non-linear function in Y-direction (only for y = NONLINEAR)
        :param z: constraint type in Z-direction (default: RIGID)
        :param stiffness_z: stiffness in Z-direction [N/m2] (only for z = FLEXIBLE | FLEXIBLE_PRESS_ONLY |
         FLEXIBLE_TENSION_ONLY | NONLINEAR)
        :param function_z: non-linear function in Z-direction (only for z = NONLINEAR)
        :param rx: constraint type in X-rotation (default: RIGID)
        :param stiffness_rx: stiffness in X-rotation [Nm/m/rad] (only for rx = FLEXIBLE | NONLINEAR)
        :param function_rx: non-linear function in X-rotation (only for rx = NONLINEAR)
        :param ry: constraint type in Y-rotation (default: RIGID)
        :param stiffness_ry: stiffness in Y-rotation [Nm/m/rad] (only for ry = FLEXIBLE | NONLINEAR)
        :param function_ry: non-linear function in Y-rotation (only for ry = NONLINEAR)
        :param rz: constraint type in Z-rotation (default: RIGID)
        :param stiffness_rz: stiffness in Z-rotation [Nm/m/rad] (only for rz = FLEXIBLE | NONLINEAR)
        :param function_rz: non-linear function in Z-rotation (only for rz = NONLINEAR)
        :param c_sys: coordinate system (default: LOCAL)
        :param extent: extension of support (default: FULL)
        :param c_def: coordinate definition (default: RELATIVE)
        :param position_x1: start of support along the edge with respect to origin ([m] if c_def = ABSOLUTE, else [-])
         (default: 0.0)
        :param position_x2: end of support along the edge with respect to origin ([m] if c_def = ABSOLUTE, else [-])
         (default: 1.0)
        :param origin: reference for position_x1 and position_x2 (default: FROM_START)
        """
    def create_line_support_on_plane(self, edge: tuple[Plane, int] | InternalEdge, *, name: str = None, x: LineSupportSurface.Freedom = None, stiffness_x: float = None, y: LineSupportSurface.Freedom = None, stiffness_y: float = None, z: LineSupportSurface.Freedom = None, stiffness_z: float = None, rx: LineSupportSurface.Freedom = None, stiffness_rx: float = None, ry: LineSupportSurface.Freedom = None, stiffness_ry: float = None, rz: LineSupportSurface.Freedom = None, stiffness_rz: float = None, c_sys: LineSupportSurface.CSys = None, c_def: LineSupportSurface.CDef = None, position_x1: float = None, position_x2: float = None, origin: LineSupportSurface.Origin = None) -> LineSupportSurface:
        """ Method to construct a line support on a plane edge.

        :param edge: tuple of the plane object (:meth:`~.create_plane`) and edge number to which the load
         should be applied (1 = between plane.corner_nodes[0] and plane.corner_nodes[1], etc.),
         or InternalEdge (:meth:`~.create_internal_edge`)
        :param name: name which will be shown in SCIA (default: 'Sle{i}')
        :param x: constraint type in X-direction (default: FREE)
        :param stiffness_x: stiffness in X-direction [N/m2] (only for x = FLEXIBLE)
        :param y: constraint type in Y-direction (default: FREE)
        :param stiffness_y: stiffness in Y-direction [N/m2] (only for y = FLEXIBLE)
        :param z: constraint type in Z-direction (default: FREE)
        :param stiffness_z: stiffness in Z-direction [N/m2] (only for z = FLEXIBLE)
        :param rx: constraint type in X-rotation (default: FREE)
        :param stiffness_rx: stiffness in X-rotation [Nm/m/rad] (only for rx = FLEXIBLE)
        :param ry: constraint type in Y-rotation (default: FREE)
        :param stiffness_ry: stiffness in Y-rotation [Nm/m/rad] (only for ry = FLEXIBLE)
        :param rz: constraint type in Z-rotation (default: FREE)
        :param stiffness_rz: stiffness in Z-rotation [Nm/m/rad] (only for rz = FLEXIBLE)
        :param c_sys: coordinate system (default: GLOBAL)
        :param c_def: coordinate definition (default: RELATIVE)
        :param position_x1: start of support along the edge with respect to origin ([m] if c_def = ABSOLUTE, else [-])
         (default: 0.0)
        :param position_x2: end of support along the edge with respect to origin ([m] if c_def = ABSOLUTE, else [-])
         (default: 1.0)
        :param origin: reference for position_x1 and position_x2 (default: FROM_START)
        """
    def create_surface_support(self, plane: Plane, subsoil: Subsoil, *, name: str = None) -> SurfaceSupportSurface:
        """ Method to construct a surface support.

        :param plane: plane object (:meth:`~.create_plane`) to which the support will be attached
        :param subsoil: subsoil object (:meth:`~.create_subsoil`) representing the support
        :param name: name which will be shown in SCIA
        """
    def create_hinge_on_plane(self, edge: tuple[Plane, int] | InternalEdge, *, name: str = None, ux: HingeOnPlane.Freedom = None, stiffness_ux: float = None, uy: HingeOnPlane.Freedom = None, stiffness_uy: float = None, uz: HingeOnPlane.Freedom = None, stiffness_uz: float = None, fix: HingeOnPlane.Freedom = None, stiffness_fix: float = None, c_def: HingeOnPlane.CDef = None, position_x1: float = None, position_x2: float = None, origin: HingeOnPlane.Origin = None) -> HingeOnPlane:
        """ Method to construct a hinge on a plane edge.

        :param edge: tuple of a plane object (:meth:`~.create_plane`) and edge number to which the hinge
         will be attached (1 = between plane.corner_nodes[0] and plane.corner_nodes[1], etc.),
         or InternalEdge (:meth:`~.create_internal_edge`)
        :param name: name which will be shown in SCIA (default: 'L{i}')
        :param ux: Freedom in ux (default: RIGID).
        :param stiffness_ux: Stiffness in ux [N/m2], only used if freedom in ux = flexible (default: 0.0).
        :param uy: Freedom in uy (default: RIGID).
        :param stiffness_uy: Stiffness in uy [N/m2], only used if freedom in uy = flexible (default: 0.0).
        :param uz: Freedom in uz (default: RIGID).
        :param stiffness_uz: Stiffness in uz [N/m2], only used if freedom in uz = flexible (default: 0.0).
        :param fix: Freedom in fix (default: FREE).
        :param stiffness_fix: Stiffness in fix [Nm/m/rad], only used if freedom in fix = flexible (default: 0.0).
        :param c_def: coordinate definition (default: RELATIVE)
        :param position_x1: position of p1 along the edge with respect to origin ([m] if c_def = ABSOLUTE, else [-])
         (default: 0.0)
        :param position_x2: position of p2 along the edge with respect to origin ([m] if c_def = ABSOLUTE, else [-])
         (default: 1.0)
        :param origin: reference for position_x1 and position_x2 (default: FROM_START)
        """
    def create_load_group(self, name: str, load_option: LoadGroup.LoadOption, relation: LoadGroup.RelationOption = None, load_type: LoadGroup.LoadTypeOption = None) -> LoadGroup:
        """ Method to construct a load group.

        :param name: name which will be shown in SCIA
        :param load_option: enumeration of load option types
        :param relation: enumeration of relation types
        :param load_type: enumeration of load types
        """
    def create_permanent_load_case(self, name: str, description: str, load_group: LoadGroup, load_type: LoadCase.PermanentLoadType, direction: LoadCase.Direction = None, primary_effect: LoadCase = None) -> PermanentLoadCase:
        """ Method to construct a permanent load case.

        :param name: name which will be shown in SCIA
        :param description: description which will be shown in SCIA
        :param load_group: load group object (:meth:`~.create_load_group`) in which the load case should be placed.
        :param load_type: permanent load types
        :param direction: load direction in case of a *SELF_WEIGHT* load type (default: NEG_Z)
        :param primary_effect: previously created load case object in case the selected load type is *PRIMARY_EFFECT*
        """
    def create_variable_load_case(self, name: str, description: str, load_group: LoadGroup, load_type: LoadCase.VariableLoadType, specification: LoadCase.Specification = None, duration: LoadCase.Duration = None, primary_effect: LoadCase = None) -> VariableLoadCase:
        """ Method to construct a variable load case.

        :param name: name which will be shown in SCIA
        :param description: description which will be shown in SCIA
        :param load_group: load group object (:meth:`~.create_load_group`) in which the load case should be placed.
        :param load_type: enumeration of variable load types
        :param specification: enumeration of specification types
        :param duration: enumeration of duration types
        :param primary_effect: previously created load case object in case the selected load type is *PRIMARY_EFFECT*
        """
    def create_load_combination(self, name: str, load_type: LoadCombination.Type, load_cases: dict[LoadCase, float], *, description: str = None) -> LoadCombination:
        """ Method to construct a load combination.

        :param name: name which will be shown in SCIA
        :param load_type: enumeration of load types
        :param load_cases: dictionary of previously created load case object(s) with corresponding coefficient
        :param description: description of the load combination ::version(v13.1.0)
        """
    def create_nonlinear_load_combination(self, load_type: NonLinearLoadCombination.Type, load_cases: dict[LoadCase, float], *, name: str = None, description: str = None) -> NonLinearLoadCombination:
        """ Create a non-linear load combination.

        :param load_type: type of combination
        :param load_cases: dictionary of previously created load case object(s) with corresponding coefficient
        :param name: name which will be shown in SCIA (default: 'NC{i}')
        :param description: description of the load combination ::version(v13.1.0)
        """
    def create_result_class(self, name: str, combinations: list[LoadCombination] = None, nonlinear_combinations: list[NonLinearLoadCombination] = None) -> ResultClass:
        """ Method to construct a result class.

        :param name: name which will be shown in SCIA
        :param combinations: list of load combination objects (:meth:`~.create_load_combination`)
        :param nonlinear_combinations: list of nonlinear load combination objects (:meth:`~.create_nonlinear_load_combination`)
        """
    def create_point_load_node(self, node: Node, load_case: LoadCase, load: float, *, name: str = None, direction: PointLoadNode.Direction = None, c_sys: PointLoadNode.CSys = None, angle: tuple[float, float, float] = None) -> PointLoadNode:
        """ Method to construct a point load in a node.

        :param node: node object (:meth:`~.create_node`) on which the load should be applied
        :param load_case: previously created load case object in which the load should be placed
        :param load: magnitude of the load in [N]
        :param name: name which will be shown in SCIA (default: 'F{i}')
        :param direction: direction of the load (default: Z)
        :param c_sys: coordinate system (default: global)
        :param angle: angle (Rx, Ry, Rz) [deg] of the load around the respective global X-, Y- and Z-axis
        """
    def create_point_load(self, name: str, load_case: LoadCase, beam: Beam, direction: PointLoad.Direction, load_type: PointLoad.Type, load_value: float, c_sys: PointLoad.CSys = None, c_def: PointLoad.CDef = None, position_x: float = None, origin: PointLoad.Origin = None, repeat: int = None, ey: float = None, ez: float = None, *, angle: tuple[float, float, float] = None) -> PointLoad:
        """ Method to construct a point load on a beam.

        :param name: name which will be shown in SCIA
        :param load_case: previously created load case object in which the load should be placed
        :param beam: beam object (:meth:`~.create_beam`) to which the load should be applied
        :param direction: enumeration of directions
        :param load_type: enumeration of load types
        :param load_value: magnitude of the load in [N]
        :param c_sys: enumeration of coordinate system types (default: global)
        :param c_def: enumeration of coordinate definition types (default: relative)
        :param position_x: position of the load (default: 0)
        :param origin: enumeration of origin types (default: from start)
        :param repeat: number of loads acting on the beam, distributed uniformly (default: 1)
        :param ey: eccentricity in Y-direction w.r.t. the beam's center line in [m] (default: 0)
        :param ez: eccentricity in Z-direction w.r.t. the beam's center line in [m] (default: 0)
        :param angle: angle (Rx, Ry, Rz) [deg] of the load around the respective X-, Y- and Z-axis (default: 0)
        """
    def create_point_moment_node(self, node: Node, load_case: LoadCase, load: float, direction: PointMomentNode.Direction, name: str = None, c_sys: PointMomentNode.CSys = ...) -> PointMomentNode:
        """ Create a point moment on an existing node.

        :param node: Node of appliance (:meth:`~.create_node`).
        :param load_case: Previously created load case of appliance.
        :param load: Magnitude of the load [Nm].
        :param direction: Direction of the load.
        :param name: Name of the load in SCIA (default: 'M{i}').
        :param c_sys: Coordinate system (default: global).
        """
    def create_line_load(self, name: str, load_case: LoadCase, beam: Beam, load_type: LineLoad.Type, distribution: LineLoad.Distribution, load_start: float, load_end: float, direction: LineLoad.Direction, position_start: float, position_end: float, c_def: LineLoad.CDef, c_sys: LineLoad.CSys, origin: LineLoad.Origin, ey: float, ez: float) -> LineLoad:
        """ Method to construct a line load on a beam.

        :param name: name which will be shown in SCIA
        :param load_case: previously created load case object in which the load should be placed
        :param beam: beam object (:meth:`~.create_beam`) to which the load should be applied
        :param load_type: enumeration of load types
        :param distribution: enumeration of distribution options
        :param load_start: magnitude of the load at the start point in [N]
        :param load_end: magnitude of the load at the end point in [N]
        :param direction: enumeration of directions
        :param position_start: position of the start point on the beam in [m]
        :param position_end: position of the end point on the beam in [m]
        :param c_def: enumeration of coordinate definition types
        :param c_sys: enumeration of coordinate system types
        :param origin: enumeration of origin types
        :param ey: eccentricity in Y-direction w.r.t. the beam's center line in [m]
        :param ez: eccentricity in Z-direction w.r.t. the beam's center line in [m]
        """
    def create_line_moment_on_beam(self, beam: Beam, load_case: LoadCase, m1: float, m2: float = None, *, name: str = None, direction: LineMomentOnBeam.Direction = None, c_def: LineMomentOnBeam.CDef = None, position_x1: float = None, position_x2: float = None, origin: LineMomentOnBeam.Origin = None) -> LineMomentOnBeam:
        """ Method to construct a line moment on a beam.

        :param beam: beam object (:meth:`~.create_beam`) to which the load should be applied
        :param load_case: previously created load case object in which the load should be applied
        :param m1: magnitude of the moment [Nm/m] on point 1
        :param m2: magnitude of the moment [Nm/m] on point 2. None for uniform load (with magnitude m1) (default: None)
        :param name: name which will be shown in SCIA (default: 'LM{i}')
        :param direction: direction of the moment (default: Z)
        :param c_def: coordinate definition (default: RELATIVE)
        :param position_x1: position of p1 along the beam with respect to origin ([m] if c_def = ABSOLUTE, else [-])
         (default: 0.0)
        :param position_x2: position of p2 along the beam with respect to origin ([m] if c_def = ABSOLUTE, else [-])
         (default: 1.0)
        :param origin: reference for position_x1 and position_x2 (default: FROM_START)
        """
    def create_line_moment_on_plane(self, edge: tuple[Plane, int] | InternalEdge, m1: float, m2: float = None, *, load_case: LoadCase, name: str = None, direction: LineMomentOnPlane.Direction = None, c_def: LineMomentOnPlane.CDef = None, position_x1: float = None, position_x2: float = None, origin: LineMomentOnPlane.Origin = None) -> LineMomentOnPlane:
        """ Method to construct a line moment on a plane edge.

        :param edge: tuple of the plane object (:meth:`~.create_plane`) and edge number to which the load
         should be applied (1 = between plane.corner_nodes[0] and plane.corner_nodes[1], etc.),
         or InternalEdge (:meth:`~.create_internal_edge`)
        :param m1: magnitude of the moment [Nm/m] on point 1
        :param m2: magnitude of the moment [Nm/m] on point 2. None for uniform load (with magnitude m1) (default: None)
        :param load_case: previously created load case object in which the load should be applied
        :param name: name which will be shown in SCIA (default: 'LMS{i}')
        :param direction: direction of the moment (default: Z)
        :param c_def: coordinate definition (default: RELATIVE)
        :param position_x1: position of p1 along the edge with respect to origin ([m] if c_def = ABSOLUTE, else [-])
         (default: 0.0)
        :param position_x2: position of p2 along the edge with respect to origin ([m] if c_def = ABSOLUTE, else [-])
         (default: 1.0)
        :param origin: reference for position_x1 and position_x2 (default: FROM_START)
        """
    def create_line_load_on_plane(self, edge: tuple[Plane, int] | InternalEdge, p1: float, p2: float = None, *, load_case: LoadCase, direction: LineForceSurface.Direction = None, name: str = None, location: LineForceSurface.Location = None, c_sys: LineForceSurface.CSys = None, c_def: LineForceSurface.CDef = None, position_x1: float = None, position_x2: float = None, origin: LineForceSurface.Origin = None) -> LineForceSurface:
        """ Method to construct a line load on a plane edge.

        :param edge: tuple of a plane object (:meth:`~.create_plane`) and edge number to which the load
         will be applied (1 = between plane.corner_nodes[0] and plane.corner_nodes[1], etc.),
         or InternalEdge (:meth:`~.create_internal_edge`)
        :param p1: magnitude of the load [N/m] on point 1
        :param p2: magnitude of the load [N/m] on point 2. None for uniform load (with magnitude p1) (default: None)
        :param load_case: previously created load case object in which the load should be applied
        :param direction: direction of the load (default: Z)
        :param name: name which will be shown in SCIA (default: 'LFS{i}')
        :param location: location type (default: LENGTH)
        :param c_sys: coordinate system (default: LOCAL)
        :param c_def: coordinate definition (default: RELATIVE)
        :param position_x1: position of p1 along the edge with respect to origin ([m] if c_def = ABSOLUTE, else [-])
         (default: 0.0)
        :param position_x2: position of p2 along the edge with respect to origin ([m] if c_def = ABSOLUTE, else [-])
         (default: 1.0)
        :param origin: reference for position_x1 and position_x2 (default: FROM_START)
        """
    def create_surface_load(self, name: str, load_case: LoadCase, plane: Plane, direction: SurfaceLoad.Direction, load_type: SurfaceLoad.Type, load_value: float, c_sys: SurfaceLoad.CSys, location: SurfaceLoad.Location) -> SurfaceLoad:
        """ Method to construct a surface load on a plane.

        :param name: name which will be shown in SCIA
        :param load_case: previously created load case object in which the load should be placed
        :param plane: plane object (:meth:`~.create_plane`) to which the load should be applied
        :param direction: enumeration of directions
        :param load_type: enumeration of load types
        :param load_value: magnitude of the load in [N]
        :param c_sys: enumeration of coordinate system types
        :param location: enumeration of location options
        """
    def create_thermal_load(self, name: str, load_case: LoadCase, beam: Beam, distribution: ThermalLoad.Distribution, delta: float, left_delta: float, right_delta: float, top_delta: float, bottom_delta: float, position_start: float, position_end: float, c_def: ThermalLoad.CDef, origin: ThermalLoad.Origin) -> ThermalLoad:
        """ Method to construct a temperature load on a beam.

        :param name: name which will be shown in SCIA
        :param load_case: previously created load case object in which the load should be placed
        :param beam: beam object (:meth:`~.create_beam`) to which the load should be applied
        :param distribution: enumeration of distribution options
        :param delta: temperature difference in case of a *CONSTANT* distribution
        :param left_delta: temperature difference in +Y direction
        :param right_delta: temperature difference in -Y direction
        :param top_delta: temperature difference in +Z direction
        :param bottom_delta: temperature difference in -Z direction
        :param position_start: position of the start point on the beam in [m]
        :param position_end: position of the end point on the beam in [m]
        :param c_def: enumeration of coordinate definition types
        :param origin: enumeration of origin types
        """
    def create_thermal_surface_load(self, name: str, load_case: LoadCase, plane: Plane, delta: float = None, top_delta: float = None, bottom_delta: float = None) -> ThermalSurfaceLoad:
        """ Method to construct a temperature load on a plane.

        :param name: name which will be shown in SCIA
        :param load_case: previously created load case object in which the load should be placed
        :param plane: plane object (:meth:`~.create_plane`) to which the load should be applied
        :param delta: temperature difference in case of a constant distribution
        :param top_delta: temperature difference in +Z direction
        :param bottom_delta: temperature difference in -Z direction
        """
    def create_free_surface_load(self, name: str, load_case: LoadCase, direction: FreeSurfaceLoad.Direction, q1: float, q2: float = None, q3: float = None, points: list[tuple[float, float]] = None, *, distribution: FreeSurfaceLoad.Distribution = None, selection: list[Plane] = None) -> FreeSurfaceLoad:
        """ Method to construct a free surface load.

        Note: can only be defined in XY-plane.

        :param name: name which will be shown in SCIA
        :param load_case: previously created load case object in which the load should be placed
        :param direction: direction of the load
        :param q1: magnitude of the load in the first point in [N]
        :param q2: magnitude of the load in the second point in [N] (distribution = DIR_X | DIR_Y | POINTS only)
        :param q3: magnitude of the load in the third point in [N] (distribution = POINTS only)
        :param points: list of XY coordinates (at least 3). If distribution = DIR_X | DIR_Y: q1 and q2 are applied to
         points[0] and points[1] respectively. If distribution = POINTS: q1, q2 and q3 are applied to points[0],
         points[1] and points[2] respectively.
        :param distribution: distribution of the load (default: POINTS)
        :param selection: selection of 1 or more planes (:meth:`~.create_plane`) to generate the load
         on (default: select = auto)
        """
    def create_free_line_load(self, name: str, load_case: LoadCase, point_1: tuple[float, float], point_2: tuple[float, float], direction: FreeLineLoad.Direction, magnitude_1: float, magnitude_2: float) -> FreeLineLoad:
        """ Method to construct a free line load.

        :param name: name which will be shown in SCIA
        :param load_case: previously created load case object in which the load should be placed
        :param point_1: XY coordinate of the first point
        :param point_2: XY coordinate of the second point
        :param direction: enumeration of direction options
        :param magnitude_1: magnitude of the load in point_1 in [N]
        :param magnitude_2: magnitude of the load in point_2 in [N]
        """
    def create_free_point_load(self, name: str, load_case: LoadCase, direction: FreePointLoad.Direction, magnitude: float, position: tuple[float, float]) -> FreePointLoad:
        """ Method to construct a free point load.

        :param name: name which will be shown in SCIA
        :param load_case: previously created load case object in which the load should be placed
        :param direction: enumeration of direction options
        :param magnitude: magnitude of the load in [N]
        :param position: XY coordinate of the load
        """
    def generate_xml_input(self, as_file: bool = False) -> tuple[BytesIO, BytesIO] | tuple[File, File]:
        """ Returns the input file XML representation of the SCIA model and corresponding .def file.

        .. note:: This method needs to be mocked in (automated) unit and integration tests.

        :returns:

            - File if as_file = True
            - BytesIO if as_file = False (default)

        """

class OutputFileParser:
    """ Helper class to extract results from a SCIA output file (.xml).

    Example using BytesIO:

    .. code-block:: python

        xml_output_file = scia_analysis.get_xml_output_file()
        result_table = OutputFileParser.get_result(xml_output_file, 'Reactions')
        another_result_table = OutputFileParser.get_result(xml_output_file, '2D internal forces')


    Example using :class:`~viktor.core.File`:

    .. code-block:: python

        xml_output_file = scia_analysis.get_xml_output_file(as_file=True)
        with xml_output_file.open_binary() as f:
            result_table = OutputFileParser.get_result(f, 'Reactions')
            another_result_table = OutputFileParser.get_result(f, '2D internal forces')

    """
    @classmethod
    def get_result(cls, file: BinaryIO, table_name: str, *, parent: str = None) -> dict[str, dict]:
        ''' Retrieve the results of an output XML by \'table_name\'. This corresponds to the \'name\' attribute that is
        found in the XML table, e.g. "Result classes - UGT" in the example below:

        .. code-block::

            <container id="..." t="...">
                <table id="..." t="..." name="Result classes - UGT">

        In case indenting has been used in the SCIA I/O doc, multiple tables with the name \'table_name\' will be found.
        A parent name can be specified as input to account for this indenting (up to 1 indent level). If indenting is
        used but no parent name is specified, this method will return the first \'table_name\' table it can find.

        :param file: SCIA output file (.xml).
        :param table_name: Name of the result table to be extracted from the output XML.
        :param parent: Name of the parent, e.g. a result class.

        :raises :class:`viktor.errors.SciaParsingError`:
            - if table \'table_name\' could not be found in the provided output file
            - if no results were found in the XML table \'table_name\'
        '''
