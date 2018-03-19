# Matrix Stack Library

# you should modify the routines below to complete the assignment

def gtInitialize():
    global stack
    i_matrix = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    stack = [i_matrix]

def gtPushMatrix():
    global stack
    stack.append(stack[len(stack) - 1])

def gtPopMatrix():
    global stack
    if len(stack) == 1:
        print("Cannot pop last matrix in stack.")
    else:
        stack.pop(len(stack) - 1)
    
def mult_4x4_mat(a, b):
    new_matrix = []
    for i in range(0, 4):
        new_row = []
        for j in range(0, 4):
            val = 0
            for k in range(0, 4):
                val += a[i][k] * b[k][j]
            new_row.append(val)
        new_matrix.append(new_row)
    return new_matrix
            

def gtTranslate(x, y, z):
    mat = [[1, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1]]
    stack[len(stack) - 1] = mult_4x4_mat(stack[len(stack) - 1], mat)

def gtScale(x, y, z):
    mat = [[x, 0, 0, 0], [0, y, 0, 0], [0, 0, z, 0], [0, 0, 0, 1]]
    stack[len(stack) - 1] = mult_4x4_mat(stack[len(stack) - 1], mat)

def gtRotateX(theta):
    theta = radians(theta)
    mat = [[1, 0, 0, 0], [0, cos(theta), -sin(theta), 0], [0, sin(theta), cos(theta), 0], [0, 0, 0, 1]]
    stack[len(stack) - 1] = mult_4x4_mat(stack[len(stack) - 1], mat)

def gtRotateY(theta):
    theta = radians(theta)
    mat = [[cos(theta), 0, sin(theta), 0], [0, 1, 0, 0], [-sin(theta), 0, cos(theta), 0], [0, 0, 0, 1]]
    stack[len(stack) - 1] = mult_4x4_mat(stack[len(stack) - 1], mat)

def gtRotateZ(theta):
    theta = radians(theta)
    mat = [[cos(theta), -sin(theta), 0, 0], [sin(theta), cos(theta), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    stack[len(stack) - 1] = mult_4x4_mat(stack[len(stack) - 1], mat)

def gtGetMatrix():
    pass

def print_ctm():
    print(stack[len(stack) - 1])