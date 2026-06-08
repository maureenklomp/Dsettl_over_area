import abc
from .api_v1 import ChatConversation
from .core import File, _Result, _SerializableObject
from .views import ImageResult
from _typeshed import Incomplete
from io import BytesIO, StringIO
from munch import Munch
from typing import Any, Iterable

__all__ = ['DownloadResult', 'OptimizationResult', 'OptimizationResultElement', 'SetParamsResult', 'ChatResult']

class _ButtonResult(_Result, metaclass=abc.ABCMeta): ...

class SetParamsResult(_ButtonResult):
    ''' Container for the output of a :class:`~viktor.parametrization.SetParamsButton`.

    In order to set the content of the field `Tab 1 > Section 1 > NumberField 1` to 1234 use the format:

    .. code-block:: python

        vkt.SetParamsResult({
            "tab_1": {
                "section_1": {
                    "numberfield_1": 1234
                }
            }
        })

    To clear one or more fields one has to explicitly set the params to the empty state. Note that the empty value is
    different for each field and can be found in their docs:

    .. code-block:: python

        vkt.SetParamsResult({
            "tab_1": {
                "section_1": {
                    "numberfield_1": None,
                }
            }
        })

    '''
    def __init__(self, params: dict | Munch) -> None:
        """
        :param params: the params you want to set. If a param is not specified, the value will be kept as is.
        """
    def get(self, key: str) -> Any: ...
SetParametersResult = SetParamsResult

class DownloadResult(_ButtonResult):
    ''' Container for the output of a :class:`~viktor.parametrization.DownloadButton`.

    Download of single file:

    .. code-block:: python

        vkt.DownloadResult(file_content=my_file, file_name="my_file.txt")

    Download of multiple files bundled in a zip-file:

    .. code-block:: python

        vkt.DownloadResult(zipped_files={\'my_file_1.txt\': my_file_1, \'my_file_2.txt\': my_file_2}, file_name="my_file.zip")

    '''
    def __init__(self, file_content: str | bytes | File | StringIO | BytesIO = None, file_name: str = None, encoding: str = 'utf-8', *, zipped_files: dict[str, File | StringIO | BytesIO] = None) -> None:
        """
        :param file_content: if type str and encoding is not utf-8, specify in additional argument. Mutual exclusive
         with 'zipped_files'.
        :param file_name: name (including extension) to be used for download. In case of 'zipped_files', this is the
         name of the zip-file. May only consist of alphanumeric characters, underscores and dots (any other characters
         are converted to an underscore).
        :param encoding: optional argument to specify file encoding when file_content is provided with type str
        :param zipped_files: a dict of {file name: content} to be bundled in a zip-file with file-name 'file_name'.
         Mutual exclusive with 'file_content'.
        """

class OptimizationResultElement:
    def __init__(self, params: dict | Munch, analysis_result: dict = None) -> None:
        """
        :param params: a complete parameter set
        :param analysis_result: the accompanying results.

        For an example, see :class:`OptimizationResult`
        """
OptimisationResultElement = OptimizationResultElement

class OptimizationResult(_ButtonResult):
    result_column_names_input: Incomplete
    result_column_names_result: list
    def __init__(self, results: list[OptimizationResultElement], result_column_names_input: list[str] = None, output_headers: dict = None, image: ImageResult = None) -> None:
        """
        Container for the output of an :class:`~viktor.parametrization.OptimizationButton`.

        :param results: list of results, order is kept in user interface.
        :param result_column_names_input: specifies which input parameters should be shown the table.
                                          The parametrization class defined the label which is shown
        :param output_headers: specifies which results should be shown in the results table.
                                Key should match the key of the analysis_result inside each result.
                                Value is the corresponding label which the end user sees.
        :param image: image which is shown next to the results. Could be JPG, PNG or SVG.

        Example:

        .. code-block:: python

            params1 = {'tab': {'section': {'field1': 'a', 'field2': 5}}}
            params2 = {'tab': {'section': {'field1': 'b', 'field2': 8}}}
            analysis1 = {'result1': 10, 'result2': 20}
            analysis2 = {'result1': 100, 'result2': 150}

            results = [
                vkt.OptimizationResultElement(params1, analysis1),
                vkt.OptimizationResultElement(params2, analysis2),
            ]

            vkt.OptimizationResult(
                results, result_column_names_input=['tab.section.field1'], output_headers={'result1': 'Result 1'}
            )

        This renders as the following table for the end-user:

        +---------+---------+----------+
        |    #    | Field 1 | Result 1 |
        +=========+=========+==========+
        |    1    |    a    |    10    |
        +---------+---------+----------+
        |    2    |    b    |    100   |
        +---------+---------+----------+

        """
OptimisationResult = OptimizationResult

class ViktorResult(_SerializableObject):
    def __init__(self, optimisation_result: OptimizationResult = None, set_parameters_result: SetParamsResult = None, download_result: DownloadResult = None, *, optimization_result: OptimizationResult = None, set_params_result: SetParamsResult = None) -> None:
        """
        Standard output object of a ViktorController method, which serialises and combines several individual results
        into the standard automation output. All inputs are optional to facilitate many combinations of results where
        needed in the future. Currently, the serialisation only accounts for the following (backward compatible)
        combinations:

        - a single optimization result
        - a single set_params result
        - a single download result

        :param optimisation_result: alias for optimization_result
        :param set_parameters_result: alias for set_params_result
        :param download_result: DownloadResult object
        :param optimization_result: OptimizationResult object
        :param set_params_result: SetParamsResult object
        """

class ChatResult(_ButtonResult):
    ''' Container for the output of a :class:`~viktor.parametrization.Chat`.

    .. code-block:: python

        vkt.ChatResult(conversation=my_conversation, response="The LLM response")
    '''
    def __init__(self, conversation: ChatConversation, response: str | Iterable[str]) -> None:
        """
        :param conversation: The conversation that has to be updated.
        :param response: The response that the conversation has to be updated with.
        """
