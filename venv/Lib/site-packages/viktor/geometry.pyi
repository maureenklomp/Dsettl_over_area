import abc
import numpy as np
import trimesh
import uuid
from .core import Color, File
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from typing import Any, Iterator, Sequence, TextIO, TypeVar

__all__ = ['Arc', 'ArcExtrusion', 'ArcRevolve', 'BidirectionalPattern', 'CartesianAxes', 'CircularExtrusion', 'Cone', 'Extrusion', 'GeoPoint', 'GeoPolygon', 'GeoPolyline', 'Group', 'Line', 'LineRevolve', 'LinearPattern', 'Material', 'Pattern', 'Point', 'Polygon', 'Polyline', 'RDWGSConverter', 'RectangularExtrusion', 'Revolve', 'Sphere', 'SquareBeam', 'Torus', 'TransformableObject', 'Triangle', 'TriangleAssembly', 'Vector']

T = TypeVar('T')

class Vector:
    """ A 3-dimensional vector in space.

    The following operations are supported:

    - Negation

        .. code-block:: python

            v1 = Vector(1, 2, 3)
            v2 = -v1  # results in Vector(-1, -2, -3)

    - Addition

        .. code-block:: python

            v1 = Vector(1, 2, 3)
            v2 = Vector(1, 2, 3)
            v3 = v1 + v2  # results in Vector(2, 4, 6)

    - Subtraction

        .. code-block:: python

            v1 = Vector(1, 2, 3)
            v2 = Vector(1, 2, 3)
            v3 = v1 - v2  # results in Vector(0, 0, 0)

    - (reverse) Multiplication

        .. code-block:: python

            v1 = Vector(1, 2, 3)
            v2 = v1 * 3  # results in Vector(3, 6, 9)
            v3 = 3 * v1  # results in Vector(3, 6, 9)

    - Dot product

        .. code-block:: python

            v1 = Vector(1, 2, 3)
            v2 = Vector(1, 2, 3)
            res = v1.dot(v2)  # results in 14

    - Cross product

        .. code-block:: python

            v1 = Vector(1, 0, 0)
            v2 = Vector(0, 1, 0)
            v3 = v1.cross(v2)  # results in Vector(0, 0, 1)
    """
    x: Incomplete
    y: Incomplete
    z: Incomplete
    def __init__(self, x: float, y: float, z: float = 0) -> None:
        """
        :param x: X-coordinate.
        :param y: Y-coordinate.
        :param z: Z-coordinate (default: 0).
        """
    def __getitem__(self, index: int) -> float: ...
    def __iter__(self) -> Iterator[float]: ...
    def __eq__(self, other: object) -> bool: ...
    def __neg__(self) -> Vector: ...
    def __add__(self, other: Vector) -> Vector: ...
    def __sub__(self, other: Vector) -> Vector: ...
    def __mul__(self, other: float) -> Vector: ...
    def __rmul__(self, other: float) -> Vector: ...
    @property
    def squared_magnitude(self) -> float:
        """ Vector magnitude without square root; faster than magnitude. """
    @property
    def magnitude(self) -> float:
        """ Magnitude of the Vector. """
    @property
    def coordinates(self) -> tuple[float, float, float]:
        """ Coordinates of the Vector as tuple (X, Y, Z). """
    def normalize(self) -> Vector:
        """ Return the normalized vector (with unit-length).

        :raises ValueError: if vector is a null-vector.
        """
    def dot(self, other: Vector) -> float:
        """ Scalar product of two vectors.

        :param other: Second Vector
        """
    def cross(self, other: Vector) -> Vector:
        """ Vector product of two vectors.

        :param other: Second Vector
        """

class _GLTF:
    @staticmethod
    def add_geometry_to_scene(scene: trimesh.Scene, geometry: trimesh.parent.Geometry3D, *, transform: np.ndarray = None, **metadata: Any) -> str:
        """ Method to add geometry to an existing scene. """
    @classmethod
    def to_gltf(cls, *objects: TransformableObject) -> File: ...

class Material:
    uuid: Incomplete
    name: Incomplete
    density: Incomplete
    price: Incomplete
    color: Incomplete
    roughness: Incomplete
    metalness: Incomplete
    opacity: Incomplete
    def __init__(self, name: str = None, density: float = None, price: float = None, *, threejs_type: str = 'MeshStandardMaterial', roughness: float = 1.0, metalness: float = 0.5, opacity: float = 1.0, color: str | tuple[int, int, int] | Color = ...) -> None:
        """
        .. note:: The following properties were renamed since v14.5.0.
          If you are using a lower version, please use the old naming.

          - threejs_roughness -> roughness
          - threejs_metalness -> metalness
          - threejs_opacity -> opacity

        **(new in v14.22.0)** Provide a hex value or tuple (r, g, b) as 'color'.

        :param name: Optional name.
        :param density: Optional density.
        :param price: Optional price.
        :param threejs_type: deprecated
        :param roughness: Between 0 - 1 where closer to 1 gives the material a rough texture.
        :param metalness: Between 0 - 1 where closer to 1 gives the material a shiny metal look.
        :param opacity: Between 0 - 1 where closer to 0 makes the material less visible.
        :param color: Color of the material.
        """

