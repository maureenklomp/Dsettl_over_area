# flake8: noqa
# type: ignore

from .__version__ import __version__

# imports required for connector
from .core import _Context, _handle_job, _get_entity_type_definition

# from .api_v1 import *  # cannot import all objects because 'Label' clashes with views.Label
from .core import *
from .errors import *
from .geometry import *
from .parametrization import *
from .result import *
from .utils import *
from .views import *


def __getattr__(attr):
    # NOTE! In case of changes to the list below, ALSO update build_src/postprocess_stubs.py!
    if attr in (
        "api_v1",
        "external",
        "geo",
        "testing",
    ):
        import importlib  # pylint: disable=import-outside-toplevel
        return importlib.import_module(f'viktor.{attr}')

    # NOTE! In case of changes to the list below, ALSO update build_src/postprocess_stubs.py!
    if attr in (
        "idea_rcs",
        "scia",
        "autodesk",
        "axisvm",
        "dfoundations",
        "dgeostability",
        "dsettlement",
        "dsheetpiling",
        "dstability",
        "dynamo",
        "etabs",
        "excel",
        # external_program,  # baseclass
        # generic,  # to avoid confusing name 'vkt.generic.GenericAnalysis'
        "grasshopper",
        "grlweap",
        "matlab",
        "plaxis",
        # python,  # to avoid confusing name 'vkt.python.PythonAnalysis'
        "revit",
        "rfem",
        "robot",
        "sap2000",
        "spreadsheet",
        "tekla",
        "word",
    ):
        import importlib  # pylint: disable=import-outside-toplevel
        return importlib.import_module(f'viktor.external.{attr}')

    raise AttributeError(f"module {__name__!r} has no attribute {attr!r}")
