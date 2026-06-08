import abc
import datetime
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Literal, Sequence

__all__ = ['BarSurface', 'CalculationSetup', 'CheckMember', 'CheckMember1D', 'CheckSection', 'CheckSectionExtreme', 'CodeSettings', 'ConcAggregateType', 'ConcCementClass', 'ConcDependentParams', 'ConcDiagramType', 'ConcreteMaterial', 'ConcreteMemberDataEc2', 'CrossSection', 'CrossSectionComponent', 'CrossSectionParameter', 'CrossSectionType', 'EvaluationInteractionDiagram', 'ExposureClassEc2Carbonation', 'ExposureClassEc2ChemicalAttack', 'ExposureClassEc2Chlorides', 'ExposureClassEc2ChloridesFromSea', 'ExposureClassEc2FreezeAttack', 'ExposureClassesDataEc2', 'FatigueLoading', 'LoadingSLS', 'LoadingULS', 'MatConcrete', 'MatConcreteEc2', 'MatReinforcement', 'MatReinforcementEc2', 'MemberType', 'NationalAnnex', 'NoResistanceConcreteTension1d', 'ProjectData', 'ReinfClass', 'ReinfDiagramType', 'ReinfFabrication', 'ReinfType', 'ReinforcedBar', 'ReinforcedCrossSection', 'ReinforcementMaterial', 'ResultOfInternalForces', 'StandardCheckSection', 'StandardCheckSectionExtreme', 'Stirrup', 'ThermalState', 'ThermalStateType', 'TwoWaySlabType', 'TypeSLSCalculation']

class ConcreteMaterial(Enum):
    C12_15: ConcreteMaterial
    C16_20: ConcreteMaterial
    C20_25: ConcreteMaterial
    C25_30: ConcreteMaterial
    C30_37: ConcreteMaterial
    C35_45: ConcreteMaterial
    C40_50: ConcreteMaterial
    C45_55: ConcreteMaterial
    C50_60: ConcreteMaterial
    C55_67: ConcreteMaterial
    C60_75: ConcreteMaterial
    C70_85: ConcreteMaterial
    C80_95: ConcreteMaterial
    C90_105: ConcreteMaterial
    C100_115: ConcreteMaterial

class ReinforcementMaterial(Enum):
    B_400A: ReinforcementMaterial
    B_500A: ReinforcementMaterial
    B_600A: ReinforcementMaterial
    B_400B: ReinforcementMaterial
    B_500B: ReinforcementMaterial
    B_600B: ReinforcementMaterial
    B_400C: ReinforcementMaterial
    B_500C: ReinforcementMaterial
    B_600C: ReinforcementMaterial
    B_550A: ReinforcementMaterial
    B_550B: ReinforcementMaterial

class _OpenObject(ABC, metaclass=abc.ABCMeta):
    """ Abstract base class of all IDEA OpenModel objects. """
    @abstractmethod
    def __init__(self): ...

class _OpenElementId(ABC):
    def __init__(self, id_: int) -> None: ...
    @property
    def id(self) -> int: ...

class _ReferenceElement:
    def __init__(self, id_: int, type_name: str) -> None: ...
    @property
    def id(self) -> int: ...

class NationalAnnex(Enum):
    NO_ANNEX: NationalAnnex
    DUTCH: NationalAnnex
    BELGIUM: NationalAnnex

class ProjectData(_OpenObject):
    national_annex: Incomplete
    fatigue_check: Incomplete
    name: Incomplete
    number: Incomplete
    description: Incomplete
    author: Incomplete
    date: Incomplete
    design_working_life: Incomplete
    def __init__(self, *, national_annex: NationalAnnex = None, fatigue_check: bool = False, name: str = None, number: str = None, description: str = None, author: str = None, date: datetime.date = None, design_working_life: Literal[50, 75, 100] = None) -> None:
        """ Project data.

        :param name: Project name ::version(v14.6.0)
        :param number: Project number ::version(v14.6.0)
        :param description: Project description ::version(v14.6.0)
        :param author: Author ::version(v14.6.0)
        :param date: Date (default: today) ::version(v14.6.0)
        :param national_annex: national annex (default: No national annex (EN))
        :param fatigue_check: functionality - fatigue (default: false)
        :param design_working_life: Design working life (default: 50) ::version(v14.6.0)
        """