class TransformableObject(ABC, metaclass=abc.ABCMeta):
    def __init__(self, *, identifier: str = None) -> None: ...
    def translate(self, translation_vector: Vector | tuple[float, float, float]) -> TransformableObject:
        """ Translate an object along a translation vector.

        :param translation_vector: Vector along which translation is to be performed.
        """
    def rotate(self, angle: float, direction: Vector | tuple[float, float, float], point: Point | tuple[float, float, float] = None) -> TransformableObject:
        """ Rotate an object along an axis (direction) by an angle. Direction will follow right hand rule.

        :param angle: Angle of desired rotation in radians.
        :param direction: Vector along which rotation is to be performed.
        :param point: Point through which the rotation vector runs.
        """
    def mirror(self, point: Point | tuple[float, float, float], normal: Vector | tuple[float, float, float]) -> TransformableObject:
        """ Mirror an object on a plane defined by a point and normal vector.

        :param point: Point within the mirror plane.
        :param normal: Normal vector of the mirror plane.
        """
    def scale(self, scaling_vector: Vector | tuple[float, float, float]) -> TransformableObject:
        """ Scale an object along a scaling vector.

        :param scaling_vector: Vector along which scaling is to be performed.
        """

class Group(TransformableObject):
    def __init__(self, objects: Sequence[TransformableObject], *, identifier: str = None) -> None:
        """
        :param objects: Objects that are part of the group.
        :param identifier: object identifier (new in v14.10.0)
        """
    def add(self, objects: list | tuple | TransformableObject) -> None: ...
    @property
    def children(self) -> list[TransformableObject]: ...
    def duplicate(self) -> Group: ...

class Point:
    """
    This class represents a point object, which is instantiated by means of 3-dimensional coordinates X, Y, and Z. It
    forms a basis of many structural 2D and 3D objects.

    Example usage:

    .. code-block:: python

        p1 = Point(1, 2)        # create a 2D point
        p1.z                    # 0
        p2 = Point(1, 2, 3)     # create a 3D point
        p1.z                    # 3
    """
    def __init__(self, x: float, y: float, z: float = 0) -> None:
        """
        :param x: X-coordinate.
        :param y: Y-coordinate.
        :param z: (optional) Z-coordinate, defaults to 0.

        :raises TypeError: if the point is instantiated with a None value.
        """
    def __getitem__(self, index: int) -> float: ...
    def __iter__(self) -> Iterator[float]: ...
    def __eq__(self, other: object) -> bool: ...
    @property
    def x(self) -> float:
        """ X-coordinate. """
    @property
    def y(self) -> float:
        """ Y-coordinate. """
    @property
    def z(self) -> float:
        """ Z-coordinate. """
    @property
    def coordinates(self) -> np.ndarray:
        """ Coordinates of the Point as array (X, Y, Z). """
    def copy(self) -> Point:
        """ Returns a deep copy of the object. """
    def coincides_with(self, other: Point) -> bool:
        """ Given another `Point` object, this method determines whether the two points coincide. """
    def vector_to(self, point: Point | tuple[float, float, float]) -> Vector:
        """ Vector pointing from self to point.

        Example usage:

        .. code-block:: python

            p1 = Point(1, 2, 3)
            p2 = Point(0, 0, 0)         # origin
            v = p1.vector_to(p2)        # vector from p1 to the origin
            v = p1.vector_to((0, 0, 0)) # short notation
        """
    def get_local_coordinates(self, local_origin: Point | tuple[float, float, float], spherical: bool = False) -> np.ndarray:
        """ Method to determine the local coordinates of the current Point with respect to a 'local origin'. """

class Line(TransformableObject):
    color: Incomplete
    def __init__(self, start_point: Point | tuple[float, float, float], end_point: Point | tuple[float, float, float], *, color: Color = ..., identifier: str = None) -> None:
        """
        :param start_point: Start point of the line (cannot coincide with end_point).
        :param end_point: End point of the line (cannot coincide with start_point).
        :param color: Visualization color ::version(v13.5.0).
        :param identifier: object identifier (new in v14.10.0)
        """
    def __getitem__(self, index: int) -> Point: ...
    def __iter__(self) -> Iterator[Point]: ...
    def __eq__(self, other: object) -> bool: ...
    @property
    def start_point(self) -> Point: ...
    @property
    def end_point(self) -> Point: ...
    @property
    def length(self) -> float: ...
    def direction(self, normalize: bool = True) -> Vector:
        """ Direction vector between start and end point. """
    def collinear(self, point: Point | tuple[float, float, float]) -> bool:
        """ True if point is collinear (in line) with Line, else False. """
    def project_point(self, point: Point | tuple[float, float, float]) -> Point:
        """ Project the point on the (unbounded) line. """
    def distance_to_point(self, point: Point | tuple[float, float, float]) -> float:
        """ Calculate the (minimal) distance from the given point to the (unbounded) line. """
    @property
    def length_vector(self) -> np.ndarray: ...
    @property
    def unit_vector(self) -> np.ndarray: ...
    @property
    def geometries(self) -> tuple[Point, Point]:
        """:meta private:"""
    @property
    def horizontal(self) -> bool: ...
    @property
    def vertical(self) -> bool: ...
    def discretize(self, num: int = 2) -> list[Point]:
        """:meta private:"""
    def revolve(self, *, material: Material = None, identifier: str = None, **kwargs: Any) -> LineRevolve:
        """ Revolve line around y-axis, only possible for lines in x-y plane.

        :param material: optional material
        :param identifier: object identifier (new in v14.10.0)

        :raises NotImplementedError: when line is not in x-y plane
        """
    def get_line_function_parameters(self) -> tuple[float, float]:
        """ Get parameters for y=ax+b definition of a line.

        :return: (a, b) or (nan, nan) if line is vertical
        """
    def find_overlap(self, other: Line, inclusive: bool = False) -> Point | Line | None:
        """ Find the overlapping part of this line with another line.

        The returned value depends on the situation:

        - None, if no overlap is found or the two lines are not parallel
        - Point, if an overlap is found with length equal to 0
        - Line, if an overlap is found with length larger than 0

        :param other: Other Line object
        :param inclusive: True to treat overlapping points as overlap
        """

