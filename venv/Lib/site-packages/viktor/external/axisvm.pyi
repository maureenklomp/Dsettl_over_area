import abc
from ..core import File
from .external_program import ExternalProgram
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from enum import Enum
from io import BytesIO
from typing import Any, Iterator

__all__ = ['AxisVMAnalysis', 'CircleArc', 'CrossSection', 'CrossSectionInterface', 'Domain', 'DomainInterface', 'Line', 'LineInterface', 'LineSupport', 'LineSupportInterface', 'Load', 'LoadCase', 'LoadCaseInterface', 'LoadCombination', 'LoadCombinationInterface', 'LoadInterface', 'Material', 'MaterialInterface', 'Member', 'Model', 'Node', 'NodeInterface', 'NodeSupport', 'NodeSupportInterface', 'Object', 'Reference', 'ReferenceInterface', 'ResultInterface', 'Section', 'SectionInterface']

class AxisVMAnalysis(ExternalProgram):
    """
    Perform an analysis using AxisVM on a third-party worker. To start an analysis call the method
    :meth:`~.ExternalProgram.execute`, with an appropriate timeout (in seconds).

    To retrieve the results call the method :meth:`get_results`, after :meth:`~.ExternalProgram.execute`. The
    model file can be retrieved by calling :meth:`get_model_file` and the result by calling
    :meth:`get_result_file`.

    Usage:

    .. code-block:: python

        axisvm_analysis = AxisVMAnalysis(model, return_results=True, return_model=True)
        axisvm_analysis.execute(timeout=10)
        results = axisvm_analysis.get_results()
        model_file = axisvm_analysis.get_model_file()
        result_file = axisvm_analysis.get_result_file()

    Exceptions which can be raised during calculation:

     - :class:`~viktor.errors.ExecutionError`: generic error. Error message provides more information
    """
    def __init__(self, model: Model, *, return_results: bool = True, return_model: bool = False, report_template: BytesIO | File = None) -> None:
        """
        :param model: AxisVM model (:class:`Model`)
        :param return_results: If True, an analysis will be run and the result file is returned.
        :param return_model: If True, the model file is returned.
        :param report_template: (optional) report template that is added to AxisVM file
        """
    def get_results(self) -> dict:
        """ Retrieve the results (only if return_results = True).
        :meth:`~.ExternalAnalysis.execute` must be called first.

        The format of the returned dictionary is:

        .. code-block:: python

            {
                'Forces': <dict>,
                'Displacements': <dict>,
                'Sections': <dict>
            }
        """
    def get_model_file(self, *, as_file: bool = False) -> BytesIO | File | None:
        """ Retrieve the model file (only if return_model = True).
        :meth:`~.ExternalProgram.execute` must be called first.

        :param as_file: Return as BytesIO (default) or File ::version(v13.5.0)
        """
    def get_result_file(self, *, as_file: bool = False) -> BytesIO | File | None:
        """ Retrieve the result file (only if return_results = True).
        :meth:`~.ExternalProgram.execute` must be called first.

        :param as_file: Return as BytesIO (default) or File ::version(v13.5.0)
        """

class _Point3D:
    x: Incomplete
    y: Incomplete
    z: Incomplete
    def __init__(self, x: float, y: float, z: float) -> None: ...
    @classmethod
    def from_tuple(cls, xyz: tuple[float, float, float]) -> _Point3D: ...
    def serialize(self) -> dict: ...

class CircleArc:
    center: Incomplete
    normal_vector: Incomplete
    alpha: Incomplete
    def __init__(self, center: tuple[float, float, float], normal_vector: tuple[float, float, float], alpha: float) -> None:
        """ Circular arc defined by its center, normal vector and angle. Used in various methods, in conjunction with
        a start and end point.

        :param center: (x, y, z) position [m] of the arc's center point.
        :param normal_vector: (x, y, z) component [m] of the arc plane's normal vector.
        :param alpha: signed angle [rad]. Positive angle is counterclockwise, from the start point.
        """

class _InstructionList:
    def __init__(self) -> None: ...
    def add_function(self, name: str, parameters: dict) -> None: ...
    def add_property(self, name: str, value: Any) -> None: ...
    def serialize(self) -> dict: ...

class Object(ABC):
    """
    Abstract base class of all AxisVM objects. Do not use this __init__ directly.
    """
    def __init__(self, id_: int) -> None: ...
    @property
    def id(self) -> int:
        """ Object id. """

class Reference(Object, ABC, metaclass=abc.ABCMeta):
    """
    Do not use this __init__ directly, but create the object from :class:`Model`
    """
    class _Type(Enum):
        POINT: Reference._Type
        VECTOR: Reference._Type
        AXIS: Reference._Type
        PLANE: Reference._Type
        ANGLE: Reference._Type

class _ReferencePoint(Reference):
    x: Incomplete
    y: Incomplete
    z: Incomplete
    def __init__(self, id_: int, x: float, y: float, z: float) -> None: ...

