import abc
import os
from ..core import File
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from io import BytesIO
from typing import Any, BinaryIO

__all__ = ['DirectInputCell', 'DirectOutputCell', 'InputCellRange', 'NamedInputCell', 'NamedOutputCell', 'render_spreadsheet', 'SpreadsheetCalculation', 'SpreadsheetCalculationInput', 'SpreadsheetResult', 'SpreadsheetTemplate']

class _NamedCellBaseClass(ABC, metaclass=abc.ABCMeta):
    """
    Base class for excel and spreadsheet named cells:
    cells which can be identified with their name.
    """
    name: Incomplete
    def __init__(self, name: str) -> None: ...
    @abstractmethod
    def serialize(self) -> dict: ...

class NamedInputCell(_NamedCellBaseClass):
    """
    Class for defining a named cell in which a value must be inserted.
    """
    value: Incomplete
    def __init__(self, name: str, value: bool | int | str | float) -> None:
        """

        :param name: name of the cell.
        :param value: value to be placed in the cell.
        """
    def serialize(self, convert_value_to_str: bool = False) -> dict:
        """
        :param convert_value_to_str: convert value to str. Necessary when NamedInputCell is used in
            coupled Excel program (only old workers).
        """
    def serialize_for_fill_spreadsheet(self) -> dict: ...

class SpreadsheetCalculationInput(NamedInputCell):
    """
    This class is subclassed from NamedInputCell because the same functionality is needed.
    """

class NamedOutputCell(_NamedCellBaseClass):
    """
    Class for defining named cells of which the output is desired.
    Example usage:

    .. code-block:: python

        named_cell = NamedOutputCell('my_name')
        excel = Excel(template, named_output_cells=[named_cell])
        excel.execute()
        my_desired_value = named_cell.result
    """
    def __init__(self, name: str) -> None: ...
    @property
    def result(self) -> Any:
        """
        Property that returns the result of this cell.
        May be called after Excel has been executed.

        :return: the result of this cell after excel execution
        """
    @result.setter
    def result(self, value: Any) -> None: ...
    def equals(self, named_cell_result: dict) -> bool: ...
    def serialize(self) -> dict: ...

class _DirectCellBaseClass(ABC, metaclass=abc.ABCMeta):
    """
    Base class for defining excel and spreadsheet direct cells:
    cells which can be identified by (sheet name, column, row).
    """
    sheet_name: Incomplete
    column: Incomplete
    row: Incomplete
    def __init__(self, sheet_name: str, column: str, row: int) -> None: ...
    @abstractmethod
    def serialize(self) -> dict: ...

class DirectInputCell(_DirectCellBaseClass):
    """
    Class for defining a direct cell in which a value must be inserted

    If a rectangular block of data has to be inserted, use :class:`InputCellRange` for more efficiency.
    """
    value: Incomplete
    def __init__(self, sheet_name: str, column: str, row: int, value: bool | int | str | float) -> None:
        """

        :param sheet_name: name of the sheet in which the cell is present.
        :param column: target column.
        :param row: target row.
        :param value: value to be placed in the cell.
        """
    def serialize(self, convert_value_to_str: bool = False) -> dict:
        """
        :param convert_value_to_str: convert value to str. Necessary when DirectInputCell is used in
            coupled Excel program (only old workers).
        """

class DirectOutputCell(_DirectCellBaseClass):
    """
    Class for defining a direct cell of which an output is desired.

    Example usage:

    .. code-block:: python

        direct_cell = DirectOutputCell('sheet_name', 'G', 3)
        excel = Excel(template, direct_output_cells=[direct_cell])
        excel.execute()
        my_desired_value = direct_cell.result
    """
    def __init__(self, sheet_name: str, column: str, row: int) -> None: ...
    @property
    def result(self) -> Any: ...
    @result.setter
    def result(self, value: Any) -> None: ...
    def equals(self, direct_cell_result: dict) -> bool: ...
    def serialize(self) -> dict: ...

class InputCellRange:
    """
    Convenience object to define a range of cells in row- and/or column direction.

    For single cells, use :class:`DirectInputCell`

    Example:

    .. code-block:: python

        data = [
            [1, 2, 3],
            [4, 5, 6],
            ['a', 'b', 'c'],
        ]
        cell_range = InputCellRange('Sheet1', left_column='B', top_row=3, data=data)

    This produces the following sheet:

     +---+---+---+---+---+---+
     |   | A | B | C | D | E |
     +---+---+---+---+---+---+
     | 1 |   |   |   |   |   |
     +---+---+---+---+---+---+
     | 2 |   |   |   |   |   |
     +---+---+---+---+---+---+
     | 3 |   | 1 | 2 | 3 |   |
     +---+---+---+---+---+---+
     | 4 |   | 4 | 5 | 6 |   |
     +---+---+---+---+---+---+
     | 5 |   | a | b | c |   |
     +---+---+---+---+---+---+
     | 6 |   |   |   |   |   |
     +---+---+---+---+---+---+
    """
    def __init__(self, sheet_name: str, left_column: str, top_row: int, data: list[list[float | str]]) -> None:
        """
        :param sheet_name: name of the sheet in which the data is inserted
        :param left_column: column letter of the top left target of the data
        :param top_row: row number of the top left target of the data
        :param data: content which is filled in the cell range.
                     the nested list structure should be rectangular (each list should have the same length)
                     and not empty.
        """
    def serialize(self) -> dict: ...

