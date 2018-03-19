import math

WIDTH, HEIGHT = 500, 500
GRID_L, GRID_R = -3., 3.
GRID_B, GRID_T = -3., 3.

color_map = {
    -1: (0, 0, 0),
    0: (255, 0, 0),
    1: (255, 0, 0),
    2: (255, 0, 0),
    3: (255, 0, 0),
    4: (0, 255, 0),
    5: (0, 255, 0),
    6: (0, 255, 0),
    7: (0, 255, 0),
    8: (0, 0, 255),
    9: (0, 0, 255),
    10: (0, 0, 255),
    11: (0, 0, 255),
    12: (0, 0, 255)
    }

def setup():
    size(WIDTH, HEIGHT)
    
def draw():
    background(255, 255, 255)
    
    noStroke()
    fill(0,0,0)
    
    a, b = screen_to_grid(mouseX, mouseY)
    #a, b = .312, .576
    #a, b = .664, .336
    gen_fractal(0j, a + b * 1j, -1)
    
    
def gen_fractal(curr, v, pwr):
    if pwr < 12:
        c = color_map[pwr]
        fill(c[0], c[1], c[2])
        x, y = grid_to_screen(curr.real, curr.imag)
        ellipse(x, y, 10 - (pwr / 2), 10 - (pwr / 2))
        gen_fractal(curr + v ** (pwr + 1), v, pwr + 1)
        gen_fractal(curr - v ** (pwr + 1), v, pwr + 1)
        
        
        

        
        
def screen_to_grid(x, y): #converts pixel coordinates to relative coordinates
    return ((x * (GRID_R - GRID_L) / WIDTH) + GRID_L, -1 * ((y * (GRID_T - GRID_B) / HEIGHT) + GRID_B))

def grid_to_screen(x, y): #converts relative coordinates to pixel coordinates
    return ((x - GRID_L) * WIDTH / (GRID_R - GRID_L), (-y - GRID_B) * HEIGHT / (GRID_T - GRID_B))
    