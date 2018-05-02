"""
This is the geometric object cone

(renderable object)
"""

from ..geometry import Shape
from ..math import Ray, HitRecord, Vec3, dot3, G_EPSILON
from ..material import Material, PhongMaterial
from .bbox import BBox
from math import sqrt, pi, cos


class Cone(Shape):

    """The Cone class for raytracing"""

    def __init__(self, center: Vec3, direction: Vec3, theta: float, material: Material = PhongMaterial()) -> None:
        Shape.__init__(self, "Cone")

        self.center = center
        self.material = material
        self.direction = direction
        self.theta = theta

    def hit(self, ray: Ray, hitrecord: HitRecord) -> bool:
        """
        Hit ray with Cone.

        :param ray: the ray to check hit
        :param hitrecord: the hitrecord which is only valid if there is a hit
        :return: True if there is a hit
        """
        t0 = hitrecord.t

        # http://lousodrome.net/blog/light/2017/01/03/intersection-of-a-ray-and-a-cone/

        #a = dot3(ray.direction, ray.direction)
        a = dot3(ray.direction, self.direction) ** 2 - cos(self.theta) ** 2
        #b = dot3(ray.direction, (2.0 * (ray.start - self.center)))
        CO = ray.start - self.center
        b = 2 * ( dot3(ray.direction, self.direction) * dot3(CO, self.direction) - dot3(ray.direction, CO) * cos(self.theta)**2)
        #c = dot3(self.center, self.center) + dot3(ray.start, ray.start) \
        #   - 2.0 * dot3(ray.start,self.center) - self.radius * self.radius
        c = dot3(CO, self.direction)**2 - dot3(CO, CO)*cos(self.theta)**2
        D = b * b - (4.0) * a * c

        if D < G_EPSILON:
            return False

        D = sqrt(D)
        t = -0.5*(b + D) / a

        if t0 is not None and t0 < t:
            return False

        if t>0:
            hitrecord.t = t
            hitrecord.point = ray.start + t * ray.direction
            hitrecord.normal_g = (hitrecord.point - self.center)
            #v = (hitrecord.point - self.center)
            #hitrecord.normal_g = (-(v.y + v.z)/v.x, 1, 1)
            #hitrecord.normal_g = dot3(hitrecord.point, hitrecord.point) + (hitrecord.point - self.center) / (hitrecord.point - self.center)
            hitrecord.normal = hitrecord.normal_g
            hitrecord.color = Vec3(1., 1., 1.)  # cones don't have interpolated colors, set to white
            hitrecord.material = self.material
            return True
        return False


    def hitShadow(self, ray: Ray) -> bool:
        """
        :param ray:
        :param tmin:
        :param tmax:
        :return:
        """

        a = dot3(ray.direction, self.direction) ** 2 - cos(self.theta) * cos(self.theta)
        CO = ray.start - self.center
        b = 2 * (dot3(ray.direction, self.direction) * dot3(CO, self.direction) - dot3(ray.direction, CO) * cos(self.theta) **2 )
        c = dot3(CO, self.direction) ** 2 - dot3(CO, CO) * cos(self.theta)**2
        D = b * b - (4.0) * a * c

        if D < G_EPSILON:
            return False

        D = sqrt(D)
        t = -0.5 * (b + D) / a

        if t > 0:
            return True
        return False


    def getBBox(self):
        """
        Retrieve axis aligned bounding box of the cone


        :return: bounding box
        """
        bbmin = Vec3(self.center - Vec3(10,10,10))
        bbmax = Vec3(self.center + Vec3(10,10,10))
        return BBox(bbmin, bbmax)


    def getCentroid(self) -> Vec3:
        """
        Retrieve center of cone
        :return:
        """
        return self.center


    def getSurfaceArea(self):
        """
        Retrieve surface area

        :return: surface area
        """
        return 4. * pi * self.radius**2
        #return 4. * pi * 2