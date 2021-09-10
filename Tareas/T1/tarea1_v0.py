# coding=utf-8
"""Tarea 1 Gonzalo Sobarzo"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import grafica.easy_shaders as es
import grafica.basic_shapes as bs
from grafica.gpu_shape import GPUShape, SIZE_IN_BYTES

# We will use 32 bits data, so floats and integers have 4 bytes
# 1 byte = 8 bits
SIZE_IN_BYTES = 4


# A class to store the application control
class Controller:
    fillPolygon = True


# we will use the global controller as communication with the callback function
controller = Controller()


def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

    else:
        print('Unknown key')
def createQuad(): #Creating the board with a white background and adding the black squares in a iterative way.
    # Defining locations and colors for each vertex of the shape
    #####################################
    background=[
         #posicion           Color
        -0.5, -0.5, 0.0,  1.0, 1.0, 1.0,
         0.5, -0.5, 0.0,  1.0, 1.0, 1.0,
         0.5,  0.5, 0.0,  1.0, 1.0, 1.0,
        -0.5,  0.5, 0.0,  1.0, 1.0, 1.0
    ]
    for x in range(0,4):
        background.extend([
        #      posicion                 Color
        -0.5+(0.25*x)  , 0.5-0.125, 0.0,  0.0, 0.0, 0.0,
        -0.375+(0.25*x), 0.5-0.125, 0.0,  0.0, 0.0, 0.0,
        -0.375+(0.25*x),  0.5     , 0.0,  0.0, 0.0, 0.0,
        -0.5+(0.25*x)  ,  0.5     , 0.0,  0.0, 0.0, 0.0
    ])
        background.extend([
        #         posicion                     Color
        -0.375+(0.25*x),  0.5-0.25  , 0.0,  0.0, 0.0, 0.0,
        -0.25+(0.25*x) ,  0.5-0.25  , 0.0,  0.0, 0.0, 0.0,
        -0.25+(0.25*x) ,  0.5-0.125 , 0.0,  0.0, 0.0, 0.0,
        -0.375+(0.25*x),  0.5-0.125 , 0.0,  0.0, 0.0, 0.0
    ])
        background.extend([
        #       posicion                       Color
        -0.5+(0.25*x)  ,  0.5-0.375, 0.0,  0.0, 0.0, 0.0,
        -0.375+(0.25*x),  0.5-0.375, 0.0,  0.0, 0.0, 0.0,
        -0.375+(0.25*x),  0.5-0.25 , 0.0,  0.0, 0.0, 0.0,
        -0.5+(0.25*x)  ,  0.5-0.25 , 0.0,  0.0, 0.0, 0.0
    ])
        background.extend([
        #              posicion                Color
        -0.375+(0.25*x),  0.5-0.5  , 0.0,  0.0, 0.0, 0.0,
        -0.25+(0.25*x) ,  0.5-0.5  , 0.0,  0.0, 0.0, 0.0,
        -0.25+(0.25*x) ,  0.5-0.375, 0.0,  0.0, 0.0, 0.0,
        -0.375+(0.25*x),  0.5-0.375, 0.0,  0.0, 0.0, 0.0
    ])   
        background.extend([
        #      posicion                Color
        -0.5+(0.25*x)  ,  0.5-0.625, 0.0,  0.0, 0.0, 0.0,
        -0.375+(0.25*x),  0.5-0.625, 0.0,  0.0, 0.0, 0.0,
        -0.375+(0.25*x),  0.5-0.5  , 0.0,  0.0, 0.0, 0.0,
        -0.5+(0.25*x)  ,  0.5-0.5  , 0.0,  0.0, 0.0, 0.0
    ])
        background.extend([
        #              posicion                 Color
        -0.375+(0.25*x),  0.5-0.75 , 0.0,  0.0, 0.0, 0.0,
        -0.25+(0.25*x) ,  0.5-0.75 , 0.0,  0.0, 0.0, 0.0,
        -0.25+(0.25*x) ,  0.5-0.625, 0.0,  0.0, 0.0, 0.0,
        -0.375+(0.25*x),  0.5-0.625, 0.0,  0.0, 0.0, 0.0
    ])
        background.extend([
        #      posicion                 Color
        -0.5+(0.25*x)  ,  0.5-0.875, 0.0,  0.0, 0.0, 0.0,
        -0.375+(0.25*x),  0.5-0.875, 0.0,  0.0, 0.0, 0.0,
        -0.375+(0.25*x),  0.5-0.75 , 0.0,  0.0, 0.0, 0.0,
        -0.5+(0.25*x)  ,  0.5-0.75 , 0.0,  0.0, 0.0, 0.0
    ])
        background.extend([
        #              posicion               Color
        -0.375+(0.25*x),  0.5-1.0  , 0.0,  0.0, 0.0, 0.0,
        -0.25+(0.25*x) ,  0.5-1.0  , 0.0,  0.0, 0.0, 0.0,
        -0.25+(0.25*x) ,  0.5-0.875, 0.0,  0.0, 0.0, 0.0,
        -0.375+(0.25*x),  0.5-0.875, 0.0,  0.0, 0.0, 0.0
    ])
    vertexData = np.array(background, dtype = np.float32) #The vertex info is stored in a array with the matrix called background and defining the dtype to np.float32

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    matriz=[] #empty matrix for storing the indexs of the vertexs
    m=0
    while m <=128: #total of vertexs and using the patern counter-clock wise
        matriz.extend([m,m+1,m+2,m+2,m+3,m])
        m+=4
    indices = np.array(matriz, dtype= np.uint32) #indexs in a array

    size = len(indices) 
    return bs.Shape(vertexData, indices) #returning bs.Shape for drawing   
def crear_dama(x,y,r,g,b,radius): 
    
    circle = []
    for angle in range(0,360,10):
        circle.extend([x, y, 0.0, r, g, b])
        circle.extend([x+np.cos(np.radians(angle))*radius, 
                       y+np.sin(np.radians(angle))*radius, 
                       0.0, r, g, b])
        circle.extend([x+np.cos(np.radians(angle+10))*radius, 
                       y+np.sin(np.radians(angle+10))*radius, 
                       0.0, r, g, b])
    
    return np.array(circle, dtype = np.float32)
def crear_grupo(): #Creating the 24 objects for the board using the numpy function append and crear_dama
    dama=np.array([],dtype = np.float32)
    for x in range(0,4): #In the same way of crear_tablero we use a for to add the cheeks to array
        dama=np.append(dama,crear_dama(-0.4375+(0.25*x),0.4375, 0.0, 1.0, 0.0, 0.05)) #First row of green cheeks 
        dama=np.append(dama,crear_dama(-0.3125+(0.25*x),0.4375-0.125, 0.0, 1.0, 0.0, 0.05))#Second row of green cheeks
        dama=np.append(dama,crear_dama(-0.4375+(0.25*x),0.4375-0.25, 0.0, 1.0, 0.0, 0.05)) #Third row of green cheeks
        dama=np.append(dama,crear_dama(-0.3125+(0.25*x),-0.4375, 0.0, 0.0, 1.0, 0.05))    #First row of blue cheeks
        dama=np.append(dama,crear_dama(-0.4375+(0.25*x),-0.4375+0.125, 0.0, 0.0, 1.0, 0.05)) #Second row of blue cheeks
        dama=np.append(dama,crear_dama(-0.3125+(0.25*x),-0.4375+0.25, 0.0, 0.0, 1.0, 0.05))  #Third row of blue cheeks
    return dama
window=None
if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Tarea 1", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)
    glfw.set_key_callback(window, on_key)
    
    # Creating our shader program and telling OpenGL to use it
    pipeline = es.SimpleShaderProgram()

    # Creating board in the GPU
    shape = createQuad()
    gpuShape = GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    
    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)
    dama=crear_grupo()
    # Defining shaders for our pipeline
    vertex_shader = """
    #version 330
    in vec3 position;
    in vec3 color;

    out vec3 newColor;
    void main()
    {
        gl_Position = vec4(position, 1.0f);
        newColor = color;
    }
    """

    fragment_shader = """
    #version 330
    in vec3 newColor;

    out vec4 outColor;
    void main()
    {
        outColor = vec4(newColor, 1.0f);
    }
    """

    # Binding artificial vertex array object for validation
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    # Assembling the shader program (pipeline) with both shaders
    shaderProgram = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))
    # Waiting to close the window
    while not glfw.window_should_close(window):
# Using GLFW to check for input events
        glfw.poll_events()
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClearColor(0.5,0.5, 0.5, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # OpenGL is told to use the simple shaderProgram
        glUseProgram(pipeline.shaderProgram)
        pipeline.drawCall(gpuShape) 
        vboDama = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vboDama)
        glBufferData(GL_ARRAY_BUFFER, len(dama) * SIZE_IN_BYTES, dama, GL_STATIC_DRAW)
        # Telling OpenGL to use our shader program
        glUseProgram(shaderProgram)
        glBindBuffer(GL_ARRAY_BUFFER, vboDama)
        position = glGetAttribLocation(shaderProgram, "position")
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(position)

        color = glGetAttribLocation(shaderProgram, "color")
        glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(color)
        # It renders a scene using the active shader program (pipeline) and the active VAO (shapes)
        glDrawArrays(GL_TRIANGLES, 0, int(len(dama)/6))
        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuShape.clear()
    # Getting events from GLFW
    glfw.terminate()