class Revolve(TransformableObject, ABC, metaclass=abc.ABCMeta):
    """ Abstract base class of a revolved object."""
    material: Incomplete
    def __init__(self, *args: Any, rotation_angle: float = None, material: Material = None, identifier: str = None, **kwargs: Any) -> None: ...
    @property
    @abstractmethod
    def surface_area(self) -> float: ...
    @property
    @abstractmethod
    def inner_volume(self) -> float: ...
    @property
    def thickness(self) -> float: ...
    @thickness.setter
    def thickness(self, thickness: float) -> None: ...
    @property
    def mass(self) -> float:
        """Calculates the mass of the object as rho * area * thickness, with rho the density of the Material."""

class LineRevolve(Revolve):
    """ Returns a revolved object of a Line around the global y-axis.

    An example revolve of a line between the point (1, 1, 0) and (3, 2, 0) is shown below, with the line object
    shown in black.

    .. code-block:: python

        line = Line(Point(1, 1, 0), Point(3, 2, 0))
        line_rev = LineRevolve(line)


    .. figure:: ../_static/line-revolve.png
        :width: 800px
        :align: center
    """
    def __init__(self, line: Line, *args: Any, material: Material = None, identifier: str = None, **kwargs: Any) -> None:
        """
        :param line: Line object which is to be revolved.
        :param material: optional material
        :param identifier: object identifier (new in v14.10.0)
        """
    @property
    def line(self) -> Line: ...
    @property
    def uuid(self) -> uuid.UUID: ...
    @property
    def height(self) -> float: ...
    @property
    def surface_area(self) -> float:
        """ Returns the total exterior area of the revolved object. """
    @property
    def inner_volume(self) -> float:
        """ Returns the inner volume of the revolved object.

        This method will only return a value if the defined Line meets the following conditions:

            - it should NOT be horizontal, i.e. y_start != y_end
            - it should be defined in positive y-direction, i.e. y_start < y_end
        """
    @property
    def geometries(self) -> tuple[Line, ...]:
        """:meta private:"""

class Arc(TransformableObject):
    color: Incomplete
    def __init__(self, centre_point: Point | tuple[float, float, float], start_point: Point | tuple[float, float, float], end_point: Point | tuple[float, float, float], short_arc: bool = True, *, n_segments: int = 30, color: Color = ..., identifier: str = None) -> None:
        """ Creates a constant radius arc in the xy plane. Clockwise rotation creates an outward surface.

        :param centre_point: Point in xy plane.
        :param start_point: Point in xy plane. Should have the same distance to centre_point as end_point.
        :param end_point: Point in xy plane. Should have the same distance to centre_point as start_point.
        :param short_arc: Angle of arc smaller than pi if True, larger than pi if False.
        :param n_segments: Number of discrete segments of the arc (default: 30) ::version(v13.5.0).
        :param color: Visualization color ::version(v13.5.0).
        :param identifier: object identifier (new in v14.10.0)
        """
    @property
    def radius(self) -> float: ...
    @property
    def centre_point(self) -> Point: ...
    @property
    def start_point(self) -> Point: ...
    @property
    def end_point(self) -> Point: ...
    @property
    def n_segments(self) -> int: ...
    @property
    def theta1_theta2(self) -> tuple[float, float]:
        """ Angles of the end (theta1) and start (theta2) points with respect to the x-axis in radians. """
    @property
    def theta1(self) -> float:
        """ Angle of the end point with respect to the x-axis in radians. """
    @property
    def theta2(self) -> float:
        """ Angle of the start point with respect to the x-axis in radians. """
    @property
    def short_arc(self) -> bool: ...
    @property
    def geometries(self) -> tuple[Point, Point, Point]:
        """:meta private:"""
    @property
    def angle(self) -> float:
        """ Absolute angle of the arc in radians, which is the difference between theta1 and theta2. """
    @property
    def length(self) -> float:
        """ Arc length. """
    def discretize(self, num: int = 2) -> list[Point]:
        """
        Returns a discrete representation of the arc, as a list of Point objects. The amount of points can be
        specified using 'num', which should be larger than 1.
        """
    def revolve(self, *, rotation_angle: float = None, material: Material = None, identifier: str = None, **kwargs: Any) -> ArcRevolve:
        """ Returns an ArcRevolve object, revolved around the global y-axis.

        :param rotation_angle: Angle of the revolved object according to the right-hand-rule, with the start of the
            rotation in positive z-direction. Angle in radians. If not specified, 2 pi will be used.
        :param material: optional material
        :param identifier: object identifier (new in v14.10.0)
        """

class ArcRevolve(Revolve):
    """
    Returns a revolved object of an arc around the global y-axis.

    In the example below, rotation_angle is equal to pi / 3:

    .. figure:: ../_static/arc-revolve.png
        :width: 800px
        :align: center
    """
    def __init__(self, arc: Arc, *args: Any, rotation_angle: float = None, material: Material = None, identifier: str = None, **kwargs: Any) -> None:
        """
        :param arc: Arc object.
        :param rotation_angle: Angle of the revolved object according to the right-hand-rule, with the start of the
            rotation in positive z-direction. Angle in radians. If not specified, 2 pi will be used.
        :param material: optional material
        :param identifier: object identifier (new in v14.10.0)
        """
    @property
    def arc(self) -> Arc:
        """:class:`~.geometry.Arc`"""
    @property
    def uuid(self) -> str: ...
    @property
    def surface_area(self) -> float:
        """Total exterior area of the object."""
    @property
    def inner_volume(self) -> float:
        """
        Returns the inner volume of the revolved object.

        This method will only return a value if the defined Arc meets the following conditions:

           - it should be short, i.e. short_arc=True
           - the start- and end-point are located on the same side w.r.t. the y-axis of the center-point of the Arc
           - it is defined in clockwise direction
        """
    @property
    def height(self) -> float:
        """Height of the object."""
    @property
    def geometries(self) -> tuple[Arc, ...]:
        """:meta private:"""

