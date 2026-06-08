import json
from .core import File
from munch import Munch
from typing import Any, BinaryIO, Callable, Iterator

__all__ = ['convert_excel_to_pdf', 'convert_svg_to_pdf', 'convert_word_to_pdf', 'memoize', 'merge_pdf_files', 'render_jinja_template']

Serializable = bool | dict | float | int | list | None | tuple

class _CacheMiss:
    """ Object used when result is not found in the store. """

class _ParamsEncoder(json.JSONEncoder):
    """ Serialize non-serializable params. """
    def iterencode(self, o: dict | Munch, _one_shot: bool = False) -> Iterator[str]:
        """ Pass prepared params to json.JSONEncoder.iterencode(). """

class _ParamsDecoder(json.JSONDecoder):
    """ Deserialize params. """
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    @staticmethod
    def object_hook(data: dict) -> Any:
        """ Optional function that will be called with the result of any object literal decoded (a dict). """

def memoize(fun: Callable) -> Callable:
    '''
    Decorator that applies memoization to a function. This can increase performance
    when the function is called multiple times with identical input.

    When using multiple decorators, this should be the last decorator.

    .. warning:: memoized keys will differ depending on parameters being passed as args or kwargs, which can cause a
     (unexpected) cache miss! For example, f(1, y=2) and f(x=1, y=2) will be treated as two different entries.
     Prefer to use functions with kwargs only to prevent this.

    Example:

    .. code-block:: python

        # In this example, a DataView performs a long-running calculation when
        # calling `func`. When the user changes input in the editor and updates
        # the view again, `func` will only be evaluated again if either one of
        # `param_a`, `param_b`, or `param_c` is changed in-between jobs.

        import viktor as vkt

        @vkt.memoize
        def func(*, param_a, param_b, param_c):
            # perform lengthy calculation
            return result

        class Controller(vkt.Controller):
            ...

            @vkt.DataView("Results", duration_guess=30)
            def get_data_view(self, params, **kwargs):
                ...
                result = func(param_a=..., param_b=..., param_c=...)
                ...

                return vkt.DataResult(...)

    CAUTION: Only use this function when you are 100% sure of the following:

        - The function is a pure function (e.g. @staticmethod) meaning:

            - It always returns the same result for a given input. [1]_
            - It does not depend on other data and does not have side effects such
              as API calls or calls to others objects that persist state. [2]_

        - If part of the returning data contains a modified input, it must not
          be a problem that the memory reference is lost and a new object is
          returned.
        - The input of the function is serializable. [3]_
        - The output of the function is serializable. [3]_
        - During memoization, tuples in the input are casted to lists before
          determining uniqueness.
        - During memoization, tuples in the output are casted to lists before returning.
        - In the design of your application you should take into account that the
          application should not fail in timeouts/unresponsiveness if the
          memoization does not work. It should be a bonus if it works.
        - The function name is unique within the Python file.

    .. [1] Variables/objects/functions defined outside of the memoized function are
        not used in the memoized function.
    .. [2] The function should only return results. Any other actions defined in
        the function are not performed if the function call is memoized.
    .. [3] \'Serializable\' in this context means the data is any of the following types:
        boolean, dictionary, float, int, list, none, string, tuple. Types as returned in the \'params\' are also allowed
        (e.g. GeoPoint, FileResource, Color, datetime.date, etc.) with the exception of Entity. When data is nested, the
        nesting can only contain any of the aforementioned types.

    Practical uses of this are, but not limited to, function calls with input
    and output that is relatively small compared to the amount of time required
    for the evaluation. Cached results are kept for a maximum of 24 hours.

    .. note:: When using the memoization decorator on your development environment the cache is stored locally.
        The local storage is limited to 50 function calls. If the limit is exceeded, cached results are cleared based
        on a first in, first out approach. In production the storage is unlimited.

    :param fun: original function
    '''
def render_jinja_template(template: BinaryIO, variables: dict) -> File:
    ''' Render a template using Jinja.

    Example usage:

    .. code-block:: python

        with open("path/to/template.jinja", \'rb\') as template:
            result = render_jinja_template(template, {\'name\': \'John Doe\'})

    .. note:: This method needs to be mocked in (automated) unit and integration tests.

    :param template: Jinja template file.
    :param variables: set of variables to fill the template with.
    :return: File object containing the rendered template
    '''
def merge_pdf_files(*files: BinaryIO) -> File:
    '''
    This method can be used to merge several PDFs into one document. `BinaryIO` objects can be directly used as
    arguments in the method. The merged document is returned as a File object. The order of the input files is preserved
    in the resulting document.

    Example usages:

    .. code-block:: python
    
        import viktor as vkt

        # using File object
        file1 = vkt.File.from_path(Path(__file__).parent / "pdf1.pdf")
        file2 = vkt.File.from_path(Path(__file__).parent / "pdf2.pdf")
        with file1.open_binary() as f1, file2.open_binary() as f2:
            merged_pdf = merge_pdf_files(f1, f2)

        # using built-in `open()`
        with open(Path(__file__).parent / "pdf1.pdf", "rb") as f1, open(Path(__file__).parent / "pdf2.pdf", "rb") as f2:
            merged_pdf = merge_pdf_files(f1, f2)

    .. note:: This method needs to be mocked in (automated) unit and integration tests.

    :return: File object containing merged document.
    '''
def convert_word_to_pdf(file: BinaryIO) -> File:
    '''
    Convert a Word document to PDF.

    Example usages:

    .. code-block:: python

        import viktor as vkt

        # using File object
        file1 = vkt.File.from_path(Path(__file__).parent / "mydocument.docx")
        with file1.open_binary() as f1:
            pdf = convert_word_to_pdf(f1)

        # using built-in `open()`
        with open(Path(__file__).parent / "mydocument.docx", "rb") as f1:
            pdf = convert_word_to_pdf(f1)

    .. note:: This method needs to be mocked in (automated) unit and integration tests.

    :param file: Document to be converted.
    :return: File object containing converted document.
    '''
def convert_excel_to_pdf(file: BinaryIO) -> File:
    '''
    Convert an Excel document to PDF.

    Example usages:

    .. code-block:: python

        import viktor as vkt

        # using File object
        file1 = vkt.File.from_path(Path(__file__).parent / "mydocument.xlsx")
        with file1.open_binary() as f1:
            pdf = convert_excel_to_pdf(f1)

        # using built-in `open()`
        with open(Path(__file__).parent / "mydocument.xlsx", "rb") as f1:
            pdf = convert_excel_to_pdf(f1)

    .. note:: This method needs to be mocked in (automated) unit and integration tests.

    :param file: Document to be converted.
    :return: File object containing converted document.
    '''
def convert_svg_to_pdf(file: BinaryIO) -> File:
    '''
    Convert a SVG document to PDF.

    Example usages:

    .. code-block:: python

        import viktor as vkt

        # using File object
        file1 = vkt.File.from_path(Path(__file__).parent / "mydocument.svg")
        with file1.open_binary() as f1:
            pdf = convert_svg_to_pdf(f1)

        # using built-in `open()`
        with open(Path(__file__).parent / "mydocument.svg", "rb") as f1:
            pdf = convert_svg_to_pdf(f1)

    .. note:: This method needs to be mocked in (automated) unit and integration tests.

    :param file: Document to be converted.
    :return: File object containing converted document.
    '''
