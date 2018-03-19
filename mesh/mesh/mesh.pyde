# Sample code for starting the mesh processing project
from classes import *

rotate_flag = True    # automatic rotation of model?
time = 0   # keep track of passing time, for automatic rotation
mesh = None
norm_toggle = False
white = False

# initalize stuff
def setup():
    size (600, 600, OPENGL)
    noStroke()

# draw the current mesh
def draw():
    global time, mesh
    
    background(0)    # clear screen to black

    perspective (PI*0.333, 1.0, 0.01, 1000.0)
    camera (0, 0, 5, 0, 0, 0, 0, 1, 0)    # place the camera in the scene
    scale (1, -1, 1)    # change to right-handed coordinate system
    
    # create an ambient light source
    ambientLight (102, 102, 102)
  
    # create two directional light sources
    lightSpecular (204, 204, 204)
    directionalLight (102, 102, 102, -0.7, -0.7, -1)
    directionalLight (152, 152, 152, 0, 0, -1)
    
    pushMatrix();

    fill (50, 50, 200)            # set polygon color
    ambient (200, 200, 200)
    specular (0, 0, 0)            # no specular highlights
    shininess (1.0)
  
    rotate (time, 1.0, 0.0, 0.0)

    # THIS IS WHERE YOU SHOULD DRAW THE MESH

    if mesh != None:
        for i in range(int(len(mesh.geo) / 3)):
            v0_i = mesh.geo[i * 3]
            v0 = mesh.verts[v0_i]
            v1_i = mesh.geo[i * 3 + 1]
            v1 = mesh.verts[v1_i]
            v2_i = mesh.geo[i * 3 + 2]
            v2 = mesh.verts[v2_i]
            fill(mesh.colors[i])
            if norm_toggle:
                beginShape()
                v0_n = mesh.v_n[v0_i]
                normal(v0_n.x, v0_n.y, v0_n.z)
                vertex(v0.x, v0.y, v0.z)
                
                v1_n = mesh.v_n[v1_i]
                normal(v1_n.x, v1_n.y, v1_n.z)
                vertex(v1.x, v1.y, v1.z)
                
                v2_n = mesh.v_n[v2_i]
                normal(v2_n.x, v2_n.y, v2_n.z)
                vertex(v2.x, v2.y, v2.z)
                endShape(CLOSE)
            else:
                f_n = mesh.f_n[i]
                
                beginShape()
                normal(f_n.x, f_n.y, f_n.z)
                vertex(v0.x, v0.y, v0.z)
                vertex(v1.x, v1.y, v1.z)
                vertex(v2.x, v2.y, v2.z)
                endShape(CLOSE)
    
    popMatrix()
    
    # maybe step forward in time (for object rotation)
    if rotate_flag:
        time += 0.02

# process key presses
def keyPressed():
    global rotate_flag, norm_toggle, mesh, white
    if key == ' ':
        rotate_flag = not rotate_flag
    elif key == '1':
        read_mesh ('tetra.ply')
    elif key == '2':
        read_mesh ('octa.ply')
    elif key == '3':
        read_mesh ('icos.ply')
    elif key == '4':
        read_mesh ('star.ply')
    elif key == '5':
        read_mesh ('torus.ply')
    elif key == 'n':
        # toggle per-Vector shading
        norm_toggle = not norm_toggle  
    elif key == 'r':
        # randomly color faces
        white = False
        mesh.randColors()
    elif key == 'w':
        # color faces white
        white = True
        mesh.white()
    elif key == 'd':
        # calculate the dual mesh
        dual()
    elif key == 'q':
        exit()

# read in a mesh file (THIS NEEDS TO BE MODIFIED !!!)
def read_mesh(filename):
    global mesh, white

    fname = "data/" + filename
    # read in the lines of a file
    with open(fname) as f:
        lines = f.readlines()
        
    # determine number of vertices (on first line)
    words = lines[0].split()
    num_vertices = int(words[1])
    print "number of vertices =", num_vertices

    # determine number of faces (on first second)
    words = lines[1].split()
    num_faces = int(words[1])
    print "number of faces =", num_faces
    
    mesh = Mesh()

    # read in the vertices
    for i in range(num_vertices):
        words = lines[i+2].split()
        x = float(words[0])
        y = float(words[1])
        z = float(words[2])
        print "Vector = ", x, y, z
        
        mesh.verts.append(Vector(x, y, z))
    
    # read in the faces
    for i in range(num_faces):
        j = i + num_vertices + 2
        words = lines[j].split()
        nverts = int(words[0])
        if nverts != 3:
            print "error: this face is not a triangle"
            exit()
        
        index1 = int(words[1])
        index2 = int(words[2])
        index3 = int(words[3])
        print "face =", index1, index2, index3
        
        mesh.geo.append(index1)
        mesh.geo.append(index2)
        mesh.geo.append(index3)
        
    construct()
        
