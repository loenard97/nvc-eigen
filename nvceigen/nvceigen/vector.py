import numpy as np


class Vector3D:

    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z
    
    def __str__(self) -> str:
        return f"Vector3D <{self.x}, {self.y}, {self.z}>"

    def __repr__(self) -> str:
        return self.__str__()

    def __iter__(self):
        return (e for e in self.__dict__.values())

    def __add__(self, other) -> "Vector3D":
        """
        Add other to self
        """
        assert isinstance(other, Vector3D)

        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Vector3D(x, y, z)

    def __sub__(self, other) -> "Vector3D":
        """
        Subtract other from self
        """
        assert isinstance(other, Vector3D)
        
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Vector3D(x, y, z)

    def __mul__(self, scalar) -> "Vector3D":
        """
        Multiply with scalar factor
        """
        x = self.x * scalar
        y = self.y * scalar
        z = self.z * scalar
        return Vector3D(x, y, z)
    
    def __truediv__(self, scalar) -> "Vector3D":
        """
        Divide by scalar factor
        """
        x = self.x / scalar
        y = self.y / scalar
        z = self.z / scalar
        return Vector3D(x, y, z)

    @classmethod
    def unit_vector(cls, axis) -> "Vector3D":
        """
        Unit Vector along axis
        """
        if axis == 'x':
            return cls(1, 0, 0)
        
        if axis == 'y':
            return cls(0, 1, 0)
        
        if axis == 'z':
            return cls(0, 0, 1)
        
        raise ValueError('Axis has to be x, y or z')

    @property
    def length(self) -> float:
        """
        Length of Vector
        """
        return np.sqrt(np.power(self.x, 2) + np.power(self.y, 2) + np.power(self.z, 2))

    def normalize(self) -> "Vector3D":
        """
        Noramlize length of Vector
        """
        return self / self.length

    def rotate(self, u: "Vector3D", theta) -> "Vector3D":
        """
        Rotate around arbitrary axis
        :param Vector3D axis: Rotation axis (Vector3D of arbitrary length)
        :param float angle: Rotation angle in radians
        """
        u = u.normalize()

        cos = np.cos(theta)
        sin = np.sin(theta)

        x = (cos + np.power(u.x, 2)*(1-cos)) * self.x    + (u.x*u.y*(1-cos) - u.z*sin)      * self.y    + (u.x*u.z*(1-cos) + u.y*sin)      * self.z
        y = (u.y*u.x*(1-cos) + u.z*sin)      * self.x    + (cos + np.power(u.y, 2)*(1-cos)) * self.y    + (u.y*u.z*(1-cos) - u.x*sin)      * self.z
        z = (u.z*u.x*(1-cos) - u.y*sin)      * self.x    + (u.z*u.y*(1-cos) + u.x*sin)      * self.y    + (cos + np.power(u.z, 2)*(1-cos)) * self.z
        return Vector3D(x, y, z)

    def rotate_axis(self, axis: str, theta) -> "Vector3D":
        """
        Rotate around arbitrary axis
        :param str axis: Rotation axis x | y | z
        :param float angle: Rotation angle in radians
        """
        if axis == 'x':
            u = Vector3D.unit_vector('x')
        elif axis == 'y':
            u = Vector3D.unit_vector('y')
        elif axis == 'z':
            u = Vector3D.unit_vector('z')
        else:
            return ValueError('axis has to be x, y or z')
        u = u.normalize()

        cos = np.cos(theta)
        sin = np.sin(theta)

        x = (cos + np.power(u.x, 2)*(1-cos)) * self.x    + (u.x*u.y*(1-cos) - u.z*sin)      * self.y    + (u.x*u.z*(1-cos) + u.y*sin)      * self.z
        y = (u.y*u.x*(1-cos) + u.z*sin)      * self.x    + (cos + np.power(u.y, 2)*(1-cos)) * self.y    + (u.y*u.z*(1-cos) - u.x*sin)      * self.z
        z = (u.z*u.x*(1-cos) - u.y*sin)      * self.x    + (u.z*u.y*(1-cos) + u.x*sin)      * self.y    + (cos + np.power(u.z, 2)*(1-cos)) * self.z
        return Vector3D(x, y, z)

    def scalar_product(self, other) -> float:
        """
        Scalar Product between self and other
        """
        return self.x*other.x + self.y*other.y + self.z*other.z

    def cross_product(self, other) -> "Vector3D":
        """
        Cross Product between self and other
        """
        x = self.y*other.z - self.z*other.y
        y = self.z*other.x - self.x*other.z
        z = self.x*other.y - self.y*other.x
        return Vector3D(x, y, z)

    def angle(self, other) -> float:
        """
        Angle between self and other in radians
        """
        return np.arccos((self.x*other.x + self.y*other.y + self.z*other.z) / (self.length + other.length))

    def project(self, plane) -> "Vector3D":
        """
        Project self onto plane
        """
        if plane == 'xy':
            return Vector3D(self.x, self.y, 0)
        
        if plane == 'xz':
            return Vector3D(self.x, 0, self.z)
        
        if plane == 'yz':
            return Vector3D(0, self.y, self.z)
        
        raise ValueError('Plane has to be xy, xz or yz')