class EvaluationInteractionDiagram(Enum):
    NU_MU_MU: EvaluationInteractionDiagram
    NU_M_M: EvaluationInteractionDiagram
    N_MU_MU: EvaluationInteractionDiagram

class NoResistanceConcreteTension1d(Enum):
    EXTREME: NoResistanceConcreteTension1d
    SECTION: NoResistanceConcreteTension1d
    ALWAYS: NoResistanceConcreteTension1d

class TypeSLSCalculation(Enum):
    BOTH: TypeSLSCalculation
    SHORT_TERM: TypeSLSCalculation
    LONG_TERM: TypeSLSCalculation

class CodeSettings(_OpenObject):
    evaluation_interaction_diagram: Incomplete
    theta: Incomplete
    theta_min: Incomplete
    theta_max: Incomplete
    n_cycles_fatigue: Incomplete
    no_resistance_concrete_tension_1d: Incomplete
    type_sls_calculation: Incomplete
    def __init__(self, *, evaluation_interaction_diagram: EvaluationInteractionDiagram = None, theta: float = None, theta_min: float = None, theta_max: float = None, n_cycles_fatigue: float = None, no_resistance_concrete_tension_1d: NoResistanceConcreteTension1d = None, type_sls_calculation: TypeSLSCalculation = None) -> None:
        """ Code and calculation settings.

        :param evaluation_interaction_diagram: evaluation of interaction diagram (default: NuMuMu)
        :param theta: angle [deg] between the concrete compression strut and the beam axis perpendicular to the
                      shear force (default: set by IDEA)
        :param theta_min: minimum angle [deg] between the concrete compression strut and the beam axis perpendicular
                          to the shear force (default: set by IDEA)
        :param theta_max: maximum angle [deg] between the concrete compression strut and the beam axis perpendicular
                          to the shear force (default: set by IDEA)
        :param n_cycles_fatigue: number of fatigue cycles (* 10⁶) (default: set by IDEA)
        :param no_resistance_concrete_tension_1d: no resistance of concrete in tension - members 1D (default: Extreme)
        :param type_sls_calculation: type of SLS calculation (default: Both)
        """

class CheckMember(_OpenElementId, ABC, metaclass=abc.ABCMeta):
    """ Abstract base class of all check members. """
    @abstractmethod
    def __init__(self, id_: int): ...

class CheckMember1D(CheckMember):
    name: Incomplete
    def __init__(self, id_: int, name: str) -> None:
        """
        Do not use this __init__ directly, but create the object by :meth:`~.idea_rcs.OpenModel.create_check_member1d`.
        """

class ThermalStateType(Enum):
    NONE: ThermalStateType
    CODE: ThermalStateType
    USER: ThermalStateType

class ThermalState(_OpenObject):
    def __init__(self, expansion: ThermalStateType = ..., conductivity: ThermalStateType = ..., specific_heat: ThermalStateType = ..., stress_strain: ThermalStateType = ..., strain: ThermalStateType = ...) -> None:
        """ Collection of thermal states for expansion, conductivity, specific heat, stress-strain and strain.

        :param expansion: state of thermal expansion curvature.
        :param conductivity: state of thermal conductivity curvature.
        :param specific_heat: state of thermal specific heat curvature.
        :param stress_strain: state of thermal specific stress-strain curvature.
        :param strain: state of thermal strain curvature.
        """

class _Material(_OpenElementId, ABC, metaclass=abc.ABCMeta):
    """ Abstract base class of all materials. """
    @abstractmethod
    def __init__(self, id_: int, name: str, e_modulus: float, g_modulus: float, poisson: float, unit_mass: float, specific_heat: float, thermal_expansion: float, thermal_conductivity: float, is_default: bool, order_in_code: int, thermal_state: ThermalState): ...

class ReinfClass(Enum):
    A: ReinfClass
    B: ReinfClass
    C: ReinfClass

