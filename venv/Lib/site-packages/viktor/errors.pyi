from _typeshed import Incomplete
from typing import Any, Sequence

__all__ = ['BadRequestError', 'ComputeError', 'EntityCreateError', 'EntityDeleteError', 'EntityError', 'EntityNotFoundError', 'EntityReviseError', 'Error', 'ExecutionError', 'GEFClassificationError', 'GEFParsingError', 'InputViolation', 'InternalError', 'LicenseError', 'ModelError', 'ParsingError', 'PermissionDeniedError', 'ResourceNotFoundError', 'SciaParsingError', 'SpreadsheetError', 'SummaryError', 'UserError', 'ViewError', 'WordFileError']

class _OldExcelWorkerError(Exception):
    """ Exception to escape post-processing when old Excel workers are used. """

class _ParamNotFoundError(ValueError):
    """ Exception raised when a parameter cannot be found in the parametrization. """
    def __init__(self, key: str) -> None: ...

class Error(Exception): ...
class BadRequestError(Error):
    """ Exception raised if BE API returns 400. """
class PermissionDeniedError(Error):
    """ Exception raised if a resource is requested using the api module but access is not permitted (403) """
class ResourceNotFoundError(Error):
    """ Exception raised if a resource is requested using the api module but does not exist (404) """
class PreconditionFailedError(Error):
    """ Exception raised if some precondition failed (412) """
class EntityError(Error):
    """ Base class exception for all entity errors raised in the API. """
class EntityCreateError(EntityError):
    """ Exception raised if creation of an entity failed. """
class EntityDeleteError(EntityError):
    """ Exception raised if deletion of an entity failed. """
class EntityNotFoundError(EntityError):
    """ Exception raised if an entity is requested using the api module but does not exist. """
class EntityReviseError(EntityError):
    """ Exception raised if creating a revision (e.g. set params, rename) of an entity failed. """
class ExecutionError(Error):
    """ Exception raised if an error occurs during the execution of an external analysis. """
class GEFClassificationError(Exception):
    """ Exception raised if an error occurs during classification of :class:`viktor.geo.GEFData`. """
class GEFParsingError(Exception):
    """ Exception raised if an error occurs during parsing of a :class:`viktor.geo.GEFFile`. """
class InternalError(Error):
    """ Exception applicable for incorrect internal VIKTOR logic. Please contact VIKTOR. """
class ComputeError(Error):
    """ Exception raised if the job computation didn't finish successfully. """

class InputViolation:
    ''' ::version(v13.7.0)

    Annotate fields that should be marked as invalid in the interface, along with a message.

    Example:

    .. code-block:: python

        vkt.InputViolation("Width cannot be larger than height", fields=[\'width\', \'height\'])

    '''
    message: Incomplete
    fields: Incomplete
    def __init__(self, message: str, fields: Sequence[str]) -> None:
        """
        :param message: Message that is shown to the user.
        :param fields: Fields that are marked invalid in the interface. Note that these refer to the parametrization
          class attributes (e.g. 'step_1.field_x'), and not the database location in case `name` is set.
        """

class LicenseError(Error):
    """ Exception raised if an external analysis cannot be executed due to license issues. """
class ModelError(Error):
    """ Exception raised if an error occurs within the model of one of the bindings (e.g. SCIA, D-Settlement, ...). """
class ParsingError(Error):
    """ Exception raised if an error occurs during parsing. """
class SciaParsingError(Exception):
    """ Exception raised if an error occurs during parsing of SCIA output results. """
class SpreadsheetError(Exception):
    """ Exception raised if an error occurs in the Excel or Spreadsheet service. """
class SummaryError(Exception):
    """ Exception raised if an error occurs during the generation of the summary. """

class UserError(Exception):
    ''' ::version(v13.7.0)

    Exception that is shown to the user in the web-interface.

    Example:

    .. code-block:: python

        raise vkt.UserError("The design is not feasible")


    By providing `input_violations` you can mark specific fields as invalid:

    .. code-block:: python

        violations = [
            vkt.InputViolation("Width cannot be larger than height", fields=[\'width\', \'height\']),
            vkt.InputViolation(...),
        ]
        raise vkt.UserError("The design is not feasible", input_violations=violations)

    '''
    input_violations: Incomplete
    def __init__(self, *messages: Any, input_violations: Sequence['InputViolation'] = None) -> None:
        """
        :param messages: Messages to be shown to the user.
        :param input_violations: Mark fields invalid in the interface, along with a message.
        """

class ViewError(Exception):
    """ Exception raised if an error occurs during the generation of a view. """
class WordFileError(Exception):
    """ Exception raised if an error occurs during rendering of a Word file. """
