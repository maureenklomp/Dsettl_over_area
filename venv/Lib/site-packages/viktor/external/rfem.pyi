import abc
from ..core import File
from .external_program import ExternalProgram
from _typeshed import Incomplete
from abc import ABC
from enum import Enum
from io import BytesIO

__all__ = ['CopyNodalLoadAction', 'EnergyOptimizationAction', 'LoadingType', 'RFEMAction', 'RFEMAnalysis', 'WriteResultsAction']

class LoadingType(Enum):
    LOAD_CASE: LoadingType
    LOAD_COMBINATION: LoadingType

class RFEMAction(ABC, metaclass=abc.ABCMeta):
    """ Abstract base class of all RFEM action objects. """
    def __init__(self, id_: int) -> None: ...

class EnergyOptimizationAction(RFEMAction):
    load_cases: Incomplete
    loading_type: Incomplete
    goal: Incomplete
    accuracy: Incomplete
    def __init__(self, load_cases: list[int], loading_type: LoadingType = ..., *, goal: float, accuracy: float) -> None:
        """ Performs an iterative analysis (consisting of a series of RFEM analyses) to solve for the magnitude of the
         1st nodal load, such that the energy at that node (approximately) equals the 'goal'. The iteration comes to a
         finish if the change in displacement at the node is lower than the specified 'accuracy'. This is done for each
         of the load cases specified.

        :param load_cases: a list of load cases/combinations to do a energy optimization calculation for. None for all
         load cases/combinations (default: None).
        :param loading_type: defines if integers in 'load_cases' must be interpreted as load case (LOAD_CASE) or load
         combination (LOAD_COMBINATION) numbers (default: LOAD_CASE)
        :param goal: energy level [Nm] for which the calculation tries to solve the 1st nodal load. Same goal is used
         for all load cases/combinations.
        :param accuracy: change in displacement [m] of the node corresponding to the 1st nodal load at which the
         iteration will successfully return. A lower accuracy in general means more iterations. Same accuracy is used
         for all load cases/combinations.
        """

class CopyNodalLoadAction(RFEMAction):
    factor: Incomplete
    copy_from_to: Incomplete
    loading_type: Incomplete
    def __init__(self, copy_from_to: list[tuple[int, int]], loading_type: LoadingType = ..., *, factor: float = 1.0) -> None:
        """ Copy the nodal load from one load case to the other, applying a factor on the magnitude.

        Note: only the 1st nodal load is copied from and to each load case/combination, other loads are ignored. Make
         sure that at least 1 such nodal load exists in both the copy-from and copy-to load cases/combinations.

        :param copy_from_to: a list of load case/combination numbers to copy (from, to)
        :param loading_type: defines if integers in 'copy_from_to' must be interpreted as load case (LOAD_CASE) or load
         combination (LOAD_COMBINATION) numbers (default: LOAD_CASE)
        :param factor: factor to be applied on the nodal load magnitude (default: 1.0)
        """

class WriteResultsAction(RFEMAction):
    load_cases: Incomplete
    loading_type: Incomplete
    def __init__(self, load_cases: list[int] = None, loading_type: LoadingType = ...) -> None:
        """ Write all nodal deformations (X, Y, Z) and member internal forces (Location, My, Mz, Fy, Fz) for the model
        in current state, for each of the load cases/combinations requested, so that it is available in
        :meth:`~.RFEMAnalysis.get_result`.

        :param load_cases: a list of load cases/combinations to write the results for. None for all
         load cases/combinations (default: None).
        :param loading_type: defines if integers in 'load_cases' must be interpreted as load case (LOAD_CASE) or load
         combination (LOAD_COMBINATION) numbers (default: LOAD_CASE)
        """

class RFEMAnalysis(ExternalProgram):
    """ RFEMAnalysis can be used to perform an analysis with RFEM on third-party infrastructure. To start an analysis
    call the method :meth:`~.ExternalProgram.execute`, with an appropriate timeout (in seconds). To retrieve the
    model call :meth:`get_model` and for results call :meth:`get_result` for the desired load combination (only
    after :meth:`~.ExternalProgram.execute`).

    Exceptions which can be raised during calculation:

        - :class:`viktor.errors.ExecutionError`: generic error. Error message provides more information

    Example usage:

    .. code-block:: python

        # SLS
        sls_cases = [1, 2, 3]
        sls_optimization = EnergyOptimizationAction(sls_cases, goal=10000, accuracy=0.1)  # goal = 10 kNm, accuracy = 10 cm

        # ALS
        als_cases = [4, 5, 6]
        als_optimization = EnergyOptimizationAction(als_cases, goal=15000, accuracy=0.1)  # goal = 15 kNm, accuracy = 10 cm

        # ULS
        uls_cases = [7, 8, 9]
        uls_creation = CopyNodalLoadAction(list(zip(sls_cases, uls_cases)), factor=1.5)  # ULS = SLS x 1.5

        # Write action
        write_result_action = WriteResultsAction(sls_cases + als_cases + uls_cases)  # or can be left empty = all cases

        actions = [sls_optimization, als_optimization, uls_creation, write_result_action]
        rfem_analysis = RFEMAnalysis(rfx_file=my_rfx_file, actions=actions)  # my_rfx_file contains the desired load cases and nodal loads
        rfem_analysis.execute(timeout=300)
        model = rfem_analysis.get_model()
        result_lc1 = rfem_analysis.get_result(1)
        result_lc2 = rfem_analysis.get_result(2)

    """
    def __init__(self, rfx_file: BytesIO | File, actions: list[RFEMAction]) -> None:
        """
        :param rfx_file: RFEM input file
        :param actions: list of actions to be performed sequentially. Possible actions are:

            - :class:`~.EnergyOptimizationAction`
            - :class:`~.CopyNodalLoadAction`
            - :class:`~.WriteResultsAction` (required for :meth:`get_result`)

        """
    def get_model(self, *, as_file: bool = False) -> BytesIO | File:
        """ Get the model that is returned after the RFEM analysis.

        :param as_file: Return as BytesIO (default) or File ::version(v13.5.0)
        """
    def get_result(self, load_case: int, *, as_file: bool = False) -> BytesIO | File:
        """ Get the nodal deformations (X, Y, Z) [m] and member internal forces (Location [m], My and Mz [Nm], Fy and
        Fz [N]) for a certain load case/combination number.

        :param load_case: number of the load case/combination to get the result for. A 'WriteResultsAction' must have
         been performed on the corresponding load case/combination to be available.
        :param as_file: Return as BytesIO (default) or File ::version(v13.5.0)
        """