class ReinfType(Enum):
    BARS: ReinfType
    DECOILED_RODS: ReinfType
    WIRE_FABRICS: ReinfType
    LATTICE_GIRDERS: ReinfType

class BarSurface(Enum):
    SMOOTH: BarSurface
    RIBBED: BarSurface

class ReinfDiagramType(Enum):
    BILINEAR_INCLINED: ReinfDiagramType
    BILINEAR_NOT_INCLINED: ReinfDiagramType
    USER: ReinfDiagramType

class ReinfFabrication(Enum):
    HOT_ROLLED: ReinfFabrication
    COLD_WORKED: ReinfFabrication

class MatReinforcement(_Material, ABC, metaclass=abc.ABCMeta):
    """ Abstract base class of all material reinforcements. """
    @abstractmethod
    def __init__(self, id_: int, name: str, e_modulus: float, g_modulus: float, poisson: float, unit_mass: float, specific_heat: float, thermal_expansion: float, thermal_conductivity: float, is_default: bool, order_in_code: int, thermal_state: ThermalState, bar_surface: BarSurface): ...

class MatReinforcementEc2(MatReinforcement):
    def __init__(self, id_: int, name: str, e_modulus: float, g_modulus: float, poisson: float, unit_mass: float, specific_heat: float, thermal_expansion: float, thermal_conductivity: float, is_default: bool, order_in_code: int, thermal_state: ThermalState, bar_surface: BarSurface, fyk: float, ftk_by_fyk: float, epsuk: float, ftk: float, class_: ReinfClass, type_: ReinfType, fabrication: ReinfFabrication, diagram_type: ReinfDiagramType) -> None:
        """
        Do not use this __init__ directly, but create the object by :meth:`~.idea_rcs.OpenModel.create_matreinforcement_ec2`.
        """

class ConcDiagramType(Enum):
    BILINEAR: ConcDiagramType
    PARABOLIC: ConcDiagramType
    USER: ConcDiagramType

class ConcAggregateType(Enum):
    QUARTZITE: ConcAggregateType
    LIMESTONE: ConcAggregateType
    SANDSTONE: ConcAggregateType
    BASALT: ConcAggregateType

class ConcCementClass(Enum):
    S: ConcCementClass
    R: ConcCementClass
    N: ConcCementClass

class MatConcrete(_Material, ABC, metaclass=abc.ABCMeta):
    """ Abstract base class of all concrete materials. """
    @abstractmethod
    def __init__(self, id_: int, name: str, e_modulus: float, g_modulus: float, poisson: float, unit_mass: float, specific_heat: float, thermal_expansion: float, thermal_conductivity: float, is_default: bool, order_in_code: int, thermal_state: ThermalState): ...

class ConcDependentParams(_OpenObject):
    def __init__(self, E_cm: float, eps_c1: float, eps_c2: float, eps_c3: float, eps_cu1: float, eps_cu2: float, eps_cu3: float, F_ctm: float, F_ctk_0_05: float, F_ctk_0_95: float, n_factor: float, F_cm: float) -> None:
        """ Collection of all MatConcreteEc2 dependent parameters.

        :param E_cm: Secant modulus of elasticity of concrete [MPa]
        :param eps_c1: Compressive strain in the concrete - εc1 [-]
        :param eps_c2: Compressive strain in the concrete - εc2 [-]
        :param eps_c3: Compressive strain in the concrete - εc3 [-]
        :param eps_cu1: Ultimate compressive strain in the concrete - εcu1 [-]
        :param eps_cu2: Ultimate compressive strain in the concrete - εcu2 [-]
        :param eps_cu3: Ultimate compressive strain in the concrete - εcu3 [-]
        :param F_ctm: Mean value of axial tensile strength of concrete [MPa]
        :param F_ctk_0_05: Characteristic axial tensile strength of concrete 5% quantile [MPa]
        :param F_ctk_0_95: Characteristic axial tensile strength of concrete 95% quantile [MPa]
        :param n_factor: Coefficient n-factor - necessary parabolic part of stress-strain diagram - n [-]
        :param F_cm: Mean value of concrete cylinder compressive strength [MPa]
        """