def construct():
    global mesh, white
    # fill the opposites table
    mesh.opps = []
    for a in range(len(mesh.geo)):
        for b in range(len(mesh.geo)):
            a_n_v = mesh.verts[mesh.geo[c_n(a)]]
            a_p_v = mesh.verts[mesh.geo[c_p(a)]]
            b_n_v = mesh.verts[mesh.geo[c_n(b)]]
            b_p_v = mesh.verts[mesh.geo[c_p(b)]]
            if (Vector.eq_(a_n_v, b_p_v) and Vector.eq_(a_p_v, b_n_v)):
                mesh.opps.append(b)
                break
            
    # fill the face normals table
    mesh.f_n = []
    for i in range(len(mesh.geo) / 3):
        v0 = mesh.verts[mesh.geo[i * 3]]
        v1 = mesh.verts[mesh.geo[i * 3 + 1]]
        v2 = mesh.verts[mesh.geo[i * 3 + 2]]
        mesh.f_n.append(Vector.u_(Vector.cross_(Vector.sub_(v2, v0), Vector.sub_(v1, v0))))
    
    # fill the Vector normals table
    mesh.v_n = []
    for v in range(len(mesh.verts)):
        f_n_list = []
        for c in range(len(mesh.geo)):
            if mesh.geo[c] == v:
                f_n_list.append(mesh.f_n[int(c / 3)])
        v_n = Vector(0, 0, 0)
        for i in range(len(f_n_list)):
            v_n = Vector.add_(v_n, f_n_list[i])
        mesh.v_n.append(Vector.u_(v_n))
        
    # fill the color table
    if white:
        mesh.white()
    else:
        mesh.randColors()
        
def dual():
    global mesh
    
    print("Calculating dual... this may take awhile depending on complexity and depth")
    new_verts = []
    new_corns = []
    for v_ind in range(len(mesh.verts)):
        c_ind = 0
        while mesh.geo[c_ind] != v_ind:
            c_ind += 1
        centroids = []
        c_v = mesh.verts[mesh.geo[c_ind]]
        c_n_v = mesh.verts[mesh.geo[c_n(c_ind)]]
        c_p_v = mesh.verts[mesh.geo[c_p(c_ind)]]
        cen = centroid(c_v, c_n_v, c_p_v)
        centroids.append(cen)
        
        if vertInd(cen, new_verts) == -1:
            new_verts.append(cen)
            
        next = swing(c_ind)
        avg = centroids[0]
        while next != c_ind:
            c_v = mesh.verts[mesh.geo[next]]
            c_n_v = mesh.verts[mesh.geo[c_n(next)]]
            c_p_v = mesh.verts[mesh.geo[c_p(next)]]
            cen = centroid(c_v, c_n_v, c_p_v)
            centroids.append(cen)
            
            if vertInd(cen, new_verts) == -1:
                new_verts.append(cen)
            
            avg = Vector.add_(avg, cen)
            next = swing(next)
        avg = Vector.mult_(avg, 1.0 / len(centroids))
        new_verts.append(avg)
        
        cen_table = []
        for i in range(len(centroids)):
            cen_table.append(vertInd(centroids[i], new_verts))
        for i in range(len(centroids)):
            new_corns.append(len(new_verts) - 1)
            new_corns.append(cen_table[i])
            new_corns.append(cen_table[(i + 1) % len(centroids)])
    
    mesh = Mesh()
    mesh.verts = new_verts
    mesh.geo = new_corns
    construct()

def c_n(c):
    return int(c / 3) * 3 + (c + 1) % 3

def c_p(c):
    return c_n(c_n(c))

def centroid(v0, v1, v2):
    x = (v0.x + v1.x + v2.x) / 3.0
    y = (v0.y + v1.y + v2.y) / 3.0
    z = (v0.z + v1.z + v2.z) / 3.0
    return Vector(x, y, z)

def swing(c):
    return c_p(mesh.opps[c_p(c)])

def vertInd(v0, arr):
    for i in range(len(arr)):
        if Vector.eq_(v0, arr[i]):
            return i
    return -1