class Triangle:
    """ Creates a Triangle object from 3D vertices. """
    profile: Incomplete
    vertices: Incomplete
    def __init__(self, point1: Point, point2: Point, point3: Point) -> None:
        """

        :param point1: First vertex.
        :param point2: Second vertex.
        :param point3: Third vertex.
        """
    def area(self) -> float:
        """ Returns the area of the triangle. """
    @property
    def centroid(self) -> tuple[float, float, float]:
        """ Returns the centroid (X, Y, Z) of the triangle. """
    @property
    def moment_of_inertia(self) -> tuple[float, float]:
        """ Returns the moment of inertia (Ix, Iy) (only in x-y plane). """

class CartesianAxes(Group):
    def __init__(self, origin: Point = ..., axis_length: float = 1, axis_diameter: float = 0.05) -> None:
        """
        Helper visualisation object to show positive x (red), y (green) and z (blue) axes.

        .. figure:: ../_static/cartesian-axes.png
            :width: 800px
            :align: center

        :param origin: Coordinates of the origin.
        :param axis_length: Length of the axes.
        :param axis_diameter: Diameter of the axes.
        """

class RDWGSConverter:
    """
    Class that provides functions to translate latitude and longitude coordinates between the WGS system and RD system.

    The RD coordinate system is a cartesian coordinate system that is frequently used for in civil engineering to
    describe locations in the Netherlands.
    The origin is located in france, so that for all of the Netherlands, both x (m) and y (m) values are positive and
    y is always larger then x.
    The domain in which the RD coordinate system is valid is:

    - x: [-7000, 300000]
    - y: [289000, 629000]

    About the RD coordinate system:
    https://nl.wikipedia.org/wiki/Rijksdriehoeksco%C3%B6rdinaten
    """
    X0: int
    Y0: int
    phi0: float
    lam0: float
    @staticmethod
    def from_rd_to_wgs(coords: tuple[float, float]) -> list[float]:
        """ Convert RD coordinates (x, y) to WGS coordinates [latitude, longitude].

        .. code-block:: python

            lat, lon = RDWGSConverter.from_rd_to_wgs((100000, 400000))

        :param coords: RD coordinates (x, y)
        """
    @staticmethod
    def from_wgs_to_rd(coords: tuple[float, float]) -> list[float]:
        """ Convert WGS coordinates (latitude, longitude) to RD coordinates [x, y].

        .. code-block:: python

            x, y = RDWGSConverter.from_wgs_to_rd((51.58622, 4.59360))

        :param coords: WGS coordinates (latitude, longitude)
        """

class Extrusion(Group):
    def __init__(self, profile: list[Point], line: Line, profile_rotation: float = 0, *, material: Material = None, identifier: str = None) -> None:
        """
        Extruded object from a given set of points, which is called the profile. This profile should meet the following
        requirements:

            - start point should be added at the end for closed profile
            - points should be defined in z=0 plane
            - circumference should be defined clockwise

        Note that the profile is defined with respect to the start point of the Line object, i.e. the profile is defined
        in the local coordinate system. An example is given below of two extrusions with the same dimensions. Their
        corresponding Line objects are also visualized. The extrusion have the following profile:

        .. code-block::

            # black box
            profile_b = [
                Point(1, 1),
                Point(1, 2),
                Point(2, 2),
                Point(2, 1),
                Point(1, 1),
            ]
            box_b = Extrusion(profile_b, Line(Point(4, 1, 0), Point(4, 1, 1)))

            # yellow box
            profile_y = [
                Point(-0.5, -0.5),
                Point(-0.5, 0.5),
                Point(0.5, 0.5),
                Point(0.5, -0.5),
                Point(-0.5, -0.5),
            ]
            box_y = Extrusion(profile_y, Line(Point(2, 2, 0), Point(2, 2, 1)))

        .. figure:: ../_static/extrusion-profile.png
            :width: 800px
            :align: center

        :param profile: Coordinates of cross-section.
        :param line: A line object is used to define the length (thickness) of the extrusion.
        :param profile_rotation: Rotation of the profile around the Z-axis in degrees.
        :param material: optional material
        :param identifier: object identifier (new in v14.10.0)
        """
    @property
    def children(self) -> None:
        """:meta private:"""
    @property
    def profile(self) -> list[Point]: ...
    @property
    def material(self) -> Material: ...
    @material.setter
    def material(self, material: Material) -> None: ...
    @property
    def line(self) -> Line: ...
    @property
    def length(self) -> float: ...
    @property
    def uuid(self) -> str:
        """:meta private:"""
    @property
    def geometries(self) -> Line:
        """:meta private:"""
    @property
    def transformation(self) -> np.ndarray:
        """:meta private:"""