class MatConcreteEc2(MatConcrete):
    def __init__(self, id_: int, name: str, e_modulus: float, g_modulus: float, poisson: float, unit_mass: float, specific_heat: float, thermal_expansion: float, thermal_conductivity: float, is_default: bool, order_in_code: int, thermal_state: ThermalState, fck: float, stone_diameter: float, cement_class: ConcCementClass, aggregate_type: ConcAggregateType, diagram_type: ConcDiagramType, silica_fume: bool, plain_concrete_diagram: bool, dep_params: ConcDependentParams = None) -> None:
        """
        Do not use this __init__ directly, but create the object by :meth:`~.idea_rcs.OpenModel.create_matconcrete_ec2`.
        """

class CrossSectionType(Enum):
    ONE_COMPONENT_CSS: CrossSectionType
    ROLLED_I: CrossSectionType
    ROLLED_ANGLE: CrossSectionType
    ROLLED_T: CrossSectionType
    ROLLED_U: CrossSectionType
    ROLLED_CHS: CrossSectionType
    ROLLED_RHS: CrossSectionType
    ROLLED_DOUBLE_UO: CrossSectionType
    ROLLED_DOUBLE_UC: CrossSectionType
    ROLLED_DOUBLE_LT: CrossSectionType
    ROLLED_DOUBLE_LU: CrossSectionType
    ROLLED_TI: CrossSectionType
    ROLLED_I_PAR: CrossSectionType
    ROLLED_U_PAR: CrossSectionType
    ROLLED_L_PAR: CrossSectionType
    BOX_FL: CrossSectionType
    BOX_WEB: CrossSectionType
    BOX_2I: CrossSectionType
    BOX_2U: CrossSectionType
    BOX_2U_2PI: CrossSectionType
    BOX_2L: CrossSectionType
    BOX_4L: CrossSectionType
    IW: CrossSectionType
    IWN: CrossSectionType
    TW: CrossSectionType
    O: CrossSectionType
    RECT: CrossSectionType
    IGN: CrossSectionType
    IGH: CrossSectionType
    TG: CrossSectionType
    LG: CrossSectionType
    LG_MIRRORED: CrossSectionType
    UG: CrossSectionType
    CHS_G: CrossSectionType
    ZG: CrossSectionType
    RHS_G: CrossSectionType
    OVAL: CrossSectionType
    GENERAL: CrossSectionType
    ROLLED_2I: CrossSectionType
    TRAPEZOID: CrossSectionType
    TTFH: CrossSectionType
    TWH: CrossSectionType
    TGREV: CrossSectionType
    TTFHREV: CrossSectionType
    TWHREV: CrossSectionType
    TCHAMFER_1: CrossSectionType
    TCHAMFER_2: CrossSectionType
    TT: CrossSectionType
    TT1: CrossSectionType
    SG: CrossSectionType
    GENERAL_STEEL: CrossSectionType
    GENERAL_CONCRETE: CrossSectionType
    COMPOSITE_BEAM_BOX: CrossSectionType
    COMPOSITE_BEAM_BOX_1: CrossSectionType
    COMPOSITE_BEAM_IGEN_T: CrossSectionType
    COMPOSITE_BEAM_L_LEFT: CrossSectionType
    COMPOSITE_BEAM_PLATE: CrossSectionType
    COMPOSITE_BEAM_R_RES_T: CrossSectionType
    COMPOSITE_BEAM_R_RES_T_1: CrossSectionType
    COMPOSITE_BEAM_R_T: CrossSectionType
    COMPOSITE_BEAM_SHAPE_CHAMF: CrossSectionType
    COMPOSITE_BEAM_SHAPE_CHAMF_ASYM: CrossSectionType
    COMPOSITE_BEAM_SHAPE_IGEN: CrossSectionType
    COMPOSITE_BEAM_SHAPE_I_T: CrossSectionType
    COMPOSITE_BEAM_SHAPE_I_T_ASYM: CrossSectionType
    COMPOSITE_BEAM_T_LEFT: CrossSectionType
    COMPOSITE_BEAM_TRAPEZOID: CrossSectionType
    COMPOSITE_BEAM_TRES_T: CrossSectionType
    COMPOSITE_BEAM_TREV: CrossSectionType
    COMPOSITE_BEAM_TREV_RES_I: CrossSectionType
    COMPOSITE_BEAM_TREV_RES_I_1: CrossSectionType
    COMPOSITE_BEAM_TREV_RES_R: CrossSectionType
    COMPOSITE_BEAM_TREV_RES_R_1: CrossSectionType
    COMPOSITE_BEAM_TREV_T: CrossSectionType
    COMPOSITE_BEAM_SHAPE_T_T: CrossSectionType
    BEAM_SHAPE_I_HAUNCH_CHAMFER: CrossSectionType
    BEAM_SHAPE_I_HAUNCH_CHAMFER_ASYM: CrossSectionType
    BEAM_SHAPE_REV_U: CrossSectionType
    BEAM_SHAPE_BOX: CrossSectionType
    BEAM_SHAPE_BOX_1: CrossSectionType
    BEAM_SHAPE_TREV_CHAMFER_HAUNCH_S: CrossSectionType
    BEAM_SHAPE_TREV_CHAMFER_HAUNCH_D: CrossSectionType
    BEAM_SHAPE_IREV_DEGEN: CrossSectionType
    BEAM_SHAPE_IREV_DEGEN_ADD: CrossSectionType
    BEAM_SHAPE_TREV_DEGEN: CrossSectionType
    BEAM_SHAPE_TREV_DEGEN_ADD: CrossSectionType
    BEAM_SHAPE_Z_DEGEN: CrossSectionType
    BEAM_SHAPE_I_Z_DEGEN: CrossSectionType
    BEAM_SHAPE_L_DEGEN: CrossSectionType
    CHS_PAR: CrossSectionType
    UNIQUE_NAME: CrossSectionType

