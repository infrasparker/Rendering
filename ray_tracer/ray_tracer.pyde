# This is the starter code for the CS 3451 Ray Tracing project.
#
# The most important part of this code is the interpreter, which will
# help you parse the scene description (.cli) files.
from classes import *

def setup():
    size(500, 500) 
    noStroke()
    colorMode(RGB, 1.0)  # Processing color values will be in [0, 1]  (not 255)
    background(0, 0, 0)

# read and interpret the appropriate scene description .cli file based on key press
def keyPressed():
    if key == '1':
        interpreter("i1.cli")
    elif key == '2':
        interpreter("i2.cli")
    elif key == '3':
        interpreter("i3.cli")
    elif key == '4':
        interpreter("i4.cli")
    elif key == '5':
        interpreter("i5.cli")
    elif key == '6':
        interpreter("i6.cli")
    elif key == '7':
        interpreter("i7.cli")
    elif key == '8':
        interpreter("i8.cli")
    elif key == '9':
        interpreter("i9.cli")
        
def reset():
    global shapelist, fov, bgc, lightlist
    # reset data for new interpreter iteration
    print("Beginning to render... Process will take around 5 to 10 seconds.")
    shapelist = []
    fov = 60
    bgc = (0, 0, 0)
    lightlist = []

def interpreter(fname):
    global shapelist, fov, bgc, lightlist
    reset()
    fname = "data/" + fname
    # read in the lines of a file
    with open(fname) as f:
        lines = f.readlines()

    cvertexlist, csurface = None, None
    # parse each line in the file in turn
    for line in lines:
        words = line.split()  # split the line into individual tokens
        if len(words) == 0:   # skip empty lines
            continue
        if words[0] == 'sphere':
            # call your sphere creation routine here
            # for example: create_sphere(radius,x,y,z)
            if csurface == None:
                print("No surface initialized to apply to shape.")
            else:
                shapelist.append(Sphere(csurface, float(words[1]), float(words[2]), float(words[3]),
                                        float(words[4])))
        elif words[0] == 'fov':
            fov = float(words[1])
        elif words[0] == 'background':
            bgc = float(words[1]), float(words[2]), float(words[3])
        elif words[0] == 'light':
            lightlist.append(Light(float(words[1]), float(words[2]), float(words[3]),
                                   float(words[4]), float(words[5]), float(words[6])))
        elif words[0] == 'surface':
            csurface = Surface(float(words[1]), float(words[2]), float(words[3]),
                                   float(words[4]), float(words[5]), float(words[6]),
                                   float(words[7]), float(words[8]), float(words[9]),
                                   float(words[10]), float(words[11]))
        elif words[0] == 'begin':
            pass
            # if cvertexlist == None:
            #     cvertexlist = []
            # else:
            #     print("Error: attempting to initialize new shape before current shape is finished.")
        elif words[0] == 'vertex':
            pass
            # if cvertexlist == None:
            #     print("Error: attempting to add vertices to an uninitialized shape.")
            # else:
            #     cvertexlist.append(PVector(float(words[1]), float(words[2]), float(words[3])))
        elif words[0] == 'end':
            pass
            # if cvertexlist == None:
            #     print("Error: no shape initialized to add to shape list.")
            # else:
            #     if len(cvertexlist) != 3:
            #         print("Error: attempting to initialize non-triangular shape.")
            #     elif csurface == None:
            #         print("No surface initialized to apply to shape.")
            #     else:
            #         shapelist.append(Triangle(csurface, cvertexlist[0], cvertexlist[1], cvertexlist[2]))
            #         cvertexlist = None
        elif words[0] == 'write':
            render_scene()    # render the scene
            save(words[1])  # write the image to a file
            pass

# render the ray tracing scene
def render_scene():
    global shapelist, bgc
    for j in range(height):
        for i in range(width):
            # create an eye ray for pixel (i,j) and cast it into the scene
            # pix_color = color(0.8, 0.2, 0.4)  # you should calculate the correct pixel color here
            # set (i, j, pix_color)         # fill the pixel with the calculated color
            
            fovpass = tan(radians(fov / 2.0))
            ray = Ray(PVector(0.0, 0.0, 0.0), PVector((i - width / 2.0) * (fovpass / (width / 2.0)),
                                                (j - height / 2.0) * (fovpass / (height / 2.0)), -1.0))
            
            closest = None
            poi = None
            
            for s in shapelist:
                testPoint = s.intersectWith(ray)
                if (testPoint is not None) and ((poi is None) or
                                                PVector.dist(testPoint, ray.origin) < PVector.dist(poi, ray.origin)):
                    closest = s
                    poi = testPoint
            if closest is None:
                set(i, height - j, color(bgc[0], bgc[1], bgc[2]))
            else:
                set(i, height - j, rgbPixel(closest, ray, poi))
                    
def rgbPixel(object, ray, poi):
    global lightlist, shapelist, bgc
    r, g, b = 0, 0, 0
    n = object.getNormal(poi)
    surface = object.surface
    
    for l in lightlist:
        # lightray = Ray(l.origin, PVector.sub(poi, l.origin))
        lightray = Ray(poi, PVector.sub(l.origin, poi))
        lightIntersect = object.intersectWith(lightray)
        
        if lightIntersect != None:
            # if abs(PVector.dist(lightIntersect, poi)) < .0001:
            cost = max(lightray.slope.normalize().dot(n), 0)
            r += cost * surface.cdr * l.c[0]
            g += cost * surface.cdg * l.c[1]
            b += cost * surface.cdb * l.c[2]
    return color(r, g, b)
    

# should remain empty for this assignment
def draw():
    pass