class _ReferenceVector(Reference):
    point_1: Incomplete
    point_2: Incomplete
    def __init__(self, id_: int, point_1: tuple[float, float, float], point_2: tuple[float, float, float]) -> None: ...

class _ReferenceAxis(Reference):
    point_1: Incomplete
    point_2: Incomplete
    def __init__(self, id_: int, point_1: tuple[float, float, float], point_2: tuple[float, float, float]) -> None: ...

class _ReferencePlane(Reference):
    point_1: Incomplete
    point_2: Incomplete
    point_3: Incomplete
    def __init__(self, id_: int, point_1: tuple[float, float, float], point_2: tuple[float, float, float], point_3: tuple[float, float, float]) -> None: ...

class _ReferenceAngle(Reference):
    angle: Incomplete
    def __init__(self, id_: int, angle: float) -> None: ...

class _ReferenceData:
    point: Incomplete
    vector: Incomplete
    axis: Incomplete
    plane: Incomplete
    angle: Incomplete
    def __init__(self, point: _ReferencePoint = None, vector: _ReferenceVector = None, axis: _ReferenceAxis = None, plane: _ReferencePlane = None, angle: _ReferenceAngle = None) -> None: ...
    def serialize(self) -> dict: ...

class Material(Object):
    """
    Do not use this __init__ directly, but create the object from :class:`Model`
    """
    class DesignCode(Enum):
        """ National design code. """
        OTHER: Material.DesignCode
        HUNGARIAN_MSZ: Material.DesignCode
        EURO_CODE: Material.DesignCode
        ROMANIAN_STAS: Material.DesignCode
        DUTCH_NEN: Material.DesignCode
        GERMAN_DIN1045_1: Material.DesignCode
        SWISS_SIA26X: Material.DesignCode
        EURO_CODE_GER: Material.DesignCode
        ITALIAN: Material.DesignCode
        EURO_CODE_AUSTRIAN: Material.DesignCode
        EURO_CODE_UK: Material.DesignCode
        EURO_CODE_NL: Material.DesignCode
        EURO_CODE_FIN: Material.DesignCode
        EURO_CODE_RO: Material.DesignCode
        EURO_CODE_HU: Material.DesignCode
        EURO_CODE_CZ: Material.DesignCode
        EURO_CODE_B: Material.DesignCode
        EURO_CODE_PL: Material.DesignCode
        EURO_CODE_DK: Material.DesignCode
        EURO_CODE_S: Material.DesignCode
        US: Material.DesignCode
        CA_NBCC: Material.DesignCode
        CA_ONTARIO: Material.DesignCode
        CA_BRIDGE: Material.DesignCode
        EURO_CODE_SK: Material.DesignCode
    def __init__(self, id_: int, name: str) -> None: ...
    @property
    def name(self) -> str:
        """ Name of the material. """

class Node(Object):
    """
    Do not use this __init__ directly, but create the object from :class:`Model`
    """
    def __init__(self, id_: int, x: float, y: float, z: float) -> None: ...
    @property
    def x(self) -> float:
        """ X-coordinate. """
    @property
    def y(self) -> float:
        """ Y-coordinate. """
    @property
    def z(self) -> float:
        """ Z-coordinate. """

class CrossSection(Object):
    """
    Do not use this __init__ directly, but create the object from :class:`Model`
    """
    class Process(Enum):
        """ Manufacturing process. """
        OTHER: CrossSection.Process
        ROLLED: CrossSection.Process
        WELDED: CrossSection.Process
        COLD_FORMED: CrossSection.Process
    def __init__(self, id_: int, name: str) -> None: ...
    @property
    def name(self) -> str:
        """ Name of the cross-section. """

class Line(Object):
    """
    Do not use this __init__ directly, but create the object from :class:`Model`
    """
    class _GeomType(Enum):
        STRAIGHT_LINE: Line._GeomType
        CIRCLE_ARC: Line._GeomType
    def __init__(self, id_: int, interface: LineInterface, node1: Node, node2: Node) -> None: ...
    @property
    def start_node(self) -> Node:
        """ Start node of the line. """
    @property
    def end_node(self) -> Node:
        """ End node of the line. """
    def define_as_beam(self, material: Material, css_start: CrossSection, css_end: CrossSection = None, *, local_z_reference: Reference = None) -> Member:
        """ Define the line as beam with given material and cross-section.

        :param material: material of the beam.
        :param css_start: cross-section at the start node of the beam.
        :param css_end: cross-section at the start node of the beam (default: same as css_start).
        :param local_z_reference: local z-reference (must be of type vector) (default: auto).
        """
    def split_by_number(self, n: int) -> None:
        """ Split the line in 'n' equal parts.

        :param n: number of parts after the split.
        """

class Member(Object):
    """
    Do not use this __init__ directly, but create the object from :class:`Model`
    """
    class _Type(Enum):
        BEAM: Member._Type
        RIB: Member._Type
    def __init__(self, line: Line, type_: _Type) -> None: ...

