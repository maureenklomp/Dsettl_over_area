from ..core import File
from .generic import GenericAnalysis
from io import BytesIO
from typing import Any, BinaryIO

__all__ = ['convert_geometry_to_glb', 'DynamoAnalysis', 'DynamoFile', 'get_dynamo_result']

class DynamoAnalysis(GenericAnalysis):
    ''' ::version(14.17.0)

    DynamoAnalysis can be used to evaluate a matlab script on third-party infrastructure. The script is expected
    to be blocking, i.e. if the executable is invoked from command prompt, it should wait until the script is
    finished. For security purposes the executable that should be called has to be defined in the configuration file
    of the worker.

    Usage:

    .. code-block:: python

        files = [
            (\'input1.txt\', file1),
            (\'input2.txt\', file2)
        ]
        analysis = DynamoAnalysis(files=files, output_filenames=["output.txt"])
        analysis.execute(timeout=60)
        output_file = analysis.get_output_file("output.txt")

    Exceptions which can be raised during calculation:

        - :class:`viktor.errors.LicenseError`: no license available
        - :class:`viktor.errors.ExecutionError`: generic error. Error message provides more information
    '''
    def __init__(self, files: list[tuple[str, BytesIO | File]] | None = None, executable_key: str = 'dynamo', output_filenames: list[str] = None) -> None:
        """
        :param files: Files that are transferred to the working directory on the server. Each file is a tuple
                      containing the content and the filename which is used to save on the infrastructure.
        :param executable_key: The key of the executable that needs to be evaluated. This key should be present in the
                               configuration file of the worker, defaults to `run_matlab`.
        :param output_filenames: A list of filenames (including extension) that are to be transferred back to the SDK.
                                 This filename is relative to the working directory.

        At least one of the attributes above should be included in the call.

        :raises ValueError: when no attribute is included in call.
        """

class DynamoFile:
    """
    Dynamo file instantiated from an existing input .dyn file. This class allows for easy transformation of input
    nodes by means of the :meth:`update` method.
    """
    def __init__(self, file: File) -> None:
        """
        :param file: Dynamo input file (.dyn).
        """
    def generate(self) -> File:
        """ Generate the (updated) Dynamo input file. """
    def update(self, name: str, value: Any) -> None:
        """ Update the value of an input node with specified name.

        :param name: Name of the input node.
        :param value: New input value.
        """
    def get_node_id(self, name: str) -> str:
        """ Retrieve the unique node id by name.

        :param name: Name of the node.
        """

def get_dynamo_result(file: BinaryIO, id_: str) -> str:
    ''' Extract results from a Dynamo output file (.xml) by means of a node \'id\', which can be obtained
    by calling :meth:`~.DynamoFile.get_node_id`.

    Example using BytesIO:

    .. code-block:: python

        input_file = DynamoFile(file)
        output_id = input_file.get_node_id("Area")  # output node called "Area"
        ...
        output_file = dynamo_analysis.get_output_file(filename=\'output.xml\')  # viktor.external.dynamo.DynamoAnalysis
        result = get_dynamo_result(output_file, id_=output_id)


    Example using :class:`~viktor.core.File`:

    .. code-block:: python

        input_file = DynamoFile(file)
        output_id = input_file.get_node_id("Area")  # output node called "Area"
        ...
        output_file = dynamo_analysis.get_output_file(filename=\'output.xml\', as_file=True)  # viktor.external.dynamo.DynamoAnalysis
        with output_file.open_binary() as f:
            result = get_dynamo_result(f, id_=output_id)

    :param file: Dynamo output file (.xml).
    :param id_: Unique identifier of the output result node.
    '''
def convert_geometry_to_glb(file: File, filter: list[str] = None) -> File:
    ''' Convert a Dynamo geometry file (.json) to a GLB file, which can directly be used in a
    :class:`~viktor.views.GeometryResult`.

    Filter specific geometric objects by id, obtained by calling :meth:`~.DynamoFile.get_node_id`:

    .. code-block:: python

        input_file = DynamoFile(file)
        sphere_id = input_file.get_node_id("Sphere")  # geometry node called "Sphere"
        ...
        geometry_file = dynamo_analysis.get_output_file(filename=\'geometry.json\', as_file=True)  # viktor.external.dynamo.DynamoAnalysis
        glb_file = convert_geometry_to_glb(geometry_file, filter=[sphere_id])

    :param file: Dynamo geometry file (.json).
    :param filter: Filter geometric objects by id (default: include all).
    '''