class CrossSection(_OpenElementId, ABC, metaclass=abc.ABCMeta):
    """ Abstract base class of all cross-sections. """
    @abstractmethod
    def __init__(self, id_: int, name: str): ...

class CrossSectionParameter(CrossSection):
    def __init__(self, id_: int, name: str, cross_section_type: CrossSectionType, material: _ReferenceElement, **parameters: Any) -> None:
        """
        Do not use this __init__ directly, but create the object by :meth:`~.idea_rcs.OpenModel.create_cross_section_parameter`.
        """

class CrossSectionComponent(CrossSection):
    def __init__(self, id_: int, name: str) -> None:
        """
        Do not use this __init__ directly, but create the object by :meth:`~.idea_rcs.OpenModel.create_cross_section_component`.
        """
    def create_component(self, outline: Sequence[tuple[float, float]], material: MatConcrete, *, openings: Sequence[Sequence[tuple[float, float]]] = None) -> None:
        """ Create a component to build up the cross-section.

        :param outline: Vertices which define the outline of the section (y, z). A minimum of 3 vertices is required,
                        the outline is automatically closed.
        :param material: Material (created by :meth:`~.create_matconcrete_ec2`).
        :param openings: One or multiple openings, defined by vertices (y, z). A minimum of 3 vertices per opening is
                         required, the opening is automatically closed.
        """

class _CssComponent(_OpenElementId):
    def __init__(self, id_: int, material: _ReferenceElement, outline: Sequence[tuple[float, float]], openings: Sequence[Sequence[tuple[float, float]]] | None) -> None: ...

class ReinforcedBar(_OpenObject):
    def __init__(self, coordinates: tuple[float, float], diameter: float, material: _ReferenceElement) -> None:
        """
        Do not use this __init__ directly, but create the object by :meth:`ReinforcedCrossSection.create_bar`.
        """
    @property
    def coordinates(self) -> tuple[float, float]: ...
    @property
    def diameter(self) -> float: ...
    @property
    def material_id(self) -> int: ...