class Domain(Object):
    """
    Do not use this __init__ directly, but create the object from :class:`Model`
    """
    class SurfaceType(Enum):
        """ Finite element type. """
        HOLE: Domain.SurfaceType
        MEMBRANE_STRESS: Domain.SurfaceType
        MEMBRANE_STRAIN: Domain.SurfaceType
        PLATE: Domain.SurfaceType
        SHELL: Domain.SurfaceType
    class MeshType(Enum):
        """ Contour division method. """
        ADAPTIVE: Domain.MeshType
        UNIFORM: Domain.MeshType
    class MeshGeometry(Enum):
        """ Mesh geometry type. """
        TRIANGLE: Domain.MeshGeometry
        QUAD: Domain.MeshGeometry
        MIXED: Domain.MeshGeometry
    class EccentricityType(Enum):
        """ Type of eccentricity. """
        CONSTANT: Domain.EccentricityType
        ONE_WAY: Domain.EccentricityType
        TWO_WAY: Domain.EccentricityType
        TOP_ALIGNED: Domain.EccentricityType
        BOTTOM_ALIGNED: Domain.EccentricityType
    def __init__(self, id_: int, interface: DomainInterface) -> None: ...
    def generate_mesh(self, mesh_geometry: MeshGeometry, mesh_size: float, *, mesh_type: MeshType = ..., fit_to_point_loads: float = None, fit_to_line_loads: float = None, fit_to_surface_loads: float = None, quad_mesh_quality: int = 2) -> None:
        """ Generate a mesh on the domain.

        :param mesh_geometry: mesh geometry type.
        :param mesh_size: average mesh size [m].
        :param mesh_type: contour division method (default: uniform).
        :param fit_to_point_loads: fit mesh to point loads (default: false).
        :param fit_to_line_loads: fit mesh to line loads (default: false).
        :param fit_to_surface_loads: fit mesh to surface loads (default: false)
        :param quad_mesh_quality: smoothing quality (1-6) (default: 2)
        """
    def set_eccentricity(self, eccentricity_type: EccentricityType, *, ecc_1: float = None, p1: tuple[float, float, float] = None, ecc_2: float = None, p2: tuple[float, float, float] = None, ecc_3: float = None, p3: tuple[float, float, float] = None) -> None:
        """ Set eccentricity for the domain.

        :param eccentricity_type: type of eccentricity.
        :param ecc_1: eccentricity [m] at reference point 1.
        :param p1: (x, y, z) position [m] of reference point 1.
        :param ecc_2: eccentricity [m] at reference point 2.
        :param p2: (x, y, z) position [m] of reference point 2.
        :param ecc_3: eccentricity [m] at reference point 3.
        :param p3: (x, y, z) position [m] of reference point 3.
        """

class NodeSupport(Object):
    """
    Do not use this __init__ directly, but create the object from :class:`Model`
    """

class LineSupport(Object):
    """
    Do not use this __init__ directly, but create the object from :class:`Model`
    """
    class NonLinearity(Enum):
        """ Type of non-linear behavior. """
        LINEAR: LineSupport.NonLinearity
        TENSION_ONLY: LineSupport.NonLinearity
        COMPRESSION_ONLY: LineSupport.NonLinearity

class LoadCase(Object):
    """
    Do not use this __init__ directly, but create the object from :class:`Model`
    """
    class _Type(Enum):
        STANDARD: LoadCase._Type
    def __init__(self, id_: int, name: str) -> None: ...
    @property
    def name(self) -> str:
        """ Name of the load case. """

class Load(Object):
    """
    Do not use this __init__ directly, but create the object from :class:`Model`
    """
    class DistributionType(Enum):
        GLOBAL: Load.DistributionType
        LOCAL: Load.DistributionType
        PROJECTED: Load.DistributionType
    class SurfaceDistributionType(Enum):
        SURFACE: Load.SurfaceDistributionType
        PROJECTED: Load.SurfaceDistributionType
    class System(Enum):
        GLOBAL: Load.System
        LOCAL: Load.System
        REFERENCE: Load.System
    class _LoadDistributionType(Enum):
        CONSTANT: Load._LoadDistributionType
        LINEAR: Load._LoadDistributionType
    class Axis(Enum):
        X: Load.Axis
        Y: Load.Axis
        Z: Load.Axis
        XX: Load.Axis
        YY: Load.Axis
        ZZ: Load.Axis

