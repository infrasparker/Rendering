# Devin Wu

time = 0   # use time to move objects from one frame to the next

def setup():
    size (800, 800, P3D)
    perspective (60 * PI / 180, 1, 0.1, 1000)  # 60 degree field of view
    
def draw():
    global time
    time += 0.01
    # camera (0, 0, 100, 0, 0, 0, 0, 1, 0)
    
    if time > 11:
        exit()

    if time < 2:
        camera (-50 - time * 45, -50, 100, time * -40, 0, 0, 0, 1, 0)  # position the virtual camera
    elif 2 <= time < 4:
        camera (-50 - time * 45, -50 + (2 - time) * 25, 100, time * -40, 0, 0, 0, 1, 0)
    elif 4 <= time < 5:
        camera (-100, -10, 100, -200, 0, 0, 0, 1, 0)
    elif 5 <= time < 6:
        camera (-120, -10, -40, -200, 0, -20 - (time - 6) * 10, 0, 1, 0)
    # elif 7 <= time < 9:
    #     camera (-120, -10, 40, -180, -60, 0, 0, 1, 0)
    # elif 15 <= time < 17:
    #     camera (-160, -60, -50, -180, 0, 0, 0, 1, 0)

    background (255, 255, 255)  # clear screen and set background to white
    
    # create a directional light source
    directionalLight(50, 50, 60, -1, 1, -1);
    lightSpecular(255, 255, 255)
    directionalLight (100, 100, 100, -0.3, 0.5, -1)
    
    noStroke()
    specular (180, 180, 180)
    shininess (15.0)
    
    fill (100, 100, 100)
    
    pushMatrix()
    
    if time < 5:
        translate(time * -40, -2, 1)
        tank(0, 0)
    elif 5 <= time < 6:
        translate(-200, -2, 1)
        tank(0, 0)
    elif 6 <= time < 7:
        translate(-200, -2, 1)
        tank((6 - time) * 30, 0)
    elif 7 <= time < 7.5:
        translate(-200, -2, 1)
        tank(-30, 0)
    elif 7.5 <= time < 8:
        translate(-200, -2, 1)
        tank(-30, (7.5 - time) * 60)
    elif 8 <= time < 8.5:
        translate(-200, -2, 1)
        tank(-30, -30)
    elif 8.5 <= time < 9.5:
        translate(-200, -2, 1)
        tank(-30, -30)
        pushMatrix()
        rotateY(-15 * PI /24)
        rotateX(PI/10)
        translate(1, -1, 8 + (time - 8.5) * 240)
        bullet()
        popMatrix()
    elif 9.2 <= time:
        translate(-200, -2, 1)
        tank(-30, -30)
        
    
    popMatrix()
    
    z = 80
    for x in [20, -80, -800, -600]:
        pushMatrix()
        translate(x, 0, z)
        if z == -50:
            z = 80
        else:
            z = -50
        apartment(-1)
        popMatrix()
    
    pushMatrix()
    translate(-400, 0, -50)
    if time < 9.2:
        apartment(-1)
    elif 9.2 <= time < 10.5:
        apartment(time - 9.2)
    popMatrix()
    
    pushMatrix()
    translate(200, 0, 0)
    for x in range(0, 10):
        translate(-100, 0, 0)
        roadPiece()
    popMatrix()
    
def bullet():
    fill(230, 230, 230)
    scale(1, 1, 1)
    cylinder()
    translate(0, 0, 1)
    sphere(1)
    
def apartment(t_f):
    for s in range(0, 4):
        rotateY(-PI/2)
        translate(-40, 0, 0)
        for i in range(0, 5):
            for j in range(0, 8):
                pushMatrix()
                if t_f == -1:
                    translate(i * 10, j * -15, 0)
                else:
                    if s == 0:
                        z_dis = 50 * t_f
                        x_dis = (t_f * (i - 2))
                    elif s == 1:
                        x_dis = 50 * t_f
                        z_dis = t_f * 10
                    elif s == 2:
                        z_dis = -80 * t_f
                        x_dis = (t_f * (i - 2))
                    elif s == 3:
                        x_dis = -50 * t_f
                        z_dis = t_f * 5
                    translate(i * 10 + x_dis, min(0, j * -15 - (15/6 * (j+1) - (t_f * 15 - 5)**2)), z_dis)
                apartmentPiece()
                popMatrix()
    