class Stirrup(_OpenObject):
    diameter: Incomplete
    distance: Incomplete
    def __init__(self, points: Sequence[tuple[float, float] | tuple[tuple[float, float], tuple[float, float]]], diameter: float, material: _ReferenceElement, distance: float, shear_check: bool = None, torsion_check: bool = None, mandrel_diameter_factor: float = None, anchorage_length: float = None) -> None:
        """
        Do not use this __init__ directly, but create the object by :meth:`ReinforcedCrossSection.create_stirrup`.
        """
    @property
    def points(self) -> Sequence[tuple[float, float] | tuple[tuple[float, float], tuple[float, float]]]: ...
    @property
    def material_id(self) -> int: ...
    @property
    def shear_check(self) -> bool: ...
    @property
    def torsion_check(self) -> bool: ...
    @property
    def mandrel_diameter_factor(self) -> float: ...
    @property
    def anchorage_length(self) -> float: ...

class ReinforcedCrossSection(_OpenElementId):
    def __init__(self, id_: int, name: str, cross_section: _ReferenceElement, bars: list[ReinforcedBar] = None, stirrups: list[Stirrup] = None) -> None:
        """
        Do not use this __init__ directly, but create the object by :meth:`~.idea_rcs.OpenModel.create_reinforced_cross_section`.
        """
    @property
    def bars(self) -> list[ReinforcedBar]: ...
    @property
    def stirrups(self) -> list[Stirrup]: ...
    def create_bar(self, coordinates: tuple[float, float], diameter: float, material: MatReinforcement) -> None:
        """ Create a reinforced bar on the reinforced cross-section.

        :param coordinates: (X, Y) coordinate of the bar [m].
        :param diameter: Diameter of the bar [m].
        :param material: Reinforcement material (created by :meth:`~.idea_rcs.OpenModel.create_matreinforcement_ec2`).
        """
    def create_bar_layer(self, *, origin: tuple[float, float], diameter: float, material: MatReinforcement, number_of_bars: int, delta_y: float = None, delta_z: float = None) -> None:
        """ Create multiple reinforced bars on the reinforced cross-section, positioned on a line.

        :param origin: Origin point (Y, Z) [m].
        :param diameter: Diameter of the bar [m].
        :param material: Reinforcement material (created by :meth:`~.idea_rcs.OpenModel.create_matreinforcement_ec2`).
        :param number_of_bars: Number of bars (minimum of 2).
        :param delta_y: Distance between origin bar and the last bar in y-direction [m].
        :param delta_z: Distance between origin bar and the last bar in z-direction [m].
        """
    def create_stirrup(self, points: Sequence[tuple[float, float] | tuple[tuple[float, float], tuple[float, float]]], diameter: float, material: MatReinforcement, distance: float, shear_check: bool = None, torsion_check: bool = None, mandrel_diameter_factor: float = None, anchorage_length: float = None) -> None:
        """ Create a stirrup on the reinforced cross-section.

        :param points: Sequence of (X, Y) coordinates [m] of the stirrup vertices, connected by straight line segments.
         For arc-segments use ((X_end, Y_end), (X_on_arc, Y_on_arc)).
        :param diameter: Diameter of the stirrup [m].
        :param material: Reinforcement material (created by :meth:`~.idea_rcs.OpenModel.create_matreinforcement_ec2`).
        :param distance: Longitudinal distance between stirrups [m].
        :param shear_check: Take stirrup into account in shear check (default: False).
        :param torsion_check: Take stirrup into account in torsion check (default: False).
        :param mandrel_diameter_factor: Inner diameter of mandrel as multiple of stirrup diameter [-] (default: 1.0).
        :param anchorage_length: Anchorage length [m] (default: 0.0).
        """

class ResultOfInternalForces(_OpenObject):
    def __init__(self, N: float = 0.0, Qy: float = 0.0, Qz: float = 0.0, Mx: float = 0.0, My: float = 0.0, Mz: float = 0.0) -> None:
        """ Result of internal forces at a certain location.

        :param N: Normal force (default: 0.0).
        :param Qy: Shear force in y direction (default: 0.0).
        :param Qz: Shear force in z direction (default: 0.0).
        :param Mx: Bending moment around x-axis (default: 0.0).
        :param My: Bending moment around y-axis (default: 0.0).
        :param Mz: Bending moment around z-axis (default: 0.0).
        """

