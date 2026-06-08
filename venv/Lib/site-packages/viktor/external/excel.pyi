from ..core import File
from .external_program import ExternalProgram
from .spreadsheet import DirectInputCell, DirectOutputCell, NamedInputCell, NamedOutputCell
from _typeshed import Incomplete
from io import BytesIO
from typing import Any

__all__ = ['Excel', 'Macro']

class Macro:
    """
    Class for defining an Excel macro.
    """
    command: Incomplete
    def __init__(self, command: str) -> None:
        """
        :param command: the name of the Excel Macro command.
        """
    def serialize(self) -> dict: ...

class Excel(ExternalProgram):
    """
    Excel can be used to perform an analysis of an Excel sheet using a third-party worker. This Excel sheet may contain
    macros (i.e. .xlsm extension).

    To start an analysis call the method :meth:`~.ExternalProgram.execute`, with an appropriate timeout (in seconds).
    To retrieve the results call the method :meth:`get_named_cell_result` or :meth:`get_direct_cell_result`, after
    :meth:`~.ExternalProgram.execute`.

    Example:

    .. code-block:: python

        named_input_cells = [NamedInputCell('x', x)]
        direct_output_cells = [DirectOutputCell('Sheet1', 'B', 3)]

        excel_analysis = Excel(template, named_input_cells=named_input_cells,
            direct_output_cells=direct_output_cells, extension='.xlsx')
        excel_analysis.execute(timeout=10)
        result = excel.get_direct_cell_result('Sheet1', 'B', 3)
    """
    template: Incomplete
    def __init__(self, template: BytesIO | File, named_input_cells: list[NamedInputCell] = None, direct_input_cells: list[DirectInputCell] = None, macros: list[Macro] = None, named_output_cells: list[NamedOutputCell] = None, direct_output_cells: list[DirectOutputCell] = None, extension: str = '.xlsm', typed_results: bool = False) -> None:
        """
        :param template: Excel template to be filled, executed and returned.
        :param named_input_cells: A list of named cells containing input values.
        :param direct_input_cells: A list of direct cells containing input values.
        :param macros: A list of macros to be executed. The order of the list is preserved. This means the first macro
            in the list will be executed first, the second macro wil be executed second, etc.
        :param named_output_cells: A list of named cells of which the result after evaluation is desired.
        :param direct_output_cells: A list of direct cells of which the result after evaluation is desired.
        :param extension: Extension of the file you want to evaluate: '.xlsm' | '.xlsx'.
        :param typed_results: Cell results are of the same type as spreadsheet, if False, all values are str

        Exceptions which can be raised during calculation:
        - :class:`viktor.errors.ExecutionError`: generic error. Error message provides more information
        """
    def execute(self, timeout: int = 30) -> None:
        """
        Run method to start an external Excel analysis using a VIKTOR worker.

        .. note:: This method needs to be mocked in (automated) unit and integration tests.

        :param timeout: Timeout period in seconds.

        :raises:
            - TimeoutError when timeout has been exceeded
            - ConnectionError if no worker installed or connected
            - :class:`viktor.errors.LicenseError` if no license is available
            - :class:`viktor.errors.ExecutionError` if the external program cannot execute with the provided inputs
        """
    def result_available(self) -> bool:
        """
        :return: True if excel has returned a result. Warning! This does not necessarily have to be a successful result.
        """
    def get_named_cell_result(self, name: str) -> Any:
        '''
        Function which may be called after excel.execute().
        It can be used to fetch the result of a named cell.

        :param name: Name of the named cell of which the result is desired.
        :return: The result contained in the named cell corresponding to name.
        :rtype: Check :attr:`~.ExternalProgram.worker_version` to know which type of result is expected:

            - worker_version < 1 returns the result with type `str`.
            - worker version >= 1 returns the result with type depending on cell type:

                - cell type integer / long returns integer
                - cell type single / double / currency / decimal returns float
                - cell type string returns string
                - cell type boolean returns boolean
                - cell type date returns RFC 3339 format string (e.g. "1998-02-23T00:00:00Z")
        '''
    def get_direct_cell_result(self, sheet_name: str, column: str, row: int) -> Any:
        '''
        Function which may be called after excel.execute().
        It can be used to fetch the result of a direct cell.

        :param sheet_name: Name of the worksheet of the desired cell.
        :param column: Name of the column of the desired cell.
        :param row: Name of the row of the desired cell.
        :return: The result contained in the cell corresponding to (sheet_name, column, row).
        :rtype: Check :attr:`~.ExternalProgram.worker_version` to know which type of result is expected:

            - worker_version < 1 returns the result with type `str`.
            - worker version >= 1 returns the result with type depending on cell type:

                - cell type integer / long returns integer
                - cell type single / double / currency / decimal returns float
                - cell type string returns string
                - cell type boolean returns boolean
                - cell type date returns RFC 3339 format string (e.g. "1998-02-23T00:00:00Z")
        '''
    def get_filled_template(self) -> File:
        """ ::version(v13.5.0)

        Retrieve the filled-in template if available, otherwise raises a SpreadsheetError.
        """
    @property
    def filled_template(self) -> BytesIO:
        """A BytesIO object which contains the filled template if available, otherwise raises a SpreadsheetError."""
    @property
    def success(self) -> bool | None:
        """
        True if excel has returned a successful result, False if excel has returned an unsuccessful result,
        None otherwise.
        """
    @property
    def error_message(self) -> str | None:
        """The error string containing information from the Excel worker when available, None otherwise."""