class ArcExtrusion(Group):
    def __init__(self, profile: list[Point], arc: Arc, profile_rotation: float = 0, n_segments: int = 50, *, material: Material = None, identifier: str = None) -> None:
        """
        Given an Arc and a cross-section of the extrusion, a discretized Extrusion object is returned.

        The coordinates of the profile are defined with respect to the Arc and have a LOCAL coordinate system:

            - z-axis is in direction of the arc from start to end.
            - x-axis is in positive global z-axis.
            - y-axis follows from the right-hand-rule.

        Rotation of the profile is about the axis according to the right-hand-rule with LOCAL z-axis (see definition
        above).

        Example:

        .. code-block:: python

            profile = [
                Point(1, 1),
                Point(1, 2),
                Point(3, 2),
                Point(3, 1),
                Point(1, 1),
            ]
            arc = Arc(Point(1, 1, 0), Point(3, 1, 0), Point(1, 3, 0))
            arc_ext = ArcExtrusion(profile, arc, profile_rotation=10, n_segments=10)

        This will result in the following visualization, where the Arc itself is also shown in the xy plane:

        .. figure:: ../_static/arc-extrusion.png
            :width: 800px
            :align: center

        :param profile: Coordinates of cross-section.
        :param arc: An Arc object is used to define the direction of the extrusion.
        :param profile_rotation: Rotation of the profile around its local Z-axis in degrees.
        :param n_segments: Number of discrete segments of the arc, which is 50 by default.
        :param material: optional material
        :param identifier: object identifier (new in v14.10.0)
        """
    @property
    def children(self) -> None:
        """:meta private:"""

class CircularExtrusion(TransformableObject):
    material: Incomplete
    def __init__(self, diameter: float, line: Line, *, shell_thickness: float = None, material: Material = None, identifier: str = None) -> None:
        """
        This class is used to construct an extrusion which has a circular base, e.g. a circular foundation pile.

        :param diameter: Outer diameter of the cross-section.
        :param line: Line object along which the circular cross-section is extruded.
        :param shell_thickness: Optional shell thickness. None for solid (default: None) ::version(v13.6.0).
        :param material: Optional material.
        :param identifier: object identifier (new in v14.10.0)
        """
    @property
    def line(self) -> Line: ...
    @property
    def length(self) -> float: ...
    @property
    def diameter(self) -> float: ...
    @property
    def radius(self) -> float: ...
    @property
    def shell_thickness(self) -> float | None: ...
    @property
    def cross_sectional_area(self) -> float: ...

class RectangularExtrusion(Extrusion):
    def __init__(self, width: float, height: float, line: Line, profile_rotation: float = 0, *, material: Material = None, identifier: str = None) -> None: ...
    @property
    def width(self) -> float:
        """Width of the extrusion."""
    @property
    def height(self) -> float:
        """Height of the extrusion."""
    @property
    def cross_sectional_area(self) -> float:
        """Returns the area of the cross-section (width x height)."""
    @property
    def inner_volume(self) -> float:
        """Returns the inner volume of the extruded object."""

class SquareBeam(RectangularExtrusion):
    """
    High level object to create a rectangular beam object around the origin. The centroid of the beam is located at
    the origin (0, 0, 0).
    """
    def __init__(self, length_x: float, length_y: float, length_z: float, *, material: Material = None, identifier: str = None) -> None:
        """
        :param length_x: Width of the extrusion in x-direction.
        :param length_y: Length of the extrusion in y-direction.
        :param length_z: Height of the extrusion in z-direction.
        :param material: optional material
        :param identifier: object identifier (new in v14.10.0)
        """

class Pattern(Group):
    base_object: Incomplete
    def __init__(self, base_object: TransformableObject, duplicate_translation_list: list[list[float]], *, identifier: str = None) -> None:
        """
        Instantiates a pattern based on a base object and several duplicates, each translated by an input vector. If
        identifier has been set on the base-object, the identifiers of the objects within the pattern are suffixed with
        '-i' (i = 1, 2, 3, ...).

        :param base_object: the object to be duplicated
        :param duplicate_translation_list: a list of translation vectors, each of which generates a duplicate
        :param identifier: object identifier (new in v14.10.0)
        """

class LinearPattern(Pattern):
    def __init__(self, base_object: TransformableObject, direction: list[float], number_of_elements: int, spacing: float, *, identifier: str = None) -> None:
        """
        Instantiates a linear, evenly spaced, pattern along a single direction. If identifier has been set on the
        base-object, the identifiers of the objects within the pattern are suffixed with '-i' (i = 1, 2, 3, ...).

        :param base_object: the object to be duplicated
        :param direction: a unit vector specifying in which direction the pattern propagates
        :param number_of_elements: total amount of elements in the pattern, including the base object
        :param spacing: the applied spacing
        :param identifier: object identifier (new in v14.10.0)
        """

class BidirectionalPattern(Pattern):
    def __init__(self, base_object: TransformableObject, direction_1: list[float], direction_2: list[float], number_of_elements_1: int, number_of_elements_2: int, spacing_1: float, spacing_2: float, *, identifier: str = None) -> None:
        """
        Instantiates a two-dimensional pattern, evenly spaced in two separate directions. If identifier has been set on
        the base-object, the identifiers of the objects within the pattern are suffixed with '-i' (i = 1, 2, 3, ...).

        :param base_object: the object to be duplicated
        :param direction_1: a unit vector specifying the first direction
        :param direction_2: a unit vector specifying the second direction
        :param number_of_elements_1: total amount of elements along direction 1
        :param number_of_elements_2: total amount of elements along direction 2
        :param spacing_1: the applied spacing in direction 1
        :param spacing_2: the applied spacing in direction 2
        :param identifier: object identifier (new in v14.10.0)
        """

