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
        self.center = PVector(x, y, z)
        self.radius = r
        
    def getNormal(self, v):
        diff = PVector.sub(v, self.center)
        return diff.normalize()
    
    # A ray O + St intersects a sphere A^2 + B^2 + C^2 = R^2 with center c
    # Project c - O (vector between O and c) onto ray to get a line segment going halfway through (S dot (c - O))
    # Use Pythag: proj^2 - (c - O)^2 = d^2 where d is distance between line segment and c at endpoint
    # Use Pythag: R^2 - d^2 = h^2 where h is the distance between the line segment endpoint and the edge of the sphere
    # (x - xc)^2 + (y - yc)^2 + (z - zc)^2 = R^2; (P - c) dot (P - c) - R^2 = 0
    # P = O + St; (O + St - c) dot (O + St - c) - R^2 = 0
    # (S dot S)t^2 + 2S(O - c)t + (O - c) dot (O - c) - R^2 = 0
    def intersectWith(self, ray):
        a = ray.slope.dot(ray.slope)
        b = 2 * ray.slope.dot(PVector.sub(ray.origin, self.center))
        c = (PVector.sub(ray.origin, self.center)).dot(PVector.sub(ray.origin, self.center)) - self.radius**2
        d = b**2 - 4 * a * c
        
        if d <= 0:
            return None
        else:
            return ray.pointAtT(min((-b + sqrt(d)) / (2 * a), (-b - sqrt(d)) / (2 * a)))
        
class Triangle(Intersectable):
    def __init__(self, surface, v0, v1, v2):
        super(Triangle, self).__init__(surface)
        self.vertices = [v0, v1, v2]
        self.n = (PVector.cross(PVector.sub(v1, v0), PVector.sub(v2, v1))).normalize()
        self.a = self.n.x
        self.b = self.n.y
        self.c = self.n.z
        self.d = PVector.dot(self.n, v0)
    
    def getNormal(self, v):
        return self.n
    
    def intersectWith(self, ray):
        numer = (PVector.dot(self.n, ray.origin) + self.d) * -1.0
        denom = PVector.dot(self.n, ray.slope)
        if denom <= 0:
            return None
        else:
            t = numer / denom
            p = ray.pointAtT(t)
            edges = [PVector.sub(self.vertices[1], self.vertices[0]),
                     PVector.sub(self.vertices[2], self.vertices[1]),
                     PVector.sub(self.vertices[0], self.vertices[2])]
            cs = [PVector.sub(p, self.vertices[0]),
                  PVector.sub(p, self.vertices[1]),
                  PVector.sub(p, self.vertices[2])]
            for i in range(0, 3):
                if PVector.dot(self.n, PVector.cross(edges[i], cs[i])) < 0:
                    return None
            return p
        
class Ray:
    def __init__(self, origin, slope):
        self.origin = origin
        self.slope = slope
        
    def pointAtT(self, t):
        return PVector.add(self.origin, PVector.mult(self.slope, t))
        
class Light:
    def __init__(self, x, y, z, r, g, b):
        self.origin = PVector(x, y, z)
        self.c = [r, g, b]