class LoadingULS(_OpenObject):
    def __init__(self, internal_forces: ResultOfInternalForces, internal_forces_second_order: ResultOfInternalForces = None, internal_forces_begin: ResultOfInternalForces = None, internal_forces_end: ResultOfInternalForces = None, internal_forces_imperfection: ResultOfInternalForces = None) -> None:
        """ Loading ULS.

        :param internal_forces: Internal force in section.
        :param internal_forces_second_order: Internal forces of 2nd order effect.
        :param internal_forces_begin: Internal forces at the beginning.
        :param internal_forces_end: Internal forces at the end.
        :param internal_forces_imperfection: Internal forces of imperfection effect.
        """

class LoadingSLS(_OpenObject):
    def __init__(self, internal_forces: ResultOfInternalForces, internal_forces_imperfection: ResultOfInternalForces = None) -> None:
        """ Loading SLS.

        :param internal_forces: Internal force in section.
        :param internal_forces_imperfection: Internal forces of imperfection effect.
        """

class FatigueLoading(_OpenObject):
    def __init__(self, max_loading: LoadingULS, min_loading: LoadingULS) -> None:
        """ Fatigue loading.

        :param max_loading: Max. cyclic loading.
        :param min_loading: Min. cyclic loading.
        """

class CheckSectionExtreme(_OpenObject, metaclass=abc.ABCMeta):
    """ Abstract base class of all check section extremes. """
    description: Incomplete
    @abstractmethod
    def __init__(self, accidental: LoadingULS = None, fatigue: FatigueLoading = None, frequent: LoadingSLS = None, fundamental: LoadingULS = None, characteristic: LoadingSLS = None, quasi_permanent: LoadingSLS = None, *, description: str): ...

class StandardCheckSectionExtreme(CheckSectionExtreme):
    def __init__(self, *, accidental: LoadingULS = None, frequent: LoadingSLS = None, fundamental: LoadingULS = None, characteristic: LoadingSLS = None, quasi_permanent: LoadingSLS = None, fatigue: FatigueLoading = None, description: str) -> None:
        """
        Do not use this __init__ directly, but create the object by :meth:`CheckSection.create_extreme`.
        """

class CheckSection(_OpenElementId, ABC, metaclass=abc.ABCMeta):
    """ Abstract base class of all check sections. """
    @abstractmethod
    def __init__(self, id_: int, description: str, check_member: _ReferenceElement, reinf_section: _ReferenceElement, extremes: list[CheckSectionExtreme] = None): ...
    @property
    def extremes(self) -> list[CheckSectionExtreme]: ...
    def create_extreme(self, *, description: str = None, accidental: LoadingULS = None, fatigue: FatigueLoading = None, frequent: LoadingSLS = None, fundamental: LoadingULS = None, characteristic: LoadingSLS = None, quasi_permanent: LoadingSLS = None) -> None:
        """ Create an extreme case with corresponding internal forces on the section for checking.

        :param description: Description of the extreme (default: '{section_name} - E {i}'). ::version(v14.6.0)
        :param accidental: Accidental loading.
        :param fatigue: Fatigue loading.
        :param frequent: Frequent loading.
        :param fundamental: Fundamental loading.
        :param characteristic: Characteristic loading.
        :param quasi_permanent: Quasi-Permanent loading.
        """

class StandardCheckSection(CheckSection):
    def __init__(self, id_: int, description: str, check_member: _ReferenceElement, reinf_section: _ReferenceElement, extremes: list[CheckSectionExtreme] = None) -> None:
        """
        Do not use this __init__ directly, but create the object by :meth:`~.idea_rcs.OpenModel.add_check_section`.
        """

class MemberType(Enum):
    UNDEFINED: MemberType
    BEAM: MemberType
    COLUMN: MemberType
    BEAM_SLAB: MemberType
    HOLLOW_CORE_SLAB: MemberType
    TWO_WAY_SLAB: MemberType
    PLATE: MemberType
    WALL: MemberType

class TwoWaySlabType(Enum):
    SLAB: TwoWaySlabType
    WALL: TwoWaySlabType
    DEEP_BEAM: TwoWaySlabType
    SHELL_AS_PLATE: TwoWaySlabType
    SHELL_AS_WALL: TwoWaySlabType