class Polygon(TransformableObject):
    points: Incomplete
    material: Incomplete
    def __init__(self, points: list[Point], *, surface_orientation: bool = False, material: Material = None, skip_duplicate_vertices_check: bool = False, identifier: str = None) -> None:
        """ 2D closed polygon without holes in x-y plane.

        :param points: profile is automatically closed, do not add start point at the end.
                       only the x and y coordinates are considered.
                       left hand rule around circumference determines surface direction
        :param surface_orientation:
                        - if True, the left hand rule around circumference determines surface direction
                        - if False, surface always in +z direction
        :param material: optional material
        :param skip_duplicate_vertices_check: if True, duplicate vertices are not filtered on serialization of the
            triangles. This may boost performance (default: False).
        :param identifier: object identifier (new in v14.10.0)

        :raises ValueError:
            - if less than 3 points are provided.
            - if points contains duplicates.
            - if points form a polygon with self-intersecting lines.
            - if points are all collinear.
        """
    def has_clockwise_circumference(self) -> bool:
        """
        Method determines the direction of the input points, and returns:
            - True if the circumference is clockwise
            - False if the circumference is counter-clockwise
        """
    @property
    def cross_sectional_area(self) -> float: ...
    @property
    def centroid(self) -> tuple[float, float]:
        """ Returns the centroid (X, Y) of the polygon. """
    @property
    def moment_of_inertia(self) -> tuple[float, float]:
        """ Returns the moment of inertia (Ix, Iy) in xy-plane. """
    def extrude(self, line: Line, *, profile_rotation: float = 0, material: Material = None, identifier: str = None) -> Extrusion:
        """ Extrude the Polygon in the direction of the given line.

        :param line: A line object is used to define the length (thickness) of the extrusion.
        :param profile_rotation: Rotation of the profile around the Z-axis in degrees.
        :param material: optional material
        :param identifier: object identifier (new in v14.10.0)
        """

class Polyline(TransformableObject):
    color: Incomplete
    def __init__(self, points: list[Point], *, color: Color = ..., identifier: str = None) -> None:
        """ Representation of a polyline made up of multiple straight line segments.

        This class is immutable, meaning that all functions that perform changes on a polyline will
        return a mutated copy of the original polyline.

        :param points: List of points, which may contain duplicate points. Note that when calling the individual
            `lines` of the polyline, duplicate points are filtered (i.e. zero-length lines are omitted).
        :param color: Visualization color ::version(v13.5.0).
        :param identifier: object identifier (new in v14.10.0)
        """
    @property
    def points(self) -> list[Point]: ...
    @classmethod
    def from_lines(cls, lines: Sequence[Line]) -> Polyline:
        """ Create a polyline object from a list of lines.

        The end of one line must always coincide with the start of the next line.

        :param lines: Sequence of lines
        """
    def is_equal_to(self, other: Polyline) -> bool:
        """ Check if all points in this polyline coincide with all points of another polyline

        :param other: Other polyline
        """
    @property
    def start_point(self) -> Point:
        """ First point in polyline.points """
    @property
    def end_point(self) -> Point:
        """ Last point in polyline.points """
    @property
    def lines(self) -> list[Line]:
        """ A list of lines connecting all polyline points. Lines between coincident points are skipped. """
    @property
    def x_min(self) -> float | None:
        """ The lowest x-coordinate present within this polyline. """
    @property
    def x_max(self) -> float | None:
        """ The highest x-coordinate present within this polyline. """
    @property
    def y_min(self) -> float | None:
        """ The lowest y-coordinate present within this polyline. """
    @property
    def y_max(self) -> float | None:
        """ The highest y-coordinate present within this polyline. """
    @property
    def z_min(self) -> float | None:
        """ The lowest z-coordinate present within this polyline. """
    @property
    def z_max(self) -> float | None:
        """ The highest z-coordinate present within this polyline. """
    def get_reversed_polyline(self) -> Polyline:
        """ Returns a polyline that is the reverse of this one. """
    def serialize(self) -> list[dict]:
        """ Return a json serializable dict of form:

        .. code-block:: python

            [
                {'x': point_1.x, 'y': point_1.y},
                {'x': point_2.x, 'y': point_2.y}
            ]

        """
    def filter_duplicate_points(self) -> Polyline:
        """
        Returns a new Polyline object. If two consecutive points in this polyline coincide,
        the second point will be omitted
        """
    def is_monotonic_ascending_x(self, strict: bool = True) -> bool:
        """ Check if the x coordinates of the points of this polyline are ascending.

        :param strict: when set to false, equal x coordinates are accepted between points
        """
    def is_monotonic_ascending_y(self, strict: bool = True) -> bool:
        """ Check if the y coordinates of the points of this polyline are ascending

        :param strict: when set to false, equal y coordinates are accepted between points
        """
    def intersections_with_polyline(self, other_polyline: Polyline) -> list[Point]:
        """
        Find all intersections with another polyline and return them ordered according to the direction of this polyline

        If the polylines are partly parallel, the start and end points of the parallel section will be returned as
        intersections. If one of the polylines is a subset of the other, or the two lines are completely parallel, no
        intersections will be found.

        :param other_polyline:
        """
    def intersections_with_x_location(self, x: float) -> list[Point]:
        """
        Find all intersections of this polyline with a given x location. Ordered from start to end of this polyline.

        If this line is partly vertical, the start and end points of the vertical section will be returned as an
        intersection. If this line is completely vertical, no intersections will be found.

        :param x:
        """
    def point_is_on_polyline(self, point: Point) -> bool:
        """ Check if a given point lies on this polyline

        :param point:
        """
    def get_polyline_between(self, start_point: Point, end_point: Point, inclusive: bool = False) -> Polyline:
        """
        Given two points that both lie on a polyline, return the polyline that lies between those two points
        start_point has to lie before end_point on this polyline.

        If the given start point lies after the given end point on this polyline, an empty polyline will be returned.
        If the two given points are identical, it depends on the inclusive flag whether a polyline containing that point
        once, or an empty polyline will be returned.

        :param start_point:
        :param end_point:
        :param inclusive: if true, the start and the end points will be added to the returned list
        :raises ValueError: when one of the two given points does not lie on this polyline
        """
    def find_overlaps(self, other: Polyline) -> list['Polyline']:
        """
        Find all overlapping regions of this polyline with another polyline. The returned overlapping regions will all
        point in the direction of this line. The overlap polylines will contain all points of both polylines, even if
        they only occur in one of the lines.

        If no overlaps are found, an empty list will be returned.

        :param other:
        """
    def combine_with(self, other: Polyline) -> Polyline:
        """
        Given two polylines that have at least one point in common and together form one line without any side branches,
        combine those two polylines. The combined line will contain all points of both polylines.

        :param other:
        """
    def split(self, point: Point) -> tuple['Polyline', 'Polyline']:
        """ return the two separate parts of this polyline before and after the given point.

        :param point:
        :raises ValueError: if the provided point does not lie on this polyline.
        """
    @classmethod
    def get_lowest_or_highest_profile_x(cls, profile_1: Polyline, profile_2: Polyline, lowest: bool) -> Polyline:
        """
        Given two polylines with n intersections, return a third polyline that will always follow the lowest
        (or highest) of the two lines the x locations of the points of the two polylines should be not descending
        (lines from left to right or vertical) the returned polyline will only cover the overlapping range in x
        coordinates.

        If one of the profiles is an empty polyline, an empty polyline will be returned.

        examples:

        .. code-block::

                                                 /----------------|
                                                /         /-------|--------------------
              profile_1: ----------------\\     /         /        |
                                          \\   /         /         |_____________________________
              profile_2:      -------------\\-/         /
                                            \\_________/

              get_lowest_or_highest_profile_x(cls, profile_1, profile_2, lowest=True) will return:


                                                         /-------|
                                                        /        |
                                                       /         |____________________
                 result:     -------------\\           /
                                           \\_________/


        Note that only the overlapping region of the two profiles is returned!

        :param profile_1:
        :param profile_2:
        :param lowest: switch to decide whether to return highest or lowest profile

        Currently, this implementation is exclusive. Meaning that vertical line parts that lie on the start or end of
        the overlap region in x are not taken into account.
        """