class LoadCombination(Object):
    """
    Do not use this __init__ directly, but create the object from :class:`Model`
    """
    class Type(Enum):
        OTHER: LoadCombination.Type
        SLS_1: LoadCombination.Type
        SLS_CHAR: LoadCombination.Type
        SLS_2: LoadCombination.Type
        SLS_FREQ: LoadCombination.Type
        SLS_3: LoadCombination.Type
        SLS_QUASI: LoadCombination.Type
        ULS_1: LoadCombination.Type
        ULS: LoadCombination.Type
        ULS_2: LoadCombination.Type
        ULS_SEISMIC: LoadCombination.Type
        ULS_3: LoadCombination.Type
        ULS_EXCEPTIONAL: LoadCombination.Type
        ULS_ALL: LoadCombination.Type
        ULS_AB: LoadCombination.Type
        ULS_A: LoadCombination.Type
        ULS_B: LoadCombination.Type
        ULS_ALL_AB: LoadCombination.Type
        ULS_A1: LoadCombination.Type
        ULS_A2: LoadCombination.Type
        ULS_A3: LoadCombination.Type
        ULS_A4: LoadCombination.Type
        ULS_A5: LoadCombination.Type
        ULS_A6: LoadCombination.Type
        ULS_A7: LoadCombination.Type
        ULS_A8: LoadCombination.Type
    def __init__(self, id_: int, name: str) -> None: ...
    @property
    def name(self) -> str:
        """ Name of the load case. """

class _Calculation(Object):
    """
    Do not use this __init__ directly, but create the object from :class:`Model`
    """
    class UserInteraction(Enum):
        USER_INTERACTION: _Calculation.UserInteraction
        AUTO_CORRECT: _Calculation.UserInteraction
        NO_AUTO_CORRECT: _Calculation.UserInteraction
        AUTO_CORRECT_NO_SHOW: _Calculation.UserInteraction
        NO_AUTO_CORRECT_NO_SHOW: _Calculation.UserInteraction

class Section(Object):
    """
    Do not use this __init__ directly, but create the object from :class:`Model`
    """
    class _Type(Enum):
        PLANE: Section._Type
        SEGMENT: Section._Type
    def __init__(self, id_: int, interface: SectionInterface, name: str) -> None: ...
    @property
    def name(self) -> str:
        """ Name of the section. """

class _Interface(ABC, metaclass=abc.ABCMeta):
    def __init__(self) -> None: ...
    @abstractmethod
    def __contains__(self, o: object) -> bool: ...
    @abstractmethod
    def __getitem__(self, i: int): ...
    @abstractmethod
    def __iter__(self): ...
    @abstractmethod
    def __len__(self) -> int: ...

class ReferenceInterface(_Interface):
    """
    Do not use this __init__ directly, but use :attr:`Model.references`
    """
    def __contains__(self, o: object) -> bool: ...
    def __getitem__(self, i: int) -> Reference: ...
    def __iter__(self) -> Iterator[Reference]: ...
    def __len__(self) -> int: ...
    def create_point(self, x: float, y: float, z: float) -> Reference:
        """ Create a reference point.

        :param x: x-position [m].
        :param y: y-position [m].
        :param z: z-position [m].
        """
    def create_vector(self, point_1: tuple[float, float, float], point_2: tuple[float, float, float]) -> Reference:
        """ Create a reference vector.

        :param point_1: (x, y, z) position [m] of the start point.
        :param point_2: (x, y, z) position [m] of the end point.
        """
    def create_axis(self, point_1: tuple[float, float, float], point_2: tuple[float, float, float]) -> Reference:
        """ Create a reference axis.

        :param point_1: (x, y, z) position [m] of the start point.
        :param point_2: (x, y, z) position [m] of the end point.
        """
    def create_plane(self, point_1: tuple[float, float, float], point_2: tuple[float, float, float], point_3: tuple[float, float, float]) -> Reference:
        """ Create a reference plane.

        :param point_1: (x, y, z) position [m] of point 1.
        :param point_2: (x, y, z) position [m] of point 2.
        :param point_3: (x, y, z) position [m] of point 3.
        """
    def create_angle(self, angle: float) -> Reference:
        """ Create a reference angle.

        :param angle: angle [rad].
        """

class MaterialInterface(_Interface):
    """
    Do not use this __init__ directly, but use :attr:`Model.materials`
    """
    def __contains__(self, o: object) -> bool: ...
    def __getitem__(self, i: int) -> Material: ...
    def __iter__(self) -> Iterator[Material]: ...
    def __len__(self) -> int: ...
    def create_concrete_eurocode(self, *, e_x: float, e_y: float = None, e_z: float = None, nu_x: float, nu_y: float = None, nu_z: float = None, alpha_x: float = 0.0, alpha_y: float = None, alpha_z: float = None, rho: float, f_ck: float, gamma_c: float, alpha_cc: float, phi_t: float = 0.0, material_code: str = None, name: str = None) -> Material:
        """ Create a concrete material according to the Eurocode.

        :param e_x: Young's modulus of elasticity [kN/m2] in local x-direction.
        :param e_y: Young's modulus of elasticity [kN/m2] in local y-direction (default = e_x).
        :param e_z: Young's modulus of elasticity [kN/m2] in local z-direction (default = e_x).
        :param nu_x: Poisson's ratio [-] in local x-direction (0 <= nu <= 0.5).
        :param nu_y: Poisson's ratio [-] in local y-direction (0 <= nu <= 0.5) (default = nu_x).
        :param nu_z: Poisson's ratio [-] in local z-direction (0 <= nu <= 0.5) (default = nu_x).
        :param alpha_x: thermal expansion coefficient [1/C] in local x-direction (default = 0.0).
        :param alpha_y: thermal expansion coefficient [1/C] in local y-direction (default = alpha_x).
        :param alpha_z: thermal expansion coefficient [1/C] in local z-direction (default = alpha_x).
        :param rho: density [kg/m3].
        :param f_ck: characteristic compressive cylinder strength [kN/m2] at 28 days.
        :param gamma_c: safety factor [-].
        :param alpha_cc: concrete strength-reduction factor for sustained loading [-].
        :param phi_t: creeping factor [-] (default = 0.0).
        :param material_code: material code name, as shown in the interface (default: auto).
        :param name: material name, as shown in the interface (default: auto).
        """
    def add_from_catalog(self, name: str, national_design_code: Material.DesignCode) -> Material:
        """ Adds a material from the catalog.

        :param name: name of the material to be added (must exist in the corresponding national design code).
        :param national_design_code: national design code in which the material with given name resides.
        """

