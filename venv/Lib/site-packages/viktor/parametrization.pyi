import abc
import datetime
from .core import Color, _OrderedClass
from .geometry import GeoPoint, GeoPolygon, GeoPolyline
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from typing import Any, Callable, Literal, Sequence

__all__ = ['ActionButton', 'And', 'AutocompleteField', 'AutodeskFileField', 'BooleanField', 'BoolOperator', 'Chat', 'ChildEntityManager', 'ChildEntityMultiSelectField', 'ChildEntityOptionField', 'ColorField', 'DateField', 'DownloadButton', 'DynamicArray', 'DynamicArrayConstraint', 'EntityMultiSelectField', 'EntityOptionField', 'FileField', 'FunctionLookup', 'GeometryMultiSelectField', 'GeometrySelectField', 'GeoPointField', 'GeoPolygonField', 'GeoPolylineField', 'HiddenField', 'Image', 'IntegerField', 'Interaction', 'IsEqual', 'IsFalse', 'IsNotEqual', 'IsNotNone', 'IsTrue', 'LineBreak', 'Lookup', 'MapSelectInteraction', 'MultiFileField', 'MultiSelectField', 'Not', 'NumberField', 'OptimizationButton', 'OptionField', 'OptionListElement', 'Or', 'OutputField', 'Page', 'Parametrization', 'ViktorParametrization', 'RowLookup', 'Section', 'SetParamsButton', 'SiblingEntityOptionField', 'SiblingEntityMultiSelectField', 'Step', 'Tab', 'Table', 'Text', 'TextAreaField', 'TextField']

class _AttrGroup:
    def __init__(self) -> None: ...
    def __getattr__(self, name: str) -> Any:
        """
        If _attrs is called, this will get the complete ordered dict.
        Else it will return the attribute within _attrs.
        """
    def __setattr__(self, name: str, value: Any) -> None:
        """
        If _attrs is created, this attribute is set on the super of this class.
        Else it will set an attribute 'name' within _attrs.
        """

