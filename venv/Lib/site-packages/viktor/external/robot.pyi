from ..core import File
from .external_program import ExternalProgram

__all__ = ['RobotAnalysis']

class RobotAnalysis(ExternalProgram):
    """
    Perform an analysis using Autodesk Robot on a third-party worker. To start an analysis call the method
    :meth:`~.ExternalProgram.execute`, with an appropriate timeout (in seconds).

    To retrieve the results call the method :meth:`get_results`, after :meth:`~.ExternalProgram.execute`. The
    evaluated model file can be retrieved by calling :meth:`get_model_file`.
    Usage:

    .. code-block:: python

        robot_analysis = RobotAnalysis(input_file, return_model=True)
        robot_analysis.execute(timeout=10)
        results = robot_analysis.get_results()
        model_file = robot_analysis.get_model_file()

    Exceptions which can be raised during calculation:

     - :class:`~viktor.errors.ExecutionError`: generic error. Error message provides more information
    """
    def __init__(self, input_file: File, *, return_model: bool = True, return_results: bool = True, requested_results: dict = None) -> None:
        '''
        :param input_file: Robot input file in STR format
        :param return_results: If True, an analysis will be run and the result file is returned.
        :param return_model: If True, the model file (.rtd) is returned.
        :param requested_results: (optional) Dictionary containing the requested results. If requested_results is None
            and return_results is True, the worker will return all results. For the allowed components see
            the Autodesk Robot SDK documentation. The dictionary should be formatted as follows:

        .. code-block:: python

            {
                "bar_forces": List[string],
                "bar_displacements": List[string],
                "bar_stresses": List[string],
                "bar_deflections": List[string],
                "node_reactions": List[string],
                "node_displacements": List[string],
            }

        '''
    def get_model_file(self) -> File | None:
        """ Retrieve the model file (only if return_model = True) in .rtd format.

        :meth:`~.ExternalProgram.execute` must be called first.
        """
    def get_results(self) -> dict | None:
        """ Retrieve the results (only if return_results = True).
        :meth:`~.ExternalAnalysis.execute` must be called first.

        The format of the returned dictionary is:

        .. code-block:: python

            {
                'bar_forces': {
                    '1': {  # case id
                        '1': {  # bar id
                            '0.000000': {   # positions
                                'FX': 26070.462297973572    # components
                            }
                        }
                    }
                },
                'bar_displacements': {
                    '1': {
                        '1': {
                            '0.000000': {
                                'RX': 0
                            }
                        }
                    }
                },
                'bar_stresses': {
                    '1': {
                        '1': {
                            '0.000000': {
                                'FXSX': 19750.350225737555
                            }
                        }
                    }
                },
                'bar_deflections': {
                    '1': {
                        '1': {
                            '0.000000': {
                                'PosUX': 0
                            }
                        }
                    }
                },
                'node_reactions': {
                    '1': {  # case id
                        '1': {  # node id
                            'FX': -9.89530235528946e-09 # components
                        }
                    }
                },
                'node_displacements': {
                    '1': {
                        '1': {
                            'RX': 0
                        }
                    }
                }
            }

        """