class Cone(TransformableObject):
    """ Creates a cone object. """
    material: Incomplete
    def __init__(self, diameter: float, height: float, *, origin: Point = None, orientation: Vector = None, material: Material = None, identifier: str = None) -> None:
        """
        :param diameter: Diameter of the circular base surface.
        :param height: Height from base to tip.
        :param origin: Optional location of the centroid of the base surface (default: Point(0, 0, 0)).
        :param orientation: Optional orientation from origin to the tip (default: Vector(0, 0, 1)).
        :param material: Optional material.
        :param identifier: object identifier (new in v14.10.0)
        """
    @classmethod
    def from_line(cls, diameter: float, line: Line, *, material: Material = None, identifier: str = None) -> Cone:
        """ Create a Cone object by a given base diameter and line.

        :param diameter: Diameter of the circular base surface.
        :param line: Line from base to top of the cone. The start point of the line represents the location of the
                     center of the base, and the end point represents the tip of the cone.
        :param material: Optional material.
        :param identifier: object identifier (new in v14.10.0)
        """

class Sphere(TransformableObject):
    """
    This class can be used to construct a spherical object around the specified coordinate.

    The smoothness of the edges can be altered by setting width_segments and height_segments. In the example below both
    the default smoothness of 30 (left) and a rough sphere with 5 segments (right) is shown:

    .. figure:: ../_static/sphere.png
            :width: 800px
            :align: center
    """
    centre_point: Incomplete
    radius: Incomplete
    width_segments: Incomplete
    height_segments: Incomplete
    material: Incomplete
    def __init__(self, centre_point: Point, radius: float, width_segments: float = 30, height_segments: float = 30, material: Material = None, *, identifier: str = None) -> None:
        """

        :param centre_point: Center point of the sphere.
        :param radius: Radius of the sphere.
        :param width_segments: Sets the smoothness in xz-plane.
        :param height_segments: Sets the smoothness in yz-plane.
        :param material: Optionally a custom material can be set.
        :param identifier: object identifier (new in v14.10.0)
        """
    def diameter(self) -> float: ...
    def circumference(self) -> float: ...
    def surface_area(self) -> float: ...
    def volume(self) -> float: ...

class Torus(Group):
    def __init__(self, radius_cross_section: float, radius_rotation_axis: float, rotation_angle: float = ..., *, material: Material = None, identifier: str = None) -> None:
        """
        Create a torus object

        :param radius_cross_section:
        :param radius_rotation_axis: measured from central axis to centre of cross-section.
        :param rotation_angle: optional argument to control how large of a torus section you want.
            2pi for complete torus
        :param material: optional material
        :param identifier: object identifier (new in v14.10.0)
        """
    @property
    def children(self) -> None:
        """:meta private:"""
    @property
    def inner_volume(self) -> float: ...
    @property
    def material(self) -> Material: ...
    @material.setter
    def material(self, value: Material) -> None: ...