class SpreadsheetResult:
    """
    Wrapper around results obtained from spreadsheet services.

    .. warning:: Do not instantiate this class directly, it is created by the spreadsheet service.

    """
    def __init__(self, *, values: dict = None, file: File = None) -> None: ...
    @property
    def values(self) -> dict: ...
    @property
    def file_content(self) -> bytes: ...
    @property
    def file(self) -> File:
        """ ::version(v14.14.0) Returns a File object of the resulting filled-in spreadsheet. """
    def get_value(self, name: str) -> Any: ...

class SpreadsheetCalculation:
    """
    Using a spreadsheet for calculations, inserting inputs and reading outputs.
    This spreadsheet should not contain macros.
    See the excel module for spreadsheet calculations with macros.

    Example usage:

    .. code-block:: python

        inputs = [
           SpreadsheetCalculationInput('x', 1),
           SpreadsheetCalculationInput('y', 2),
        ]

        spreadsheet = SpreadsheetCalculation(spreadsheet, inputs)
        result = spreadsheet.evaluate(include_filled_file=False)
        values = result.values

    """
    def __init__(self, file: BytesIO | File, inputs: list[SpreadsheetCalculationInput]) -> None:
        """
        :param file: spreadsheet file
        """
    @classmethod
    def from_path(cls, file_path: str | bytes | os.PathLike, inputs: list[SpreadsheetCalculationInput]) -> SpreadsheetCalculation:
        """
        :param file_path: Complete path including extension
        :param inputs:
        """
    @property
    def file(self) -> File:
        """ ::version(v14.14.0) Returns a File object of the to-be-calculated spreadsheet. """
    def evaluate(self, include_filled_file: bool = False) -> SpreadsheetResult:
        """
        This function enters the values provided into the input tab of the sheet. The sheet evaluates the input
        and returns a  dictionary containing key value pairs of the result parameters

        .. note:: This method needs to be mocked in (automated) unit and integration tests.

        :param include_filled_file: when True, the SpreadsheetResult will contain the filled in spreadsheet.
        """
    @property
    def result(self) -> SpreadsheetResult: ...

class SpreadsheetTemplate:
    """ .. note:: Prefer to use the function :func:`~.render_spreadsheet` instead.

    Fill spreadsheet with values/text. This can be done both with direct cells (e.g. A2), or named cells.

    Example usage:

    .. code-block:: python

        cells = [
           DirectInputCell('sheet1', 'A', 1, 5),
           NamedInputCell('named_cell_1', 'text_to_be_placed'),
        ]

        template = SpreadsheetTemplate(template, cells)

        result = template.render()
        filled_template = result.file_content
    """
    def __init__(self, file: BytesIO, input_cells: list[DirectInputCell | NamedInputCell | InputCellRange]) -> None:
        """
        :param file: BytesIO object of the spreadsheet
        :param input_cells: The cells to fill the file with.
        """
    @classmethod
    def from_path(cls, file_path: str | bytes | os.PathLike, input_cells: list[DirectInputCell | NamedInputCell | InputCellRange]) -> SpreadsheetTemplate:
        """
        :param file_path: Complete path including extension
        :param input_cells: The cells to fill the file with
        """
    def render(self) -> SpreadsheetResult:
        """
        This function renders the SpreadsheetTemplate with cells. It returns a SpreadsheetResult object of the filled template.

        :return: a SpreadsheetResult object containing the filled template
        """
    @property
    def result(self) -> SpreadsheetResult: ...

def render_spreadsheet(template: BinaryIO, cells: list[DirectInputCell | NamedInputCell | InputCellRange]) -> File:
    """ Fill spreadsheet with values/text. This can be done both with direct cells (e.g. A2), or named cells.

    Example usage:

    .. code-block:: python

        cells = [
           DirectInputCell('sheet1', 'A', 1, 5),
           NamedInputCell('named_cell_1', 'text_to_be_placed'),
        ]

        template_path = Path(__file__).parent / 'my' / 'relative' / 'path' / 'template.xlsx'
        with open(template_path, 'rb') as template:
            filled_spreadsheet = render_spreadsheet(template, cells)

    :param template: spreadsheet template file
    :param cells: cells to fill the template with
    :return: File object containing the rendered spreadsheet
    """
