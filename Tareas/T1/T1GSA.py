# coding=utf-8
"""Dibujo de la letra E"""

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

# Se crear al figura de la letra E
def createQuad():

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
        #              posicion                      Color
        -0.375+(0.25*x),  0.5-0.25  , 0.0,  0.0, 0.0, 0.0,
        -0.25+(0.25*x) ,  0.5-0.25  , 0.0,  0.0, 0.0, 0.0,
        -0.25+(0.25*x) ,  0.5-0.125 , 0.0,  0.0, 0.0, 0.0,
        -0.375+(0.25*x),  0.5-0.125 , 0.0,  0.0, 0.0, 0.0
    ])
        background.extend([
        #      posicion                 Color
        -0.5+(0.25*x)  ,  0.5-0.375, 0.0,  0.0, 0.0, 0.0,
        -0.375+(0.25*x),  0.5-0.375, 0.0,  0.0, 0.0, 0.0,
        -0.375+(0.25*x),  0.5-0.25 , 0.0,  0.0, 0.0, 0.0,
        -0.5+(0.25*x)  ,  0.5-0.25 , 0.0,  0.0, 0.0, 0.0
    ])
        background.extend([
        #              posicion                      Color
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
        #              posicion                      Color
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
        #              posicion                      Color
        -0.375+(0.25*x),  0.5-1.0  , 0.0,  0.0, 0.0, 0.0,
        -0.25+(0.25*x) ,  0.5-1.0  , 0.0,  0.0, 0.0, 0.0,
        -0.25+(0.25*x) ,  0.5-0.875, 0.0,  0.0, 0.0, 0.0,
        -0.375+(0.25*x),  0.5-0.875, 0.0,  0.0, 0.0, 0.0
    ])
    vertexData = np.array(background, dtype = np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    matriz=[]
    m=0
    while m <=160:
        matriz.extend([m,m+1,m+2,m+2,m+3,m])
        m+=4
    indices = np.array(matriz, dtype= np.uint32)

    size = len(indices)
    return bs.Shape(vertexData, indices)
    
window=None
if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Tablero de Damas", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)
    
    # Creating our shader program and telling OpenGL to use it
    pipeline = es.SimpleShaderProgram()

    # Creating shapes on GPU memory
    shape = createQuad()
    gpuShape = GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    
    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # Se le dice a OpenGL que use el shaderProgram simple
        glUseProgram(pipeline.shaderProgram)
        pipeline.drawCall(gpuShape) # Se la letra

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuShape.clear()

    glfw.terminate()