class NodeInterface(_Interface):
    """
    Do not use this __init__ directly, but use :attr:`Model.nodes`
    """
    def __contains__(self, o: object) -> bool: ...
    def __getitem__(self, i: int) -> Node: ...
    def __iter__(self) -> Iterator[Node]: ...
    def __len__(self) -> int: ...
    def create(self, x: float, y: float, z: float) -> Node:
        """ Create a node at the given position and with given degree-of-freedom.

        :param x: x-position [m].
        :param y: y-position [m].
        :param z: z-position [m].
        """

class CrossSectionInterface(_Interface):
    """
    Do not use this __init__ directly, but use :attr:`Model.cross_sections`
    """
    def __contains__(self, o: object) -> bool: ...
    def __getitem__(self, i: int) -> CrossSection: ...
    def __iter__(self) -> Iterator[CrossSection]: ...
    def __len__(self) -> int: ...
    def create_circular(self, diameter: float, *, name: str = None) -> CrossSection:
        """ Create a circular cross-section with given diameter.

        :param diameter: diameter [m] of the cross-section.
        :param name: name of the cross-section (must be unique) (default: auto).
        """
    def create_rectangular(self, width: float, height: float, *, process: CrossSection.Process = ..., name: str = None) -> CrossSection:
        """ Create a rectangular cross-section with given width and height.

        :param width: width [m] of the cross-section.
        :param height: height [m] of the cross-section.
        :param process: process (default: other).
        :param name: name of the cross-section (must be unique) (default: auto).
        """

class LineInterface(_Interface):
    """
    Do not use this __init__ directly, but use :attr:`Model.lines`
    """
    def __contains__(self, o: object) -> bool: ...
    def __getitem__(self, i: int) -> Line: ...
    def __iter__(self) -> Iterator[Line]: ...
    def __len__(self) -> int: ...
    def __init__(self) -> None: ...
    def create(self, start_node: Node, end_node: Node, circle_arc: CircleArc = None) -> Line:
        """ Create a line between start and end node.

        :param start_node: start node.
        :param end_node: end node.
        :param circle_arc: circular arc between the nodes (default: straight line).
        """
    def define_as_beam(self, line: Line, material: Material, css_start: CrossSection, css_end: CrossSection = None, *, local_z_reference: Reference = None) -> Member:
        """ Define a line as beam with given material and cross-section.

        :param line: line to define as beam.
        :param material: material of the beam.
        :param css_start: cross-section at the start node of the beam.
        :param css_end: cross-section at the start node of the beam (default: same as css_start).
        :param local_z_reference: local z-reference (must be of type vector) (default: auto).
        """
    def split_by_number(self, line: Line, n: int) -> None:
        """ Split a line in 'n' equal parts.

        :param line: line to split.
        :param n: number of parts after the split.
        """

class DomainInterface(_Interface):
    """
    Do not use this __init__ directly, but use :attr:`Model.domains`
    """
    def __contains__(self, o: object) -> bool: ...
    def __getitem__(self, i: int) -> Domain: ...
    def __iter__(self) -> Iterator[Domain]: ...
    def __len__(self) -> int: ...
    def create(self, lines: list[Line], *, surface_type: Domain.SurfaceType, thickness: float, material: Material) -> Domain:
        """ Create a domain from given lines.

        :param lines: lines to create a domain from (lines must form a closed loop!).
        :param surface_type: finite element surface type.
        :param thickness: thickness [m] of the surface.
        :param material: material of the surface.
        """
    def generate_mesh_on_domains(self, domains: list[Domain], mesh_geometry: Domain.MeshGeometry, mesh_size: float, *, mesh_type: Domain.MeshType = ..., fit_to_point_loads: float = None, fit_to_line_loads: float = None, fit_to_surface_loads: float = None, quad_mesh_quality: int = 2) -> None:
        """ Generate a mesh on one or more domains.

        :param domains: domain(s) to generate the mesh on.
        :param mesh_geometry: mesh geometry type.
        :param mesh_size: average mesh size [m].
        :param mesh_type: contour division method (default: uniform).
        :param fit_to_point_loads: fit mesh to point loads (default: false).
        :param fit_to_line_loads: fit mesh to line loads (default: false).
        :param fit_to_surface_loads: fit mesh to surface loads (default: false)
        :param quad_mesh_quality: smoothing quality (1-6) (default: 2)
        """
    def set_eccentricity(self, domain: Domain, eccentricity_type: Domain.EccentricityType, *, ecc_1: float = None, p1: tuple[float, float, float] = None, ecc_2: float = None, p2: tuple[float, float, float] = None, ecc_3: float = None, p3: tuple[float, float, float] = None) -> None:
        """ Set eccentricity for a domain.

        :param domain: domain to set eccentricity.
        :param eccentricity_type: type of eccentricity.
        :param ecc_1: eccentricity [m] at reference point 1.
        :param p1: (x, y, z) position [m] of reference point 1.
        :param ecc_2: eccentricity [m] at reference point 2.
        :param p2: (x, y, z) position [m] of reference point 2.
        :param ecc_3: eccentricity [m] at reference point 3.
        :param p3: (x, y, z) position [m] of reference point 3.
        """

