class Vector():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __repr__(self):
        return "V[" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + "]"

    def add_(v0, v1):
        return Vector(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)
        
    def sub_(v0 , v1):
        return Vector.add_(v0, Vector.mult_(v1, -1))

    def mult_(v, s):
        return Vector(v.x * s, v.y * s, v.z * s)

    def dot_(v0, v1):
        return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

    def cross_(v0, v1):
        return Vector(v0.y * v1.z - v0.z * v1.y, v0.z * v1.x - v0.x * v1.z, v0.x * v1.y - v0.y * v1.x)

    def dist_(v0, v1):
        return sqrt((v0.x - v1.x) ** 2 + (v0.y - v1.y) ** 2 + (v0.z - v1.z) ** 2)

    def mag_(v):
        return Vector.dist_(v, Vector(0, 0, 0))

    def u_(v):
        return Vector.mult_(v, 1 / Vector.mag_(v))
    
    def proj_(v0, v1):
        return Vector.mult_(v1, Vector.dot_(v0, v1) / (Vector.mag_(v1) ** 2))

    def eq_(v0, v1):
        return (abs(v0.x - v1.x) < .001 and abs(v0.y - v1.y) < .001 and abs(v0.z - v1.z) < .001)
        
class Mesh:
    def __init__(self):
        # Vertex list, indexed by number, storing Vertex.
        self.verts = []
        self.f_n = []
        self.v_n = []
        self.opps = []
        self.colors = []
        
        # Corner list, indexed by number, storing index of vertex.
        self.geo = []
    
    def getVertIndex(self, v):
        for i in range(len(self.verts)):
            if Vector.eq_(v, self.verts[i]):
                return i
        print("Could not find " + v + " in mesh.")

    def white(self):
        self.colors = []
        for i in range(len(self.geo) / 3):
            self.colors.append(color(255, 255, 255))
    
    def randColors(self):
        self.colors = []
        for i in range(len(self.geo) / 3):
            self.colors.append(color(random(255), random(255), random(255)))