import abc
import os
from ..core import File
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from io import BytesIO
from typing import BinaryIO

__all__ = ['render_word_file', 'WordFileComponent', 'WordFileImage', 'WordFileResult', 'WordFileTag', 'WordFileTemplate']

class WordFileComponent(ABC, metaclass=abc.ABCMeta):
    """ Abstract base class for specific word file components, such as tags, images... """
    identifier: Incomplete
    @abstractmethod
    def __init__(self, identifier: str): ...

class WordFileTag(WordFileComponent):
    """ Add a value in a Word file template by tag. """
    value: Incomplete
    def __init__(self, identifier: str, value: object) -> None:
        """
        :param identifier: used to find the location in the template
        :param value: what needs to be placed at tag location
        """

class WordFileImage(WordFileComponent):
    """ Add an image in a Word file template. When neither width or height is provided, the original size is used.
    When only one is provided, the other is scaled. When both are provided, both are used and the original aspect ratio
    might be changed. """
    file_content: Incomplete
    width: Incomplete
    height: Incomplete
    def __init__(self, file: BinaryIO, identifier: str, width: int = None, height: int = None) -> None:
        """
        :param file: image to be placed at the tag location
        :param identifier: used to find the location in the template
        :param width: optional parameter for sizing. in Pt
        :param height: optional parameter for sizing. in Pt
        """
    @classmethod
    def from_path(cls, file_path: str | bytes | os.PathLike, identifier: str, width: int = None, height: int = None) -> WordFileImage:
        """ Create a WordFileImage from an image defined by its file path. """

class WordFileResult:
    def __init__(self, *, file_content: bytes = None) -> None: ...
    @property
    def file_content(self) -> bytes: ...

class WordFileTemplate:
    """ .. note:: Prefer to use the function :func:`~.render_word_file` instead.

    Fill wordfile template with components (e.g. text, image).

    Note that the template file should be a BytesIO object of a .docx file (not .doc).

    Example usage:

    >>> file = BytesIO(b'file')
    >>> image = BytesIO(b'image')
    >>>
    >>> tags = [
    >>>    WordFileTag('x', 1),
    >>>    WordFileTag('y', 2),
    >>>    WordFileImage(image, 'fig_tag', width=300),
    >>> ]
    >>> word_file_template = WordFileTemplate(file, tags)
    >>> result = word_file_template.render()
    >>> word_file = result.file_content

    """
    def __init__(self, file: BytesIO, components: list[WordFileComponent]) -> None:
        """
        :param file: BytesIO object of the Word template
        :param components: items that need to be inserted in the template
        """
    @classmethod
    def from_path(cls, file_path: str | bytes | os.PathLike, components: list[WordFileComponent]) -> WordFileTemplate:
        """
        :param file_path: Complete path including extension
        :param components: items that need to be inserted in the template
        """
    def render(self) -> WordFileResult:
        """ This function renders the docx template and returns the resulting file.

        .. note:: This method needs to be mocked in (automated) unit and integration tests.
        """
    @property
    def result(self) -> WordFileResult: ...

def render_word_file(template: BinaryIO, components: list[WordFileComponent]) -> File:
    """ Fill Word file with components (e.g. text, image).

    Example usage:

    .. code-block:: python

        components = [
           WordFileTag('x', 1),
           WordFileImage(image, 'fig_tag', width=300),
        ]

        template_path = Path(__file__).parent / 'my' / 'relative' / 'path' / 'template.docx'
        with open(template_path, 'rb') as template:
            word_file = render_word_file(template, components)

    .. note:: This method needs to be mocked in (automated) unit and integration tests.

    :param template: Word file template of type .docx (not .doc)
    :param components: components to fill the template with
    :return: File object containing the rendered Word file
    
    :raises: :class:`viktor.errors.WordFileError` when rendering fails
    """