class NodeSupportInterface(_Interface):
    """
    Do not use this __init__ directly, but use :attr:`Model.node_supports`
    """
    def __contains__(self, o: object) -> bool: ...
    def __getitem__(self, i: int) -> NodeSupport: ...
    def __iter__(self) -> Iterator[NodeSupport]: ...
    def __len__(self) -> int: ...
    def __init__(self, lines: LineInterface) -> None: ...
    def create_relative_to_member(self, node: Node, *, stiffness_x: float = 0.0, stiffness_y: float = 0.0, stiffness_z: float = 0.0, stiffness_xx: float = 0.0, stiffness_yy: float = 0.0, stiffness_zz: float = 0.0, resistance_x: float = 0.0, resistance_y: float = 0.0, resistance_z: float = 0.0, resistance_xx: float = 0.0, resistance_yy: float = 0.0, resistance_zz: float = 0.0, non_linearity_x: LineSupport.NonLinearity = ..., non_linearity_y: LineSupport.NonLinearity = ..., non_linearity_z: LineSupport.NonLinearity = ..., non_linearity_xx: LineSupport.NonLinearity = ..., non_linearity_yy: LineSupport.NonLinearity = ..., non_linearity_zz: LineSupport.NonLinearity = ...) -> NodeSupport:
        """ Create a nodal support, relative to the member's local coordinate system.

        :param node: node to create the support on. Must be an end-point of a member of type beam or rib.
        :param stiffness_x: translational stiffness [kN/m] in local x-direction (default = 0.0).
        :param stiffness_y: translational stiffness [kN/m] in local y-direction (default = 0.0).
        :param stiffness_z: translational stiffness [kN/m] in local z-direction (default = 0.0).
        :param stiffness_xx: rotational stiffness [kNm/rad] around the local x-axis (default = 0.0).
        :param stiffness_yy: rotational stiffness [kNm/rad] around the local y-axis (default = 0.0).
        :param stiffness_zz: rotational stiffness [kNm/rad] around the local z-axis (default = 0.0).
        :param resistance_x: translational resistance [kN/m] in local x-direction (default = 0.0).
        :param resistance_y: translational resistance [kN/m] in local y-direction (default = 0.0).
        :param resistance_z: translational resistance [kN/m] in local z-direction (default = 0.0).
        :param resistance_xx: rotational resistance [kNm/m] around the local x-axis (default = 0.0).
        :param resistance_yy: rotational resistance [kNm/m] around the local y-axis (default = 0.0).
        :param resistance_zz: rotational resistance [kNm/m] around the local z-axis (default = 0.0).
        :param non_linearity_x: translational non-linear behaviour in local x-direction (default: linear).
        :param non_linearity_y: translational non-linear behaviour in local y-direction (default: linear).
        :param non_linearity_z: translational non-linear behaviour in local z-direction (default: linear).
        :param non_linearity_xx: rotational non-linear behaviour around the local x-axis (default: linear).
        :param non_linearity_yy: rotational non-linear behaviour around the local y-axis (default: linear).
        :param non_linearity_zz: rotational non-linear behaviour around the local z-axis (default: linear).
        """