def apartmentPiece():
    fill(200, 255, 255)
    pushMatrix()
    translate(0, 0, 5)
    scale(6, 8, .5)
    box(1)
    popMatrix()
    
    fill(150, 150, 150)
    pushMatrix()
    scale(10, 15, 10)
    box(1)
    popMatrix()
    
def roadPiece():
    fill(75, 75, 75)
    pushMatrix()
    scale(100, .5, 50)
    box(1)
    popMatrix()
    
    fill(255, 255, 255)
    for x in range(0, 5):
        pushMatrix()
        translate(-40 + x * 20, -1, 0)
        scale(10, .5, 2)
        box(1)
        popMatrix()

def tank(swivel, rise):
    translate(0, 0, -8)
    pushMatrix()
    tread()
    popMatrix()
    translate(0, 0, 16)
    pushMatrix()
    tread()
    popMatrix()
    
    fill(100, 180, 225)
    
    translate(-2, -3, -8)
    pushMatrix()
    scale(22, 8, 14)
    box(1)
    popMatrix()
    
    fill(0, 255, 0)
    
    translate(0, -4, 0)
    pushMatrix()
    scale(6, 5, 6)
    sphere(1)
    popMatrix()
    
    fill(255, 255, 255)
    
    pushMatrix()
    rotateX(radians(rise))
    rotateY(PI/2 + radians(swivel))
    translate(0, -2, -5)
    scale(1, 1, 10)
    cylinder()
    popMatrix()
    
def tread():
    s = 2
    scale(s, s, s)
    translate(s * -.5 - s * 3, -s, 0)
    
    fill(20, 20, 20)
    
    pushMatrix()
    scale(1.2, 1.2, 1)
    cylinder()
    popMatrix()
    
    translate(s * .5, s, 0)
    for i in range(0, 5):
        cylinder()
        translate(s * 1.25, 0, 0)
    translate(-s * 1.25 + s * .5, -s, 0)
    pushMatrix()
    scale(1.2, 1.2, 1)
    cylinder()
    popMatrix()
    
    translate(-5.5, -1.1, 0)
    pushMatrix()
    scale(12, .25, 2)
    box(1)
    popMatrix()
    
    translate(0, 4, 0)
    pushMatrix()
    scale(10, .25, 2)
    box(1)
    popMatrix()
    
    translate(-6.75, -1.5, 0)
    pushMatrix()
    rotateZ(-PI/6)
    scale(.25, 3.5, 2)
    box(1)
    popMatrix()
    
    translate(12.5, 0, 0)
    pushMatrix()
    rotateZ(PI/6)
    scale(.25, 3.5, 2)
    box(1)
    popMatrix()
    

# cylinder with radius = 1, z range in [-1,1]
def cylinder(sides = 64):
    # first endcap
    beginShape()
    for i in range(sides):
        theta = i * 2 * PI / sides
        x = cos(theta)
        y = sin(theta)
        vertex ( x,  y, -1)
    endShape(CLOSE)
    # second endcap
    beginShape()
    for i in range(sides):
        theta = i * 2 * PI / sides
        x = cos(theta)
        y = sin(theta)
        vertex ( x,  y, 1)
    endShape(CLOSE)
    # sides
    x1 = 1
    y1 = 0
    for i in range(sides):
        theta = (i + 1) * 2 * PI / sides
        x2 = cos(theta)
        y2 = sin(theta)
        beginShape()
        normal (x1, y1, 0)
        vertex (x1, y1, 1)
        vertex (x1, y1, -1)
        normal (x2, y2, 0)
        vertex (x2, y2, -1)
        vertex (x2, y2, 1)
        endShape(CLOSE)
        x1 = x2
        y1 = y2