class TriangleAssembly(TransformableObject):
    material: Incomplete
    def __init__(self, triangles: list[Triangle], *, material: Material = None, skip_duplicate_vertices_check: bool = False, identifier: str = None) -> None:
        """
        Fundamental visualisation geometry, built up from triangles.
        Right hand rule on triangle circumference determines the surface direction.

        :param triangles: Triangles of the assembly.
        :param material: optional material.
        :param skip_duplicate_vertices_check: if True, duplicate vertices are not filtered on serialization of the
            triangles. This may boost performance (default: False).
        :param identifier: object identifier (new in v14.10.0)
        """

class GeoPoint:
    """ Geographical point on the Earth's surface described by a latitude / longitude coordinate pair.

    This object can be created directly, or will be returned in the params when using a
    :class:`~viktor.parametrization.GeoPointField`.
    """
    lat: Incomplete
    lon: Incomplete
    def __init__(self, lat: float, lon: float) -> None:
        """
        :param lat: Latitude, between -90 and 90 degrees.
        :param lon: Longitude, between -180 and 180 degrees.
        """
    def __eq__(self, other: Any) -> bool: ...
    def __getitem__(self, key: str) -> float:
        """Enable subscript access by key.

        Supports:
        - Short keys: geo_point['lat'], geo_point['lon']
        - Long keys: geo_point['latitude'], geo_point['longitude']
        """
    @classmethod
    def from_rd(cls, coords: tuple[float, float]) -> GeoPoint:
        """ Instantiates a GeoPoint from the provided RD coordinates.

        :param coords: RD coordinates (x, y).
        """
    @property
    def rd(self) -> tuple[float, float]:
        """ RD representation (x, y) of the GeoPoint. """
    @property
    def latitude(self) -> float:
        """ ::version(v14.22.0) """
    @property
    def longitude(self) -> float:
        """ ::version(v14.22.0) """

class GeoPolyline:
    """ Geographical polyline on the Earth's surface described by a list of :class:`GeoPoints <GeoPoint>`.

    This object can be created directly, or will be returned in the params when using a
    :class:`~viktor.parametrization.GeoPolylineField`.
    """
    def __init__(self, *points: GeoPoint) -> None:
        """
        :param points: Geo points (minimum 2).
        """
    def __eq__(self, other: Any) -> bool: ...
    def __iter__(self) -> Iterator['GeoPoint']:
        """Enable direct iteration over points: for point in geo_polyline"""
    @property
    def points(self) -> list['GeoPoint']: ...

class GeoPolygon:
    """ Geographical polygon on the Earth's surface described by a list of :class:`GeoPoints <GeoPoint>`.

    This object can be created directly, or will be returned in the params when using a
    :class:`~viktor.parametrization.GeoPolygonField`.
    """
    def __init__(self, *points: GeoPoint) -> None:
        """
        :param points: Geo points (minimum 3). The profile is automatically closed, so it is not
            necessary to add the start point at the end.
        """
    def __eq__(self, other: Any) -> bool: ...
    def __iter__(self) -> Iterator['GeoPoint']:
        """Enable direct iteration over points: for point in geo_polygon"""
    @property
    def points(self) -> list['GeoPoint']: ...

class _Mesh(TransformableObject):
    material: Incomplete
    def __init__(self, vertices: list[list[float]], faces: list[list[int]], material: Material = None, *, identifier: str = None) -> None:
        """
        Fundamental visualisation geometry that can be constructed from a list of vertices and faces

        :param identifier: object identifier (new in v14.10.0)
        """
    @classmethod
    def from_obj(cls, file: TextIO, material: Material = None, *, identifier: str = None) -> _Mesh:
        """
        Alternative constructor to generate a Mesh object from .obj file. Method parses all vertices and faces into a
        single mesh object. Groups that may be present in the .obj file are not taken into account. If you require
        separate groups of meshes, a :class:`~.geometry._MeshAssembly` can be used instead.

        :param file: TextIO of the obj file to be parsed
        :param material: Material to be assigned to Mesh
        :param identifier: object identifier (new in v14.10.0)
        """

class _MeshAssembly(Group):
    def __init__(self, meshes: list[_Mesh], *, identifier: str = None) -> None:
        """
        Group of Mesh objects

        :param meshes: Mesh objects of the assembly.
        :param identifier: object identifier (new in v14.10.0)
        """
    @classmethod
    def from_obj(cls, file: TextIO, material_library: TextIO = None, default_material: Material = None, *, identifier: str = None) -> _MeshAssembly:
        '''
        Alternative constructor to generate a MeshAssembly object from .obj file. Groups defined in .obj file are taken
        into account an for each group a separate Mesh object is created and added as child of the MeshAssembly.

        Example usage:

        .. code-block:: python

            import viktor as vkt

            # using File object
            obj_file = vkt.File.from_path(Path(__file__).parent / "cube.obj")
            mtl_file = vkt.File.from_path(Path(__file__).parent / "cube.mtl")
            with obj_file.open_binary() as f1, mtl_file.open_binary() as f2:
                assembly = _MeshAssembly.from_obj(f1, f2)

            # using built-in `open()`
            with open(Path(__file__).parent / "cube.obj", "rb") as f1, open(Path(__file__).parent / "cube.mtl", "rb") as f2:
                assembly = _MeshAssembly.from_obj(f1, f2)

        :param file: TextIO of the obj file to be parsed
        :param material_library: TextIO of the corresponding material library
        :param default_material: Material to be assigned to Mesh if no material is found in the material library
        :param identifier: object identifier (new in v14.10.0)
        '''