class LineSupportInterface(_Interface):
    """
    Do not use this __init__ directly, but use :attr:`Model.line_supports`
    """
    def __contains__(self, o: object) -> bool: ...
    def __getitem__(self, i: int) -> LineSupport: ...
    def __iter__(self) -> Iterator[LineSupport]: ...
    def __len__(self) -> int: ...
    def create_on_member(self, member: Member, k_x: float, k_y: float, k_z: float, *, non_linearity_x: LineSupport.NonLinearity = ..., non_linearity_y: LineSupport.NonLinearity = ..., non_linearity_z: LineSupport.NonLinearity = ..., resistance_fx: float = 0.0, resistance_fy: float = 0.0, resistance_fz: float = 0.0) -> LineSupport:
        """ Create a line support on a member (beam), in the member's coordinate system.

        :param member: member (beam) to create the line support on.
        :param k_x: stiffness [kN/m/m] in the local x-direction.
        :param k_y: stiffness [kN/m/m] in the local y-direction.
        :param k_z: stiffness [kN/m/m] in the local z-direction.
        :param non_linearity_x: non-linear behaviour in the local x-direction (default: linear).
        :param non_linearity_y: non-linear behaviour in the local y-direction (default: linear).
        :param non_linearity_z: non-linear behaviour in the local z-direction (default: linear).
        :param resistance_fx: resistance [kN/m] in the local x-direction (default: 0.0).
        :param resistance_fy: resistance [kN/m] in the local y-direction (default: 0.0).
        :param resistance_fz: resistance [kN/m] in the local z-direction (default: 0.0).
        """

class LoadCaseInterface(_Interface):
    """
    Do not use this __init__ directly, but use :attr:`Model.load_cases`
    """
    def __contains__(self, o: object) -> bool: ...
    def __getitem__(self, i: int) -> LoadCase: ...
    def __iter__(self) -> Iterator[LoadCase]: ...
    def __len__(self) -> int: ...
    def create(self, name: str = None) -> LoadCase:
        """ Create a load case.

        :param name: name of the load case (default: auto).
        """

class LoadInterface(_Interface):
    """
    Do not use this __init__ directly, but use :attr:`Model.loads`
    """
    def __contains__(self, o: object) -> bool: ...
    def __getitem__(self, i: int) -> Load: ...
    def __iter__(self) -> Iterator[Load]: ...
    def __len__(self) -> int: ...
    def create_domain_linear(self, load_case: LoadCase, domain: Domain, load: tuple[float, float, float], *, component: Load.Axis, point_1: tuple[float, float, float], point_2: tuple[float, float, float], point_3: tuple[float, float, float], distribution_type: Load.DistributionType = ..., load_on_hole: bool = False) -> Load:
        """ Create a linear distributed load on a domain.

        :param load_case: load case to add the load to.
        :param domain: domain to create the load on.
        :param load: magnitude of the load at (point_1, point_2, point_3) [kN].
        :param component: direction of the load (X, Y, Z only).
        :param point_1: (x, y, z) position [m] of reference point 1.
        :param point_2: (x, y, z) position [m] of reference point 2.
        :param point_3: (x, y, z) position [m] of reference point 3.
        :param distribution_type: distribution type (default: GLOBAL).
        :param load_on_hole: apply load on hole (default: False -> loads disappear on holes).
        """
    def create_domain_constant(self, load_case: LoadCase, domain: Domain, load: tuple[float, float, float], *, distribution_type: Load.SurfaceDistributionType = ..., system: Load.System = ...) -> Load:
        """ Create a constant distributed load on a domain.

        :param load_case: load case to add the load to.
        :param domain: domain to create the load on.
        :param load: magnitude of the load (x, y, z) [kN].
        :param distribution_type: distribution type (default: SURFACE).
        :param system: coordinate system (default: GLOBAL).
        """
    def create_domain_self_weight(self, load_case: LoadCase, domain: Domain) -> Load:
        """ Create a self-weight load on a domain.

        :param load_case: load case to add the load to.
        :param domain: domain to create the load on.
        """
    def create_beam_self_weight(self, load_case: LoadCase, member: Member) -> Load:
        """ Create a self-weight load on a member (beam).

        :param load_case: load case to add the load to.
        :param member: member to create the load on.
        """

class LoadCombinationInterface(_Interface):
    """
    Do not use this __init__ directly, but use :attr:`Model.load_combinations`
    """
    def __contains__(self, o: object) -> bool: ...
    def __getitem__(self, i: int) -> LoadCombination: ...
    def __iter__(self) -> Iterator[LoadCombination]: ...
    def __len__(self) -> int: ...
    def create(self, combination_type: LoadCombination.Type, load_case_factors: dict[LoadCase, float], *, name: str = None) -> LoadCombination:
        """ Create a load combination from given load cases and factors.

        :param combination_type: load combination type.
        :param load_case_factors: factorized load cases {load_case: factor}.
        :param name: name of the load combination (default: auto).
        """

class SectionInterface(_Interface):
    """
    Do not use this __init__ directly, but use :attr:`Model.sections`
    """
    def __contains__(self, o: object) -> bool: ...
    def __getitem__(self, i: int) -> Section: ...
    def __iter__(self) -> Iterator[Section]: ...
    def __len__(self) -> int: ...
    def create(self, start_point: tuple[float, float, float], end_point: tuple[float, float, float], normal_vector: tuple[float, float, float], *, name: str = None) -> Section:
        """ Create a section (segment) from coordinates, to obtain results from.

        :param start_point: (x, y, z) position [m] of the section's start point.
        :param end_point: (x, y, z) position [m] of the section's end point.
        :param normal_vector: (x, y, z) components [m] of the section plane's normal vector.
        :param name: name of the section (default: auto).
        """

