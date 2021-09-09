import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys

__author__ = "Ivan Sipiran"
__license__ = "MIT"

# We will use 32 bits data, so an integer has 4 bytes
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

def crear_tablero(): #creo fondo del tablero que sera blanco y sobrepongo cuadros negros intercalados
    background=[
         #posicion           Color
        -0.5, -0.5, 0.0,  1.0, 1.0, 1.0,
         0.5, -0.5, 0.0,  1.0, 1.0, 1.0,
         0.5,  0.5, 0.0,  1.0, 1.0, 1.0,
        -0.5,  0.5, 0.0,  1.0, 1.0, 1.0
    ]
    for x in range(0,3):
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
    return np.array(background,dtype = np.float32)  
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

    dama = crear_dama(0.5,0.0, 0.0, 1.0, 0.0, 0.1)
    tablero=crear_tablero()
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

    # Each shape must be attached to a Vertex Buffer Object (VBO)
    vboDama = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vboDama)
    glBufferData(GL_ARRAY_BUFFER, len(dama) * SIZE_IN_BYTES, dama, GL_STATIC_DRAW)
    vboTablero = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vboTablero)
    glBufferData(GL_ARRAY_BUFFER, len(tablero) * SIZE_IN_BYTES, tablero, GL_STATIC_DRAW)
    # Telling OpenGL to use our shader program
    glUseProgram(shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.5,0.5, 0.5, 1.0)

    glClear(GL_COLOR_BUFFER_BIT)

    glBindBuffer(GL_ARRAY_BUFFER, vboDama)
    position = glGetAttribLocation(shaderProgram, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)

    color = glGetAttribLocation(shaderProgram, "color")
    glVertexAttribPointer(color, 4, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)

    glBindBuffer(GL_ARRAY_BUFFER, vboTablero)
    position1 = glGetAttribLocation(shaderProgram, "position")
    glVertexAttribPointer(position1, 4, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position1)

    color1= glGetAttribLocation(shaderProgram, "color")
    glVertexAttribPointer(color1, 4, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(color1)
    # It renders a scene using the active shader program (pipeline) and the active VAO (shapes)
    glDrawArrays(GL_TRIANGLES, 0, int(len(tablero)/6))

    # Moving our draw to the active color buffer
    glfw.swap_buffers(window)

    # Waiting to close the window
    while not glfw.window_should_close(window):

        # Getting events from GLFW
        glfw.poll_events()
        
    glfw.terminate()