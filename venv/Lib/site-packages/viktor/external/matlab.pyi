from . import GenericAnalysis
from ..core import File
from io import BytesIO

__all__ = ['MatlabAnalysis']

class MatlabAnalysis(GenericAnalysis):
    ''' ::version(14.17.0)

    MatlabAnalysis can be used to evaluate a matlab script on third-party infrastructure. The script is expected
    to be blocking, i.e. if the executable is invoked from command prompt, it should wait until the script is
    finished. For security purposes the executable that should be called has to be defined in the configuration file
    of the worker.

    Usage:

    .. code-block:: python

        files = [
            (\'input1.txt\', file1),
            (\'input2.txt\', file2)
        ]
        analysis = MatlabAnalysis(files=files, output_filenames=["output.txt"])
        analysis.execute(timeout=60)
        output_file = analysis.get_output_file("output.txt")

    Exceptions which can be raised during calculation:

        - :class:`viktor.errors.LicenseError`: no license available
        - :class:`viktor.errors.ExecutionError`: generic error. Error message provides more information
    '''
    def __init__(self, files: list[tuple[str, BytesIO | File]] | None = None, executable_key: str = 'matlab', output_filenames: list[str] = None) -> None:
        """
        :param files: Files that are transferred to the working directory on the server. Each file is a tuple
                      containing the content and the filename which is used to save on the infrastructure.
        :param executable_key: The key of the executable that needs to be evaluated. This key should be present in the
                               configuration file of the worker, defaults to `run_matlab`.
        :param output_filenames: A list of filenames (including extension) that are to be transferred back to the SDK.
                                 This filename is relative to the working directory.

        :raises ValueError: when no attribute is included in call.
        """