class ResultInterface:
    def __init__(self, nodes: NodeInterface, node_supports: NodeSupportInterface, lines: LineInterface, sections: SectionInterface) -> None: ...
    def nodal_displacements(self, nodes: list[Node] = None, *, by_load_case: bool = True) -> None:
        """ Request nodal displacements for all load cases or combinations.

        :param nodes: nodes to request the results for, or None for all nodes (default: all nodes).
        :param by_load_case: True to get result on all load cases; False to get results on all load combinations.
        """
    def nodal_support_forces(self, node_supports: list[NodeSupport] = None, *, by_load_case: bool = True) -> None:
        """ Request nodal support forces for all load cases or combinations.

        :param node_supports: node supports to request the results for, or None for all node supports (default: all
         node supports).
        :param by_load_case: True to get result on all load cases; False to get results on all load combinations.
        """
    def line_forces(self, members: list[Member] = None, *, by_load_case: bool = True) -> None:
        """ Request line forces for all load cases or combinations.

        :param members: members to request the results for, or None for all members (default: all members).
        :param by_load_case: True to get the result on all load cases; False to get results on all load combinations.
        """
    def section_surface_forces(self, sections: list[Section], cases: list[LoadCombination], chain_index: int = 1) -> None:
        """ Request section chain's surface forces for given load combinations.

        :param sections: sections to request the results for, or None for all sections (default: all sections).
        :param cases: list of load combinations to request the results for.
        :param chain_index: index of the segment chain to request the results for (default: 1).
        """
    def section_surface_stresses(self, sections: list[Section], cases: list[LoadCombination], chain_index: int = 1) -> None:
        """ Request section chain's surface stresses for given load combinations.

        :param sections: sections to request the results for, or None for all sections (default: all sections).
        :param cases: list of load combinations to request the results for.
        :param chain_index: index of the segment chain to request the results for (default: 1).
        """

class _CalculationInterface:
    instructions: Incomplete
    def __init__(self) -> None: ...
    def create_linear_analysis(self) -> None: ...

class Model:
    def __init__(self) -> None:
        """
        Can be used to construct an AxisVM model, which can be used as input of :class:`~.AxisVMAnalysis`.

        Objects are created/modified through the methods on their respective interface (see the properties below for
        all available interfaces). The following basic actions can be performed on all interfaces (example: node
        interface):

        - cast to list, indexing and slicing:

            .. code-block:: python

                nodes = list(model.nodes)  # List[Node]
                node2 = model.nodes[1]  # Node
                nodes_2_3 = model.nodes[1:3]  # List[Node]

        - iteration:

            .. code-block:: python

                for node in model.nodes:
                    print(node.id)

        - length:

            .. code-block:: python

                number_of_nodes = len(model.nodes)

        - containment check:

            .. code-block:: python

                node_in_model = node in model.nodes  # bool

        Example usage:

        .. code-block:: python

            model = Model()
            material = model.materials.add_from_catalog('C12/15', AxisVMMaterial.DesignCode.EURO_CODE)
            cross_section = model.cross_sections.create_rectangular(0.01, 0.01)
            n1 = model.nodes.create(0, 0, 0)
            n2 = model.nodes.create(1, 0, 0)
            beam = model.lines.create(n1, n2).define_as_beam(material, cross_section)
            model.node_supports.create_relative_to_member(n1, stiffness_x=1e10, stiffness_y=1e10, stiffness_z=1e10,
                                                          stiffness_xx=1e10, stiffness_yy=1e10, stiffness_zz=1e10)
            load_case = model.load_cases.create()
            model.loads.create_beam_self_weight(load_case, beam)
            model.results.nodal_displacements([n2])
        """
    @property
    def references(self) -> ReferenceInterface:
        """ Interface for creating reference points, vectors, axes, planes and angles."""
    @property
    def materials(self) -> MaterialInterface:
        """ Interface for creating materials. """
    @property
    def nodes(self) -> NodeInterface:
        """ Interface for creating nodes. """
    @property
    def cross_sections(self) -> CrossSectionInterface:
        """ Interface for creating cross-sections. """
    @property
    def lines(self) -> LineInterface:
        """ Interface for creating lines, beams, etc. """
    @property
    def domains(self) -> DomainInterface:
        """ Interface for creating domains. """
    @property
    def node_supports(self) -> NodeSupportInterface:
        """ Interface for creating node supports. """
    @property
    def line_supports(self) -> LineSupportInterface:
        """ Interface for creating line supports. """
    @property
    def load_cases(self) -> LoadCaseInterface:
        """ Interface for creating load cases. """
    @property
    def loads(self) -> LoadInterface:
        """ Interface for creating loads. """
    @property
    def load_combinations(self) -> LoadCombinationInterface:
        """ Interface for creating load combinations. """
    @property
    def sections(self) -> SectionInterface:
        """ Interface for creating sections, on which results can be obtained. """
    @property
    def results(self) -> ResultInterface:
        """ Interface for requesting results from the worker (only requested results will be returned). """
