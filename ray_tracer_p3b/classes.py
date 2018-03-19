class Surface:
    def __init__(self, cdr, cdg, cdb, car, cag, cab, csr, csg, csb, p, krefl):
        self.cdr = cdr
        self.cdg = cdg
        self.cdb = cdb
        self.car = car
        self.cag = cag
        self.cab = cab
        self.csr = csr
        self.csg = csg
        self.csb = csb
        self.p = p
        self.krefl = krefl
        
class Intersectable(object):
    def __init__(self, surface):
        self.surface = surface

class Sphere(Intersectable):
    def __init__(self, surface, r, x, y, z):
        super(Sphere, self).__init__(surface)
        self.center = Vector(x, y, z)
        self.radius = r
        
    def getNormal(self, v):
        return Vector.unit(Vector.subtract(v, self.center))
    
    # A ray O + St intersects a sphere A^2 + B^2 + C^2 = R^2 with center c
    # Project c - O (vector between O and c) onto ray to get a line segment going halfway through (S dot (c - O))
    # Use Pythag: proj^2 - (c - O)^2 = d^2 where d is Vector.distance between line segment and c at endpoint
    # Use Pythag: R^2 - d^2 = h^2 where h is the Vector.distance between the line segment endpoint and the edge of the sphere
    # (x - xc)^2 + (y - yc)^2 + (z - zc)^2 = R^2; (P - c) dot (P - c) - R^2 = 0
    # P = O + St; (O + St - c) dot (O + St - c) - R^2 = 0
    # (S dot S)t^2 + 2S(O - c)t + (O - c) dot (O - c) - R^2 = 0
    def intersectWith(self, ray):
        a = Vector.dotProd(ray.slope, ray.slope)
        b = 2 * Vector.dotProd(ray.slope, Vector.subtract(ray.origin, self.center))
        c = Vector.dotProd(Vector.subtract(ray.origin, self.center), Vector.subtract(ray.origin, self.center)) - self.radius**2
        d = b**2 - 4 * a * c
        
        if d <= 0:
            return None
        else:
            return ray.pointAtT(min((-b + sqrt(d)) / (2 * a), (-b - sqrt(d)) / (2 * a)))
        
class Triangle(Intersectable):
    def __init__(self, surface, v0, v1, v2):
        super(Triangle, self).__init__(surface)
        self.vertices = [v0, v1, v2]
        self.n = Vector.scalar(Vector.unit(Vector.crossProd(Vector.subtract(v1, v0), Vector.subtract(v2, v1))), -1)
        self.a = self.n.x
        self.b = self.n.y
        self.c = self.n.z
        self.d = Vector.dotProd(self.n, v0)
    
    def __repr__(self):
        return "Triangle: <" + str(self.vertices[0]) + ", " + str(self.vertices[1]) + ", " + str(self.vertices[2]) + ">"
    
    def getNormal(self, v):
        return self.n
    
    def intersectWith(self, ray):
        v0 = self.vertices[0]
        v1 = self.vertices[1]
        v2 = self.vertices[2]
        
        numer = Vector.dotProd(Vector.subtract(v0, ray.origin), self.n)
        denom = Vector.dotProd(ray.slope, self.n)
        
        if denom == 0:
            return None

        p = ray.pointAtT(numer / denom)
        if p is not None:
            ab = Vector.subtract(v1, v0)
            cb = Vector.subtract(v1, v2)
            ap = Vector.subtract(p, v0)
            va = Vector.subtract(ab, Vector.project(ab, cb))
            
            bary_a = 1 - (Vector.dotProd(va, ap) / Vector.dotProd(va, ab))
            if bary_a < 0 or bary_a > 1:
                return None
            
            bc = Vector.subtract(v2, v1)
            ac = Vector.subtract(v2, v0)
            bp = Vector.subtract(p, v1)
            vb = Vector.subtract(bc, Vector.project(bc, ac))
            
            bary_b = 1 - Vector.dotProd(vb, bp) / Vector.dotProd(vb, bc)
            if bary_b < 0 or bary_b > 1:
                return None
            
            ca = Vector.subtract(v0, v2)
            ba = Vector.subtract(v0, v1)
            cp = Vector.subtract(p, v2)
            vc = Vector.subtract(ca, Vector.project(ca, ba))
            
            bary_c = 1 - Vector.dotProd(vc, cp) / Vector.dotProd(vc, ca)
            if bary_c < 0 or bary_c > 1:
                return None
            
            return p
        
class Vector():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __repr__(self):
        return "V[" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + "]"

    def addWith(v0, v1):
        return Vector(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)
        
    def subtract(v0 , v1):
        return Vector.addWith(v0, Vector.scalar(v1, -1))

    def scalar(v, s):
        return Vector(v.x * s, v.y * s, v.z * s)

    def dotProd(v0, v1):
        return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

    def crossProd(v0, v1):
        return Vector(v0.y * v1.z - v0.z * v1.y, v0.z * v1.x - v0.x * v1.z, v0.x * v1.y - v0.y * v1.x)

    def distance(v0, v1):
        return sqrt((v0.x - v1.x) ** 2 + (v0.y - v1.y) ** 2 + (v0.z - v1.z) ** 2)

    def magnitude(v):
        return Vector.distance(v, Vector(0, 0, 0))

    def unit(v):
        return Vector.scalar(v, 1 / Vector.magnitude(v))
    
    def project(v0, v1):
        return Vector.scalar(v1, Vector.dotProd(v0, v1) / (Vector.magnitude(v1) ** 2))
        
class Ray:
    def __init__(self, origin, slope):
        self.origin = origin
        self.slope = slope
        
    def pointAtT(self, t):
        if t >= 0:
            return Vector.addWith(self.origin, Vector.scalar(self.slope, t))
        return None
        
class Light:
    def __init__(self, x, y, z, r, g, b):
        self.origin = Vector(x, y, z)
        self.c = [r, g, b]