class Interaction(ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def __init__(self, view: str, selection: Sequence[str] = None):
        """
        :param view: method name of the view to be interacted with.
        :param selection: only features/objects within selected interaction groups can be interacted with. Interaction
            groups can be created on the view result (e.g. :class:`MapResult`) using 'interaction_groups'. None, to
            enable interaction with all features/objects with 'identifier' assigned, ignoring interaction groups
            (default: None).
        """

class MapSelectInteraction(Interaction):
    def __init__(self, view: str, *, selection: Sequence[str] = None, min_select: int = 1, max_select: int = None) -> None:
        """ ::version(v13.2.0)

        Interaction for the selection of feature(s) in a map view.

        See :class:`Interaction` for parameters.

        Additional parameters:

        :param min_select: minimum number of features a user must select (>=1).
        :param max_select: maximum number of features a user may select. None for no limit (default: None).

        Example:

        .. code-block:: python

            button = vkt.ActionButton(..., interaction=vkt.MapSelectInteraction('my_map_view', selection=['points']))
        """

class _Field(ABC, metaclass=abc.ABCMeta):
    """ Abstract base-class of a field/button """
    def __init__(self, ui_name: str, visible: VisibleType, flex: int | None, description: str | None) -> None: ...

class _ActionButton(_Field, metaclass=abc.ABCMeta):
    """
    Base-class of a button, which invokes a certain job when pressed by the user.
    See the documentation of the subclasses for example implementations.
    """
    def __init__(self, ui_name: str, method: str, longpoll: bool, visible: VisibleType, always_available: bool, flex: int | None, description: str | None, interaction: Interaction = None) -> None:
        """
        :param ui_name: Name which is visible in the VIKTOR user interface.
        :param method: Name of the download method that is defined in the controller
        :param longpoll: Set this option to True if the process that is invoked by the action button cannot be completed
                         within the timeout limit.
        :param visible: Visibility of the button. A Constraint can be used when the visibility depends on
                        other input fields.
        :param always_available: deprecated
        :param flex: The width of the field can be altered via this argument. value between 0 and 100 (default=33).
        :param description: Show more information to the user through a tooltip on hover (max. 200 characters).
        :param interaction: Enable view interaction through this button ::version(v13.2.0)
        """

class DownloadButton(_ActionButton):
    '''
    Action button which can be pressed to download a result to a file.

    Example usage:

    .. code-block:: python

        # in parametrization:
        download_btn = vkt.DownloadButton("Download file", "get_download_result", longpoll=True)

        # in controller:
        def get_download_result(self, params, **kwargs):
            return vkt.DownloadResult(file_content=\'file_content\', file_name=\'some_file.txt\')
    '''
    def __init__(self, ui_name: str, method: str, longpoll: bool = False, *, visible: VisibleType = True, always_available: bool = False, flex: int = None, description: str = None, interaction: Interaction = None) -> None: ...

class ActionButton(_ActionButton):
    '''
    Action button which can be pressed to perform a (heavy) calculation without returning a result.

    Example usage:

    .. code-block:: python

        # in parametrization:
        calculation_btn = vkt.ActionButton("Analysis", "calculation", longpoll=True)

        # in controller:
        def calculation(self, params, **kwargs):
            # perform calculation, no return necessary
    '''
    def __init__(self, ui_name: str, method: str, longpoll: bool = True, *, visible: VisibleType = True, always_available: bool = False, flex: int = None, description: str = None, interaction: Interaction = None) -> None: ...
AnalyseButton = ActionButton

class OptimizationButton(_ActionButton):
    '''
    Action button which can be pressed to perform an optimization routine.

    Example usage:

    .. code-block:: python

        # in parametrization:
        optimize_btn = vkt.OptimizationButton("Optimization", "get_optimal_result", longpoll=True)

        # in controller:
        def get_optimal_result(self, params, **kwargs):
            # specific optimization routine
            ...
            return vkt.OptimizationResult(results)
    '''
    def __init__(self, ui_name: str, method: str, longpoll: bool = True, *, visible: VisibleType = True, always_available: bool = False, flex: int = None, description: str = None, interaction: Interaction = None) -> None: ...
OptimiseButton = OptimizationButton

class SetParamsButton(_ActionButton):
    '''
    Action button which can be pressed to perform an analysis and override current input fields.

    Example usage:

    .. code-block:: python

        # in parametrization:
        set_params_btn = vkt.SetParamsButton("Set params", "set_param_a", longpoll=True)

        # in controller:
        def set_param_a(self, params, **kwargs):
            # get updated input parameters
            ...
            return vkt.SetParamsResult(updated_parameter_set)
    '''
    def __init__(self, ui_name: str, method: str, longpoll: bool = True, *, visible: VisibleType = True, always_available: bool = False, flex: int = None, description: str = None, interaction: Interaction = None) -> None: ...

class Lookup:
    """
    Can be used to lookup the value of an input field. This can be used to set visibility of a field and to set a
    minimum and / or maximum boundary on a number field.

    Example usage on visibility:

    .. code-block:: python

        field_1 = vkt.BooleanField('Field 1')
        field_2 = vkt.NumberField('Field 2', visible=Lookup('field_1'))

    Example usage on min / max:

    .. code-block:: python

        field_1 = vkt.NumberField('Field 1')
        field_2 = vkt.NumberField('Field 2', min=Lookup('field_1'))
    """
    def __init__(self, target: str) -> None:
        """
        :param target: Name of input field.
        """

class FunctionLookup:
    """
    Defines a lookup constraint where the output value is any function of several input fields.

    Example usages:

    .. code-block:: python

        def multiply(a, b=10):
            return a * b

        field_1 = vkt.NumberField('Field 1')
        field_2 = vkt.NumberField('Field 2')

    Standard usage with two field arguments:

    .. code-block:: python

        field_3 = vkt.NumberField('Field 3', min=FunctionLookup(multiply, Lookup('field_1'), Lookup('field_2')))

    Using the default value of argument b:

    .. code-block:: python

        field_4 = vkt.NumberField('Field 4', min=FunctionLookup(multiply, Lookup('field_1')))

    Using a constant instead of a field for argument a:

    .. code-block:: python

        field_5 = vkt.NumberField('Field 5', min=FunctionLookup(multiply, 8, Lookup('field_2')))

    """
    def __init__(self, func: Callable, *func_args: Any, **kwargs: Any) -> None:
        """
        :param func: Python function or lambda expression. The function can have arguments with default values.
        :param func_args: Arguments that are provided to the function. Arguments of type Lookup / BoolOperator are
          evaluated first (e.g. to refer to the value of a Field in the editor, a Lookup can be used).
        """

class RowLookup:
    """
    Can be used to lookup the value of an input field within the same row of the dynamic array. This can be used to
    set the visibility of a field and a minimum and / or maximum boundary on a number field.

    Example usage:

    .. code-block:: python

        array = vkt.DynamicArray('Array')
        array.field_1 = vkt.NumberField('Field 1')
        array.field_2 = vkt.NumberField('Field 2', min=vkt.RowLookup('field_1'))

    For more complex constructions, it is advised to use a callback function.
    """
    def __init__(self, target: str) -> None:
        """
        :param target: Name of input field within the dynamic array.
        """

class BoolOperator(ABC, metaclass=abc.ABCMeta):
    """
    .. warning:: Do not use this class directly in an application.

    Base class for operators that can be used for field visibility and min/max.
    See the documentation of the subclasses for example implementations.
    """

class And(BoolOperator):
    """
    Can be used to evaluate multiple operands to be True.

    .. code-block:: python

        field_1 = vkt.NumberField('Field 1')
        field_2 = vkt.BooleanField('Field 2')
        field_3 = vkt.NumberField('Field 3', visible=vkt.And(vkt.IsEqual(vkt.Lookup('field_1'), 5), vkt.Lookup('field_2')))
    """
    def __init__(self, *operands: Lookup | BoolOperator | bool) -> None:
        """
        :param operands: Operands to be evaluated.
        """

class Or(BoolOperator):
    """
    Can be used to evaluate if at least one operand is True.

    .. code-block:: python

        field_1 = vkt.NumberField('Field 1')
        field_2 = vkt.BooleanField('Field 2')
        field_3 = vkt.NumberField('Field 3', visible=vkt.Or(vkt.IsEqual(vkt.Lookup('field_1'), 5), vkt.Lookup('field_2')))
    """
    def __init__(self, *operands: Lookup | BoolOperator | bool) -> None:
        """
        :param operands: Operands to be evaluated.
        """

class Not(BoolOperator):
    """
    Can be used to evaluate an operand to be False.

    .. code-block:: python

        field_1 = vkt.NumberField('Field 1')
        field_2 = vkt.NumberField('Field 2', visible=vkt.Not(vkt.IsEqual(vkt.Lookup('field_1'), 5)))

    Note, above construction is the same as:

    .. code-block:: python

        field_1 = vkt.NumberField('Field 1')
        field_2 = vkt.NumberField('Field 2', visible=vkt.IsNotEqual(vkt.Lookup('field_1'), 5))
    """
    def __init__(self, operand: Lookup | BoolOperator | bool) -> None:
        """
        :param operand: Operand to be evaluated.
        """

class IsEqual(BoolOperator):
    """
    Can be used to evaluate two operands to be equal.

    .. code-block:: python

        field_1 = vkt.NumberField('Field 1')
        field_2 = vkt.NumberField('Field 2', visible=vkt.IsEqual(vkt.Lookup('field_1'), 5))
    """
    def __init__(self, operand1: Lookup | BoolOperator | Any, operand2: Lookup | BoolOperator | Any) -> None:
        """
        :param operand1: First operand to be evaluated.
        :param operand2: Second operand to be evaluated.
        """

class IsNotEqual(IsEqual):
    """
    Can be used to evaluate two operands to be NOT equal.

    .. code-block:: python

        field_1 = vkt.NumberField('Field 1')
        field_2 = vkt.NumberField('Field 2', visible=vkt.IsNotEqual(vkt.Lookup('field_1'), 5))
    """

class IsTrue(IsEqual):
    """
    Can be used to evaluate an operand to be True.

    .. code-block:: python

        field_1 = vkt.NumberField('Field 1')
        field_2 = vkt.NumberField('Field 2', visible=vkt.IsTrue(vkt.Lookup('field_1')))
    """
    def __init__(self, operand: Lookup | BoolOperator | Any) -> None:
        """
        :param operand: Operand to be evaluated.
        """

class IsFalse(IsEqual):
    """
    Can be used to evaluate an operand to be False.

    .. code-block:: python

        field_1 = vkt.NumberField('Field 1')
        field_2 = vkt.NumberField('Field 2', visible=vkt.IsFalse(vkt.Lookup('field_1')))
    """
    def __init__(self, operand: Lookup | BoolOperator | Any) -> None:
        """
        :param operand: Operand to be evaluated.
        """

class IsNotNone(IsNotEqual):
    """
    Can be used to evaluate an operand to be NOT None.

    .. code-block:: python

        field_1 = vkt.NumberField('Field 1')
        field_2 = vkt.NumberField('Field 2', visible=vkt.IsNotNone(vkt.Lookup('field_1')))
    """
    def __init__(self, operand: Lookup | BoolOperator | Any) -> None:
        """
        :param operand: Operand to be evaluated.
        """

class DynamicArrayConstraint:
    """
    This constraint facilitates usage of other constraints within a dynamic array row.

    .. warning:: The DynamicArrayConstraint can currently only be used for the **visibility** of DynamicArray
       components.

    Example usage:

    .. code-block:: python

        _show_y = vkt.DynamicArrayConstraint('array_name', vkt.IsTrue(vkt.Lookup('$row.param_x')))

        array = vkt.DynamicArray('My array')
        array.param_x = vkt.BooleanField('X')
        array.param_y = vkt.NumberField('Y', visible=_show_y)
    """
    def __init__(self, dynamic_array_name: str, operand: Lookup | BoolOperator | FunctionLookup) -> None:
        """
        :param dynamic_array_name: name of the dynamic array on which the constraint should be applied.
        :param operand: The inputs of the operand have to be altered to access the correct row within the dynamic array.
            The input for a target field becomes '$row.{field_name}'.
        """

class DynamicArray(_AttrGroup):
    '''Dynamic array input field with row definitions.

    .. warning::
        **Nesting Restrictions:**

        - Cannot nest :class:`DynamicArray` within :class:`DynamicArray`
        - Cannot nest :class:`DynamicArray` within :class:`Table`

        **Unsupported Field Types:**

        The following field types cannot be added to a dynamic array:

        - :class:`ActionButton`
        - :class:`ChildEntityManager`
        - :class:`DownloadButton`
        - :class:`HiddenField`
        - :class:`Image`
        - :class:`OptimizationButton`
        - :class:`SetParamsButton`
        - :class:`Text`

    Example usage:

    .. code-block:: python

        # Define dynamic array structure
        layers = vkt.DynamicArray("Layers")
        layers.depth = vkt.NumberField("Depth", suffix=\'m\')
        layers.material = vkt.TextField("Material")

    A dynamic array can also be created with default content. Assume the fields as defined above:

    .. code-block:: python

        _default_content = [
            {\'depth\': 2.5, \'material\': \'Sand\'},
            {\'depth\': 5.0, \'material\': \'Clay\'},
            {\'depth\': 3.2, \'material\': \'Gravel\'},
        ]

        layers = vkt.DynamicArray("Layers", default=_default_content)
        ...
    '''
    def __init__(self, ui_name: str, min: int | Lookup | FunctionLookup | Callable = None, max: int | Lookup | FunctionLookup | Callable = None, copylast: bool = None, visible: bool | BoolOperator | Lookup | FunctionLookup | Callable = True, default: list[dict] = None, *, name: str = None, description: str = None, row_label: str = None) -> None:
        """
        :param ui_name: This string is visible in the VIKTOR user interface.
        :param min: Minimum number of rows in the array.
        :param max: Maximum number of rows in the array.
        :param copylast: Copy the last row when clicking the + button. Takes precedence over field defaults.
        :param visible: Can be used when the visibility depends on other input fields.
        :param default: Default values of complete array. Filled before user interaction.
        :param name: The position of the parameter in the database can be specified in this argument. ::version(v14.18.0)
        :param description: Show more information to the user through a tooltip on hover (max. 200 characters).
        :param row_label: Label to be shown at each row. The row number is appended to the label (max. 30 characters).

        The default values of the DynamicArray are filled when the editor is entered for the first time
        (just like the other fields). The fields underneath the dynamic array can also have default values.
        These are filled when the user adds a new row. If copylast is `True`, the last values are copied,
        and the Field defaults are ignored.

        .. code-block:: python

            array = vkt.DynamicArray('Dyn Array', default=[{'a': 1, 'b': 'hello'}, {'a': 2, 'b': 'there'}])
            array.a = vkt.NumberField('A', default=99)
            array.b = vkt.TextField('B', default='foo')

        When first entering the editor:

        +---+-------+
        | A | B     |
        +===+=======+
        | 1 | hello |
        +---+-------+
        | 2 | there |
        +---+-------+

        When adding a new row:

        +----+-------+
        | A  | B     |
        +====+=======+
        | 1  | hello |
        +----+-------+
        | 2  | there |
        +----+-------+
        | 99 | foo   |
        +----+-------+

        When using `copylast`:

        .. code-block:: python

            array = vkt.DynamicArray('Dyn Array', copylast=True, default=[{'a': 1, 'b': 'hello'}])
            array.a = vkt.NumberField('A', default=99)
            array.b = vkt.TextField('B', default='foo')

        When first entering the editor:

        +---+-------+
        | A | B     |
        +===+=======+
        | 1 | hello |
        +---+-------+

        When adding a new row:

        +----+-------+
        | A  | B     |
        +====+=======+
        | 1  | hello |
        +----+-------+
        | 1  | hello |
        +----+-------+

        Data:

        - list of dictionaries: e.g. `[{'a': 1, 'b': '1'}, {'a': 2, 'b': '2'}]`
        - empty list if there are no 'rows'
        - when fields are empty, the corresponding empty values are used (see documentation of specific field)

        """

class Field(_Field, metaclass=abc.ABCMeta):
    def __init__(self, *, ui_name: str, name: str = None, prefix: str = None, suffix: str = None, default: Any = None, flex: int = None, visible: VisibleType = True, description: str = None) -> None:
        """
        :param ui_name: This string is visible in the VIKTOR user interface.
        :param name: The position of the parameter in the database can be specified in this argument.

                     .. warning::
                         **Reserved Names:** The following names are reserved and cannot be used:

                         - ``'name'`` (reserved for internal use)
                         - ``'filename'`` (reserved for file handling)

                     Using a reserved name will cause an error. Choose a different name for your field.

        :param prefix: A prefix will be put in front of the ui_name to provide info such as a dollar sign. Note that
                       this function does not yet work for input fields.
        :param suffix: A suffix will be put behind the ui_name to provide additional information such as units.
        :param default: The value or string that is specified here is filled in as a default input.
        :param flex: The width of the field can be altered via this argument. value between 0 and 100 (default=33).
        :param visible: Can be used when the visibility depends on other input fields.
        :param description: Show more information to the user through a tooltip on hover (max. 200 characters).
        """

class ColorField(Field):
    def __init__(self, ui_name: str, name: str = None, *, default: Color = None, flex: int = None, visible: VisibleType = True, description: str = None) -> None:
        """ ::version(v14.0.0)

        See :class:`Field` for parameters.

        Additional params: -

        Data:

            - :class:`~.viktor.core.Color`
            - None when empty
        """

class DateField(Field):
    def __init__(self, ui_name: str, name: str = None, *, default: datetime.date = None, flex: int = None, visible: VisibleType = True, description: str = None) -> None:
        """
        See :class:`Field` for parameters.

        Additional params: -

        Data:

        - datetime.date object
        - None, when empty
        """

class NumberField(Field):
    def __init__(self, ui_name: str, name: str = None, prefix: str = None, *, suffix: str = None, default: float = None, step: float = None, min: MinMaxType = None, max: MinMaxType = None, num_decimals: int = None, visible: VisibleType = True, flex: int = None, variant: str = 'standard', description: str = None) -> None:
        """
        See :class:`Field` for parameters.

        Additional parameters:

        :param step: Stepping interval when clicking up and down spinner buttons
        :param min: Specifies a minimum value constraint.
        :param max: Specifies a maximum value constraint.
        :param num_decimals: Specifies the number of decimals.
        :param variant: Visually alter the input field. Possible options:

            - 'standard': default

            .. figure:: ../_static/variant_NumberField_standard.png
                :width: 200px

            - 'slider': slider (ignored in Table)

            .. figure:: ../_static/variant_NumberField_slider.png
                :width: 200px

        Data:

        - integer or float
        - None, when empty
        """

class IntegerField(NumberField):
    def __init__(self, ui_name: str, name: str = None, prefix: str = None, *, suffix: str = None, default: int = None, step: int = None, min: MinMaxType = None, max: MinMaxType = None, visible: VisibleType = True, flex: int = None, description: str = None) -> None:
        """
        See :class:`NumberField` for parameters

        Additional parameters: -

        Data:

        - integer, when filled
        - None, when empty
        """

class TextField(Field):
    def __init__(self, ui_name: str, name: str = None, prefix: str = None, *, suffix: str = None, default: str = None, visible: VisibleType = True, flex: int = None, description: str = None) -> None:
        """
        See :class:`Field` for parameters.

        Additional parameters: -

        Data:

        - string
        - empty string, when empty
        """

class OutputField:
    def __init__(self, ui_name: str, *, value: ValueType = None, prefix: str = None, suffix: str = None, visible: VisibleType = True, flex: int = None, description: str = None) -> None:
        '''
        See :class:`Field` for parameters.

        Additional parameters:

        :param value: Value to be presented in the interface (can be hard-coded or calculated).

        Example: Point to another parameter

        .. code-block:: python

            field_1 = vkt.NumberField()
            field_2 = vkt.OutputField(ui_name, value=vkt.Lookup("field_1"))

        Example: Compute output value using callback function

        .. code-block:: python

            def get_value(params, entity_id, **kwargs):
                # app specific logic
                value = ...
                return value

            field = vkt.OutputField(ui_name, value=get_value)

        Data:

        - OutputFields are not present in the params
        '''

class LineBreak:
    def __init__(self) -> None:
        """
        Linebreaks can be used to force input fields to be placed in the next row to obtain a cleaner looking editor.

        Example usage:

        .. code-block:: python

            field_1 = vkt.NumberField()
            new_line = vkt.LineBreak()
            field_2 = vkt.NumberField()

        """

class BooleanField(Field):
    def __init__(self, ui_name: str, name: str = None, *, default: bool = None, visible: VisibleType = True, flex: int = None, always_available: bool = False, description: str = None) -> None:
        """
        See :class:`Field` for parameters

        Additional parameters:

        :param always_available: deprecated

        Data:

        - False or True
        """
ToggleButton = BooleanField

class _SelectField(Field, ABC, metaclass=abc.ABCMeta):
    """ Base-class for fields with distinct choices. """
    def __init__(self, *, ui_name: str, name: str | None, prefix: str | None, suffix: str | None, options: list[float | str | OptionListElement] | Callable, default: list[float | str] | float | str | None, flex: int | None, visible: VisibleType, multiple: bool = True, description: str = None) -> None: ...

class OptionField(_SelectField):
    """ Present dropdown list with options for user. If there is only one option, this option is automatically selected.

    If you want to enable multiple options to be select, use a `MultiSelectField`.

    Example usage:

    .. code-block:: python

        field = vkt.OptionField('Available options', options=['Option 1', 'Option 2'], default='Option 1')

    Or use an OptionListElement to obtain a value in the params which differs from the interface name:

    .. code-block:: python

        _options = [vkt.OptionListElement('option_1', 'Option 1'), vkt.OptionListElement('option_2', 'Option 2')]
        field = vkt.OptionField('Available options', options=_options, default='option_1')

    """
    def __init__(self, ui_name: str, options: list[float | str | OptionListElement] | Callable, name: str = None, prefix: str = None, suffix: str = None, default: float | str = None, visible: VisibleType = True, flex: int = None, *, description: str = None, variant: str = 'standard', autoselect_single_option: bool = False) -> None:
        """
        See :class:`Field` for parameters.

        Additional parameters:

        :param options: Options should be defined as a list of numbers, strings, or OptionListElement objects.
        :param variant: Visually alter the input field. Possible options:

            - 'standard': default

            .. figure:: ../_static/variant_OptionField_standard.png

            - 'radio': radio buttons, vertically positioned (ignored in Table)

            .. figure:: ../_static/variant_OptionField_radio.png

            - 'radio-inline': radio buttons, horizontally positioned (ignored in Table)

            .. figure:: ../_static/variant_OptionField_radio-inline.png

        :param autoselect_single_option: True to always automatically select when a single option is provided.
                                         This holds for static options as well as dynamic options (see examples below).

        When `autoselect_single_option=False` (default), expect the following behavior:

        +-------------------------------------------------------------------------------+-----------------------------------------+
        | Action                                                                        | Options                                 |
        +===============================================================================+=========================================+
        | enter the editor                                                              | ⚪ A, ⚪ B, ⚪ C                        |
        +-------------------------------------------------------------------------------+-----------------------------------------+
        | options dynamically change to single option A                                 | ⚪ A                                    |
        +-------------------------------------------------------------------------------+-----------------------------------------+
        | options dynamically change to multiple options                                | ⚪ A, ⚪ B, ⚪ C                        |
        +-------------------------------------------------------------------------------+-----------------------------------------+
        | user selects option B                                                         | ⚪ A, ⚫ B, ⚪ C                        |
        +-------------------------------------------------------------------------------+-----------------------------------------+
        | options dynamically change to multiple options, excluding the selected option | ⚪ A, ❌ B, ⚪ C (warning in interface) |
        +-------------------------------------------------------------------------------+-----------------------------------------+

        When `autoselect_single_option=True`, expect the following behavior:

        .. warning:: Keep in mind that in case of dynamic options and the possibility of having a single option,
           the (automatically) selected option might be changed without the user being aware of this!

        +-------------------------------------------------------------------------------+-----------------------------------------+
        | Action                                                                        | Options                                 |
        +===============================================================================+=========================================+
        | enter the editor                                                              | ⚪ A, ⚪ B, ⚪ C                        |
        +-------------------------------------------------------------------------------+-----------------------------------------+
        | options dynamically change to single option A                                 | ⚫ A                                    |
        +-------------------------------------------------------------------------------+-----------------------------------------+
        | options dynamically change to multiple options                                | ⚫ A, ⚪ B, ⚪ C                        |
        +-------------------------------------------------------------------------------+-----------------------------------------+
        | options dynamically change to single option B (user might not be aware!)      | ⚫ B                                    |
        +-------------------------------------------------------------------------------+-----------------------------------------+
        | options dynamically change to multiple options, excluding the selected option | ⚪ A, ❌ B, ⚪ C (warning in interface) |
        +-------------------------------------------------------------------------------+-----------------------------------------+

        Data:

        - type of selected option: integer, float or string
        - None when nothing is selected

        """

class MultiSelectField(_SelectField):
    """ Present dropdown list with options for user, in which multiple options can be selected.

    If there is only one option, this option will not be automatically selected.

    Example usage:

    .. code-block:: python

        field = vkt.MultiSelectField('Available options', options=['Option 1', 'Option 2'], default=['Option 1', 'Option 2'])

    Or use an OptionListElement to obtain a value in the params which differs from the interface name:

    .. code-block:: python

        _options = [vkt.OptionListElement('option_1', 'Option 1'), OptionListElement('option_2', 'Option 2')]
        field = vkt.MultiSelectField('Available options', options=_options, default=['option_1', 'option_2'])

    """
    def __init__(self, ui_name: str, options: list[float | str | OptionListElement] | Callable, name: str = None, prefix: str = None, suffix: str = None, default: list[float | str] = None, visible: VisibleType = True, flex: int = None, *, description: str = None) -> None:
        """
        See :class:`Field` for parameters.

        Additional parameters:

        :param options: Options should be defined as a list of numbers, strings, or OptionListElement objects.

        Data:

        - empty list if no options are selected
        - list with values of :class:`OptionListElements <OptionListElement>`: integer, float or string

        """
MultipleSelectField = MultiSelectField

class AutocompleteField(_SelectField):
    """ Similar to `OptionField`, except for two differences:

    - user can type to search for option
    - single option is not pre-selected

    Example usage:

    .. code-block:: python

        field = vkt.AutocompleteField('Available options', options=['Option 1', 'Option 2'], default='Option 1')

    Or use an OptionListElement to obtain a value in the params which differs from the interface name:

    .. code-block:: python

        _options = [vkt.OptionListElement('option_1', 'Option 1'), vkt.OptionListElement('option_2', 'Option 2')]
        field = vkt.AutocompleteField('Available options', options=_options, default='option_1')

    """
    def __init__(self, ui_name: str, options: list[float | str | OptionListElement] | Callable, name: str = None, prefix: str = None, suffix: str = None, default: float | str = None, visible: VisibleType = True, flex: int = None, *, description: str = None) -> None:
        """
        See :class:`Field` for parameters.

        Additional parameters:

        :param options: Options should be defined as a list of numbers, strings, or OptionListElement objects.

        Data:

        - type of selected option: integer, float or string
        - None when nothing is selected

        """

class _EntityField(Field, ABC, metaclass=abc.ABCMeta):
    def __init__(self, *, ui_name: str, name: str = None, visible: VisibleType = True, flex: int = None, entity_type_names: list[str] = None, description: str = None) -> None: ...

class _EntitySelectField(_EntityField, ABC, metaclass=abc.ABCMeta): ...

class EntityOptionField(_EntitySelectField):
    def __init__(self, ui_name: str, entity_type_names: list[str], *, name: str = None, visible: VisibleType = True, flex: int = None, description: str = None) -> None:
        """ Field to select any entity of given type(s).

        Single option is not automatically pre-selected.

        See :class:`Field` for parameters.

        Additional parameters:

        :param entity_type_names: User will only be able to select entities of type(s) within this list.

        Data:

            - :class:`~.viktor.api_v1.Entity`
            - None when nothing is selected

        """

class _EntityOptionField(_EntitySelectField, ABC, metaclass=abc.ABCMeta):
    def __init__(self, ui_name: str, name: str = None, visible: VisibleType = True, flex: int = None, *, entity_type_names: list[str] = None, description: str = None) -> None:
        """
        See :class:`Field` for parameters.

        Additional parameters:

        :param entity_type_names: User will only be able to select entities of types within this list. None = all
         entities.
        """

class ChildEntityOptionField(_EntityOptionField):
    """
    Field to select a child entity of given type(s).
    Single option is not automatically pre-selected.

    Data:

    - :class:`~.viktor.api_v1.Entity`
    - None when nothing is selected
    """
class SiblingEntityOptionField(_EntityOptionField):
    """
    Field to select a sibling entity of given type(s).
    Single option is not automatically pre-selected.

    Data:

    - :class:`~.viktor.api_v1.Entity`
    - None when nothing is selected
    """
class _EntityMultiField(_EntityField, ABC, metaclass=abc.ABCMeta): ...

class _EntityMultiSelectField(_EntityMultiField, ABC, metaclass=abc.ABCMeta):
    def __init__(self, ui_name: str, name: str = None, visible: VisibleType = True, flex: int = None, *, entity_type_names: list[str] = None, description: str = None) -> None:
        """
        See :class:`Field` for parameters.

        Additional parameters:

        :param entity_type_names: User will only be able to select entities of types within this list. None = all
         entities.
        """

class EntityMultiSelectField(_EntityMultiField):
    def __init__(self, ui_name: str, entity_type_names: list[str], *, name: str = None, visible: VisibleType = True, flex: int = None, description: str = None) -> None:
        """ Field to select zero or more entities of given type(s).

        See :class:`Field` for parameters.

        Additional parameters:

        :param entity_type_names: User will only be able to select entities of types within this list.

        Data:

            - List[:class:`~.viktor.api_v1.Entity`]
            - Empty list when nothing is selected

        """

class ChildEntityMultiSelectField(_EntityMultiSelectField):
    """
    Field to select zero or more child entities of given type(s).
    Up to 5000 entities may be visualized in the dropdown in the interface.

    Data:

    - List[:class:`~viktor.api_v1.Entity`]
    - Empty list when nothing is selected
    """

class ChildEntityManager(Field):
    def __init__(self, entity_type_name: str, *, visible: VisibleType = True) -> None:
        """ ::version(v14.2.0)

        Manager in which a user can create, inspect, and delete child entities of a specific type.

        :param entity_type_name: User will only be able to manage entities of specified type.
        :param visible: Can be used when the visibility depends on other input fields.
        """

class SiblingEntityMultiSelectField(_EntityMultiSelectField):
    """
    Field to select zero or more sibling entities of given type(s).
    Up to 5000 entities may be visualized in the dropdown in the interface.

    Data:

    - List[:class:`~viktor.api_v1.Entity`]
    - Empty list when nothing is selected
    """

class _FileField(Field, ABC, metaclass=abc.ABCMeta):
    def __init__(self, ui_name: str, file_types: Sequence[str] = None, *, max_size: int = None, name: str = None, visible: VisibleType = True, flex: int = None, description: str = None) -> None:
        """
        See :class:`Field` for parameters.

        Additional parameters:

        :param file_types: Optional restriction on file type(s) (e.g. ['.png', '.jpg', '.jpeg']) (case-insensitive).
        :param max_size: Optional restriction on file size in bytes (e.g. 10_000_000 = 10 MB).
        """

class FileField(_FileField):
    """ FileField can be used to let the user upload a file.

    Data:

    - :class:`~viktor.api_v1.FileResource`
    - None when nothing is uploaded
    """
class MultiFileField(_FileField):
    """ MultiFileField can be used to let the user upload multiple files.

    Data:

    - List[:class:`~viktor.api_v1.FileResource`]
    - Empty list when nothing is uploaded
    """

class _GeometryField(Field, ABC, metaclass=abc.ABCMeta):
    def __init__(self, ui_name: str, *, name: str = None, default: str | list[str] = None, visible: VisibleType = True, flex: int = None, description: str = None, view: str = None) -> None:
        """
        See :class:`Field` for parameters.

        Additional parameters:

        :param view: View method to which the field is connected (default: first GeometryView / IFCView).
        """

class GeometrySelectField(_GeometryField):
    """ ::version(v14.10.0)

    GeometrySelectField can be used to let the user select a geometry object from a View.

    Data:

    - str
    - None when nothing is selected
    """

class GeometryMultiSelectField(_GeometryField):
    """ ::version(v14.10.0)

    GeometryMultiSelectField can be used to let the user select multiple geometry objects from a View.

    Data:

    - List[str]
    - Empty list when nothing is selected
    """
    def __init__(self, ui_name: str, *, name: str = None, default: list[str] = None, visible: VisibleType = True, flex: int = None, description: str = None, view: str = None, min_select: int = 1, max_select: int = None) -> None:
        """
        See :class:`Field` for parameters.

        Additional parameters:

        :param view: View method to which the field is connected (default: first GeometryView / IFCView).
        :param min_select: Minimum amount of objects the user needs to select.
        :param max_select: Maximum amount of objects the user is allowed to select.
        """

class Table(Field, _AttrGroup):
    """Table input field with column definitions.

    .. warning::
        **Nesting Restrictions:**
        
        - Specifying a ``default`` on a field within a table is not supported
        - Specifying constraints on a field within a table is not supported
        - Cannot nest :class:`Table` within :class:`Table`
        - Cannot nest :class:`DynamicArray` within :class:`Table`
        - Tables can **only** contain the field types listed below

    **Supported Column Types:**

        - :class:`TextField`
        - :class:`NumberField` (without min/max constraints)
        - :class:`IntegerField`
        - :class:`BooleanField`
        - :class:`OptionField` (options argument required)
        - :class:`AutocompleteField`

    Example usage:

    .. code-block:: python

        # Define table structure
        table = vkt.Table('Input table')
        table.name = vkt.TextField('Planet')
        table.period = vkt.NumberField('Orbital period', suffix='years')
        table.eccentricity = vkt.NumberField('Orbital eccentricity', num_decimals=3)

        # ❌ INCORRECT: min/max not allowed in tables
        # table.invalid = vkt.NumberField('Value', min=0, max=100)  # Will be ignored

    A table can also be created with default content. Assume the columns as defined above:

    .. code-block:: python

        _default_content = [
            {'name': 'Earth', 'period': 1, 'eccentricity': 0.017},
            {'name': 'Mars', 'period': 1.88, 'eccentricity': 0.093},
            {'name': 'Saturn', 'period': 29.42, 'eccentricity': 0.054},
        ]

        table = vkt.Table('Input table', default=_default_content)
        ...
    """
    def __init__(self, ui_name: str, name: str = None, *, default: list[dict] = None, visible: VisibleType = True, description: str = None) -> None:
        """ See :class:`Field` for parameters.

        Data:

        - list of dictionaries
        - empty list if there are no rows
        - when fields are empty, the corresponding empty values are used (see documentation of specific field)
        """
TableInput = Table

class _GeoField(Field, metaclass=abc.ABCMeta):
    @abstractmethod
    def __init__(self, ui_name: str, *, name: str = None, default: GeoPoint | GeoPolyline | GeoPolygon | list['GeoPoint'] | list['GeoPolyline'] | list['GeoPolygon'] = None, visible: VisibleType = True, description: str = None): ...

class GeoPointField(_GeoField):
    def __init__(self, ui_name: str, *, name: str = None, default: GeoPoint = None, visible: VisibleType = True, description: str = None) -> None:
        """ GeoPointField can be used for the selection of a geographical location on a MapView/GeoJSONView.

        See :class:`Field` for parameters.

        Data:

            - :class:`~viktor.geometry.GeoPoint`

        **Data Access:** Multiple patterns are supported:

        .. code-block:: python

            # ✓ Property access (recommended)
            lat = params.my_location.lat  # or .latitude
            lon = params.my_location.lon  # or .longitude

            # ✓ Subscript access
            lat = params.my_location['lat']  # or ['latitude']
            lon = params.my_location['lon']  # or ['longitude']
        """

class GeoPolylineField(_GeoField):
    def __init__(self, ui_name: str, *, name: str = None, default: GeoPolyline = None, visible: VisibleType = True, description: str = None) -> None:
        """ GeoPolylineField can be used for the selection of a geographical (poly)line on a MapView/GeoJSONView.

        See :class:`Field` for parameters.

        Data:

            - :class:`~viktor.geometry.GeoPolyline`

        **Data Access:** Multiple patterns are supported:

        .. code-block:: python

            # ✓ Direct iteration (recommended)
            for point in params.my_polyline:
                lat, lon = point.lat, point.lon

            # ✓ Access points via .points property
            for point in params.my_polyline.points:
                lat, lon = point.lat, point.lon
        """

class GeoPolygonField(_GeoField):
    def __init__(self, ui_name: str, *, name: str = None, default: GeoPolygon = None, visible: VisibleType = True, description: str = None) -> None:
        """ GeoPolygonField can be used for the selection of a geographical polygon on a MapView/GeoJSONView.

        See :class:`Field` for parameters.

        Data:

            - :class:`~viktor.geometry.GeoPolygon`

        **Data Access:** Multiple patterns are supported:

        .. code-block:: python

            # ✓ Direct iteration (recommended)
            for point in params.my_polygon:
                lat, lon = point.lat, point.lon

            # ✓ Access points via .points property
            for point in params.my_polygon.points:
                lat, lon = point.lat, point.lon
        """

class _GeoMultiField(_GeoField, metaclass=abc.ABCMeta):
    @abstractmethod
    def __init__(self, ui_name: str, *, name: str = None, default: list['GeoPoint'] | list['GeoPolyline'] | list['GeoPolygon'] = None, visible: VisibleType = True, description: str = None): ...

class _GeoMultiPointField(_GeoMultiField):
    def __init__(self, ui_name: str, *, name: str = None, default: list['GeoPoint'] = None, visible: VisibleType = True, description: str = None) -> None:
        """ _GeoMultiPointField can be used for the selection of multiple geographical locations on a MapView/GeoJSONView.

        See :class:`Field` for parameters.

        Data:

            - List[:class:`~viktor.geometry.GeoPoint`]
        """

class _GeoMultiPolylineField(_GeoMultiField):
    def __init__(self, ui_name: str, *, name: str = None, default: list['GeoPolyline'] = None, visible: VisibleType = True, description: str = None) -> None:
        """ _GeoMultiPolylineField can be used for the selection of multiple (poly)lines on a MapView/GeoJSONView.

        See :class:`Field` for parameters.

        Data:

            - List[:class:`~viktor.geometry.GeoPolyline`]
        """

class _GeoMultiPolygonField(_GeoMultiField):
    def __init__(self, ui_name: str, *, name: str = None, default: list['GeoPolygon'] = None, visible: VisibleType = True, description: str = None) -> None:
        """ _GeoMultiPolygonField can be used for the selection of multiple polygons on a MapView/GeoJSONView.

        See :class:`Field` for parameters.

        Data:

            - List[:class:`~viktor.geometry.GeoPolygon`]
        """

class TextAreaField(Field):
    """ Multiple lines textual input. For one line use TextField. """
    def __init__(self, ui_name: str, name: str = None, default: str = None, visible: VisibleType = True, flex: int = 100, *, description: str = None) -> None:
        """
        See :class:`Field` for parameters.

        Data:

        - string
        - empty string, when empty
        """
TextAreaInput = TextAreaField

class Text(Field):
    def __init__(self, value: str, *, visible: VisibleType = True, flex: int = 100) -> None:
        """ Field that can be used to display a static text (max. 1800 characters). It is not included in the params.

        Changed in v13.3.0: character limit has been increased from 500 to 1800.

        See :class:`Field` for parameters.

        Additional parameters:

        :param value: Text to be shown
        """

class Image(Field):
    def __init__(self, path: str, *, align: Literal['left', 'center', 'right'] = 'center', caption: str = None, flex: int = 100, max_width: int = None, visible: VisibleType = True) -> None:
        ''' ::version(v14.3.0)

        Field that can be used to display a static image.

        :param path: Path to the image relative to the assets directory, note that path traversal is not allowed.
        :param align: Image alignment ("left" | "center" | "right").
        :param caption: Image caption (max. 200 characters).
        :param flex: Width of the image as percentage of the parametrization component.
        :param max_width: A maximum width (pixels) can be set to ensure an image does not end up pixelated.
        :param visible: Can be used when the visibility depends on other input fields.
        '''

class Chat(_ActionButton):
    ''' ::version(v14.21.0)

    **This field is currently in BETA**

    Chat field, e.g. to enable an LLM conversation.

    Example usage:

    .. code-block:: python

        # in parametrization:
        chat = vkt.Chat("Chatbot", method="call_llm", first_message="How can I help you?", placeholder="Ask anything")

        # in controller:
        def call_llm(self, params, **kwargs):
            conversation = params.chat
            text_stream = ...  # dependent on full conversation obtained with conversation.get_messages()
            return vkt.ChatResult(conversation, text_stream)

    Data:

    - :class:`~viktor.api_v1.ChatConversation`
    '''
    first_message: Incomplete
    placeholder: Incomplete
    def __init__(self, ui_name: str, method: str, *, first_message: str = None, placeholder: str = None, flex: int = None, visible: VisibleType = True) -> None:
        """
        :param ui_name: Name which is visible in the VIKTOR user interface.
        :param method: Name of the download method that is defined in the controller
        :param first_message: First message that is shown in the chat (or None for default message)
        :param placeholder: Placeholder message in the prompt (or None for default message)
        :param flex: Width of the image as percentage of the parametrization component (value betweeb 0-100)
        :param visible: Visibility of the button. A Constraint can be used when the visibility depends on
                        other input fields.
        """

class AutodeskFileField(Field):
    def __init__(self, ui_name: str, oauth2_integration: str, *, file_types: Sequence[str] = None, name: str = None, visible: VisibleType = True, flex: int = None, description: str = None) -> None:
        """ ::version(14.25.0)

        See :class:`Field` for parameters.

        Additional parameters:

        :param oauth2_integration: Name of the Autodesk OAuth2Integration this field is linked to.
        :param file_types: Optional restriction on file type(s) (e.g. ['.rvt']) (case-insensitive).
        """

class HiddenField:
    """
    The purpose of a HiddenField is to store data in the parametrization, without the necessity to show this
    information in the editor.

    .. warning:: Do NOT store tremendous amounts of data when it is not necessary, as this will make your
      application slow and perhaps unstable!
    """
    def __init__(self, ui_name: str, name: str = None) -> None:
        """
        :param ui_name: User-defined name of the field.
        :param name: The position of the parameter in the database can be specified in this argument.
        """

class OptionListElement:
    def __init__(self, value: float | str, label: str = None, visible: bool | BoolOperator | Lookup | FunctionLookup = True) -> None:
        """
        Create an option which can be used inside an OptionField.

        Example: value only with type str

        >>> option = OptionListElement('apple')
        >>> option.value
        'apple'
        >>> option.label
        'apple'

        Example: value only with type int

        >>> option = OptionListElement(33)
        >>> option.value
        33
        >>> option.label
        '33'

        Example: value and label

        >>> option = OptionListElement('apple', 'Delicious apple')
        >>> option.value
        'apple'
        >>> option.label
        'Delicious apple'

        :param value: The identifier which is used to store and retrieve chosen option.
        :param label: The identifier which is shown to the user.
                      If no label is specified, the value identifier is used, cast to a string.
        :param visible: Determines whether option is visible. Will mostly be used with Constraint.
        """
    @property
    def label(self) -> str: ...
    @property
    def value(self) -> float | str: ...
    def __eq__(self, other: object) -> bool: ...

class Parametrization(metaclass=_OrderedClass):
    """
    The Parametrization class functions as the basis of the parameter set of an entity.

    A simple parametrization looks as follows:

    .. code-block:: python

        import viktor as vkt

        class Parametrization(vkt.Parametrization):
            input_1 = vkt.TextField('This is a text field')
            input_2 = vkt.NumberField('This is a number field')

    In the VIKTOR user interface, this will be visualized as:

    .. figure:: ../_static/editor-single-layered.png
        :width: 800px
        :align: center

    In some cases, the parametrization becomes quite big which requires a more structured layout.
    This can be achieved by making use of a :class:`Tab` and :class:`Section` object, which
    represent a tab and collapsible section in the interface respectively.

    A 2-layered structure using `Tab` objects looks like this:

    .. code-block:: python

        import viktor as vkt


        class Parametrization(vkt.Parametrization):
            tab_1 = vkt.Tab('Tab 1')
            tab_1.input_1 = vkt.TextField('This is a text field')
            tab_1.input_2 = vkt.NumberField('This is a number field')

            tab_2 = vkt.Tab('Tab 2')
            tab_2.input_1 = vkt.TextField('Text field in Tab 2')
            tab_2.input_2 = vkt.NumberField('Number field in Tab 2')


    .. figure:: ../_static/editor-two-layered-tabs.png
        :width: 800px
        :align: center

    Using `Section` objects results in the following:

    .. code-block:: python

        import viktor as vkt


        class Parametrization(vkt.Parametrization):
            section_1 = vkt.Section('Section 1')
            section_1.input_1 = vkt.TextField('This is a text field')
            section_1.input_2 = vkt.NumberField('This is a number field')

            section_2 = vkt.Section('Section 2')
            section_2.input_1 = vkt.TextField('Text field in Section 2')
            section_2.input_2 = vkt.NumberField('Number field in Section 2')

    .. figure:: ../_static/editor-two-layered-sections.png
        :width: 800px
        :align: center

    A parametrization with a maximum depth of 3 layers consists of `Tab`, `Section`, and `Field` objects:

    .. code-block:: python

        import viktor as vkt


        class Parametrization(vkt.Parametrization):
            tab_1 = vkt.Tab('Tab 1')
            tab_1.section_1 = vkt.Section('Section 1')
            tab_1.section_1.input_1 = vkt.TextField('This is a text field')
            tab_1.section_1.input_2 = vkt.NumberField('This is a number field')

            tab_1.section_2 = vkt.Section('Section 2')
            ...

            tab_2 = vkt.Tab('Tab 2')
            ...

    .. figure:: ../_static/editor-three-layered.png
        :width: 800px
        :align: center

    Every class attribute is treated as a tab, section, or field. If you want to use a variable inside a field,
    you can either define it outside of the class or as class attribute starting with an underscore:

    .. code-block:: python

        OPTIONS = ['Option 1', 'Option 2']

        class Parametrization(vkt.Parametrization):

            _options = ['Option 3', 'Option 4']
            field_1 = vkt.OptionField('Choose option', options=OPTIONS)
            field_2 = vkt.OptionField('Choose option', options=_options)

    **Callback Functions:** When using callback functions for ``visible``, ``min``, or ``max`` parameters,
    define them before the Parametrization class:

    .. code-block:: python

        import viktor as vkt

        def my_visibility(params, **kwargs):
            return params.field_1 > 5

        class Parametrization(vkt.Parametrization):
            field_1 = vkt.NumberField('Field 1')
            field_2 = vkt.NumberField('Field 2', visible=my_visibility)

    **Adjusting Width:** The parametrization width defaults to 40% of the editor. Use the ``width`` parameter
    (range: 20-80%) to adjust this ratio:

    .. code-block:: python

        class Parametrization(vkt.Parametrization):
            number = vkt.NumberField('Number', flex=100)

        class Controller(vkt.Controller):
            parametrization = Parametrization(width=60)

    Individual fields can use ``flex`` (0-100) to adjust their width relative to the parametrization side.
    The ``width`` and ``flex`` parameters multiply: ``width=30`` with ``flex=100`` results in a field
    taking 30% of the total editor width.

    """
    def __init__(self, *, width: int = None) -> None:
        """

        :param width: Sets the width of the parametrization side as percentage of the complete width of the editor
          (input + output). The value should be an integer between 20 and 80 (default: 40). If a width is defined
          both on the Parametrization and a Page / Step, the Page / Step takes precedence.
        """
ViktorParametrization = Parametrization

class _Group(_AttrGroup, metaclass=abc.ABCMeta):
    def __init__(self, title: str, description: str = None, visible: bool | BoolOperator | Lookup | FunctionLookup | Callable = True) -> None:
        """

        :param title: Title which is shown in the interface.
        """

class Page(_Group):
    ''' A Page can be used to group certain inputs (e.g. fields) with certain outputs (views).

    For example:

    .. code-block:: python

        class Parametrization(vkt.Parametrization):
            page_1 = vkt.Page(\'Page 1\')  # no views
            page_1.field_1 = vkt.NumberField(...)
            ...

            page_2 = vkt.Page(\'Page 2\', views=\'view_data\')  # single view
            page_2.field_1 = vkt.NumberField(...)
            ...

            page_3 = vkt.Page(\'Page 3\', views=[\'view_map\', \'view_data\'])  # multiple views
            page_3.field_1 = vkt.NumberField(...)
            ...


        class Controller(vkt.Controller):
            ...

            @vkt.DataView(...)  # visible on "Page 2" and "Page 3"
            def view_data(self, params, **kwargs):
                ...

            @vkt.MapView(...)  # only visible on "Page 3"
            def view_map(self, params, **kwargs):
                ...

    **(new in v14.7.0)** Adjust the width of a specific page:

    .. code-block:: python

        class Parametrization(vkt.Parametrization):
            page_1 = vkt.Page(\'Page 1\', width=30)
            ...
            page_2 = vkt.Page(\'Page 2\', width=70)
            ...

    '''
    def __init__(self, title: str, *, views: str | Sequence[str] = None, description: str = None, visible: bool | BoolOperator | Lookup | FunctionLookup | Callable = True, width: int = None) -> None:
        """
        :param title: Title which is shown in the interface.
        :param views: View method(s) that should be visible in this page, e.g. 'my_view' for a single view, or
            ['my_data_view', 'my_geometry_view', ...] for multiple views (default: None).
        :param description: Show more information to the user through a tooltip on hover (max. 200 characters).
        :param visible: Can be used when the visibility depends on other input fields. ::version(v14.7.0)
        :param width: Sets the width of the parametrization side of this page as percentage of the complete width
          of the editor (input + output). The value should be an integer between 20 and 80. If a width is defined both
          on the Parametrization and the Page, the Page takes precedence. ::version(v14.7.0)
        """

class Step(Page):
    ''' A Step can be used to group certain inputs (e.g. fields) with certain outputs (views) within a predefined
    order, browsable through a previous and next button.

    For example:

    .. code-block:: python

        class Parametrization(vkt.Parametrization):
            step_1 = vkt.Step(\'Step 1\')  # no views
            step_1.field_1 = vkt.NumberField(...)
            ...

            step_2 = vkt.Step(\'Step 2\', views=\'view_data\')  # single view
            step_2.field_1 = vkt.NumberField(...)
            ...

            step_3 = vkt.Step(\'Step 3\', views=[\'view_map\', \'view_data\'])  # multiple views
            step_3.field_1 = vkt.NumberField(...)
            ...


        class Controller(vkt.Controller):
            ...

            @vkt.DataView(...)  # visible on "Step 2" and "Step 3"
            def view_data(self, params, **kwargs):
                ...

            @vkt.MapView(...)  # only visible on "Step 3"
            def view_map(self, params, **kwargs):
                ...

    **(new in v13.7.0)** When implementing the `on_next` argument, the corresponding function is called when a user
    clicks the \'next\' button to move to the next step. This can be used to, for example, validate the input of the
    current active step:

    .. code-block:: python

        def validate_step_1(params, **kwargs):
            if params.step_1.field_z <= params.step_1.field_x + params.step_1.field_y:
                raise vkt.UserError(...)


        class Parametrization(vkt.Parametrization):
            step_1 = vkt.Step(\'Step 1\', on_next=validate_step_1)
            ...

    **(new in v14.7.0)** Adjust the width of a specific step:

    .. code-block:: python

        class Parametrization(vkt.Parametrization):
            step_1 = vkt.Step(\'Step 1\', width=30)
            ...
            step_2 = vkt.Step(\'Step 2\', width=70)
            ...

    **(new in v14.11.0)** Disable steps:

    Disabled steps are skipped, you will go straight from Step 1 to Step 3 if Step 2 is disabled.

    .. code-block:: python

        def is_step_enabled(params, **kwargs):
            return params.step_1.field_z <= params.step_1.field_x + params.step_1.field_y

        class Parametrization(vkt.Parametrization):
            step_1 = vkt.Step(\'Step 1\', enabled=True)
            ...
            step_2 = vkt.Step(\'Step 2\', enabled=is_step_enabled)
            ...
            step_3 = vkt.Step(\'Step 3\') # enabled=True by default
            ...

    '''
    def __init__(self, title: str, *, views: str | Sequence[str] = None, description: str = None, enabled: bool | BoolOperator | Lookup | FunctionLookup | Callable = True, previous_label: str = None, next_label: str = None, on_next: Callable = None, width: int = None) -> None:
        """
        :param title: Title which is shown in the interface.
        :param views: View method(s) that should be visible in this step, e.g. 'my_view' for a single view, or
            ['my_data_view', 'my_geometry_view', ...] for multiple views (default: None).
        :param description: Show more information to the user through a tooltip on hover (max. 200 characters).
        :param enabled: Can be used to disable (skip) steps, may depend on other input fields. ::version(v14.11.0)
        :param previous_label: Text to be shown on the previous button (ignored for first step, max. 30 characters).
        :param next_label: Text to be shown on the next button (ignored for last step, max. 30 characters).
        :param on_next: Callback function which is triggered when the user moves to the next step. ::version(v13.7.0)
        :param width: Sets the width of the parametrization side of this step as percentage of the complete width
          of the editor (input + output). The value should be an integer between 20 and 80. If a width is defined both
          on the Parametrization and the Step, the Step takes precedence. ::version(v14.7.0)
        """

class Tab(_Group):
    def __init__(self, title: str, *, description: str = None, visible: bool | BoolOperator | Lookup | FunctionLookup | Callable = True) -> None:
        """
        :param title: Title which is shown in the interface.
        :param description: Show more information to the user through a tooltip on hover (max. 200 characters).
        :param visible: Can be used when the visibility depends on other input fields. ::version(v14.7.0)
        """

class Section(_Group):
    def __init__(self, title: str, *, description: str = None, initially_expanded: bool | None = None, visible: bool | BoolOperator | Lookup | FunctionLookup | Callable = True) -> None:
        """
        :param title: Title which is shown in the interface.
        :param description: Show more information to the user through a tooltip on hover (max. 200 characters).
        :param initially_expanded: Whether the section should be expanded on editor entry ::version(v14.21.0)
        :param visible: Can be used when the visibility depends on other input fields. ::version(v14.7.0)
        """