class CalculationSetup(_OpenObject):
    def __init__(self, *, uls_response: bool = None, uls_diagram: bool = None, uls_shear: bool = None, uls_torsion: bool = None, uls_interaction: bool = None, sls_crack: bool = None, sls_stress_limitation: bool = None, sls_stiffnesses: bool = None, detailing: bool = None, m_n_kappa_diagram: bool = None, fatigue: bool = None, cross_section_characteristics: bool = None) -> None:
        """ Concrete calculation setup.

        :param uls_response: Response N-M(-M) (default: False).
        :param uls_diagram: Capacity N-M(-M) (default: True).
        :param uls_shear: Shear (default: True).
        :param uls_torsion: Torsion (default: True).
        :param uls_interaction: Interaction (default: True).
        :param sls_crack: Crack width (default: True).
        :param sls_stress_limitation: Stress limitation (default: True).
        :param sls_stiffnesses: Stiffnesses (default: False).
        :param detailing: Detailing (default: True).
        :param m_n_kappa_diagram: M-N-κ diagram (default: False).
        :param fatigue: Fatigue (default: True).
        :param cross_section_characteristics: Cross-section characteristics (default: IDEA-RCS default).
        """

class ConcreteMemberData(_OpenObject, ABC, metaclass=abc.ABCMeta):
    """ Abstract base class of all concrete member data. """
    @abstractmethod
    def __init__(self, element: _ReferenceElement, member_type: MemberType, two_way_slab_type: TwoWaySlabType, calculation_setup: CalculationSetup = None): ...

class ExposureClassEc2Carbonation(Enum):
    XC1: ExposureClassEc2Carbonation
    XC2: ExposureClassEc2Carbonation
    XC3: ExposureClassEc2Carbonation
    XC4: ExposureClassEc2Carbonation

class ExposureClassEc2Chlorides(Enum):
    XD1: ExposureClassEc2Chlorides
    XD2: ExposureClassEc2Chlorides
    XD3: ExposureClassEc2Chlorides

class ExposureClassEc2ChloridesFromSea(Enum):
    XS1: ExposureClassEc2ChloridesFromSea
    XS2: ExposureClassEc2ChloridesFromSea
    XS3: ExposureClassEc2ChloridesFromSea

class ExposureClassEc2FreezeAttack(Enum):
    XF1: ExposureClassEc2FreezeAttack
    XF2: ExposureClassEc2FreezeAttack
    XF3: ExposureClassEc2FreezeAttack
    XF4: ExposureClassEc2FreezeAttack

class ExposureClassEc2ChemicalAttack(Enum):
    XA1: ExposureClassEc2ChemicalAttack
    XA2: ExposureClassEc2ChemicalAttack
    XA3: ExposureClassEc2ChemicalAttack

class ExposureClassesDataEc2(_OpenObject):
    def __init__(self, *, carbonation: ExposureClassEc2Carbonation = None, chlorides: ExposureClassEc2Chlorides = None, chlorides_from_sea: ExposureClassEc2ChloridesFromSea = None, freeze_attack: ExposureClassEc2FreezeAttack = None, chemical_attack: ExposureClassEc2ChemicalAttack = None) -> None:
        """ Exposure Classes Ec2.

        :param carbonation: Carbonation (default: None).
        :param chlorides: Chlorides (default: None).
        :param chlorides_from_sea: Chlorides from sea (default: None).
        :param freeze_attack: Freeze/Thaw Attack (default: None).
        :param chemical_attack: Chemical Attack (default: None).
        """

class ConcreteMemberDataEc2(ConcreteMemberData):
    def __init__(self, element: _ReferenceElement, member_type: MemberType, two_way_slab_type: TwoWaySlabType, calculation_setup: CalculationSetup = None, coeff_kx_for_wmax: float = None, exposure_class_data: ExposureClassesDataEc2 = None, creep_coefficient: float = None, relative_humidity: float = None) -> None:
        """
        Do not use this __init__ directly, but create the object by :meth:`~.idea_rcs.OpenModel.add_member_data_ec2`.
        """
