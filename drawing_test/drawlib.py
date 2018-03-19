# Drawing Routines, like OpenGL

from matlib import *

def gtOrtho(left, right, bottom, top, near, far):
    global proj, type
    type = "ortho"
    proj = ([[800 / (right - left), 0, 0, (-800 * left) / (right - left)],
              [0, 800 / (top - bottom), 0, (-800 * bottom) / (top - bottom)],
              [0, 0, 1, 0],
              [0, 0, 0, 1]])

def gtPerspective(fov, near, far):
    global type, ang
    type = "persp"
    ang = radians(fov)
    
def gtBeginShape():
    global verts
    verts = []

def gtEndShape():
    global verts, proj, ang
    for i in range(0, len(verts) / 2):
        if type == "ortho":
            new_v1, new_v2 = apply_mat(proj, verts[i * 2]), apply_mat(proj, verts[i * 2 + 1])
            line(new_v1[0], 800 - new_v1[1], new_v2[0], 800 - new_v2[1])
        elif type == "persp":
            v1, v2 = verts[i * 2], verts[i * 2 + 1]
            z1, z2 = v1[2], v2[2]
            x1, y1, x2, y2 = apply_persp(v1[0], z1), apply_persp(v1[1], z1), apply_persp(v2[0], z2), apply_persp(v2[1], z2)
            line(x1, 800 - y1, x2, 800 - y2)

def gtVertex(x, y, z):
    global verts
    if verts == None:
        print("No shape initialized.")
    else:
        verts.append(apply_mat(gtGetCtm(), [x, y, z, 1]))
        
def apply_mat(mat, v):
    new_v = [0, 0, 0, 1]
    for i in range(0, 3):
        for j in range(0, 4):
            new_v[i] += mat[i][j] * v[j]
    return new_v

def apply_persp(xy, z):
    global ang
    k = tan(ang / 2)
    xy1p = xy / abs(z)
    xy2p = (xy1p + k) * (800 / (2 * k))
    return xy2p