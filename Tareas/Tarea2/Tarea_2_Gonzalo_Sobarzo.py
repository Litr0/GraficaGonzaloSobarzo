# coding=utf-8
"""Tarea 2 Gonzalo Sobarzo Avion modelo 1"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.scene_graph as sg
import grafica.easy_shaders as es
import grafica.lighting_shaders as ls
import grafica.performance_monitor as pm
from grafica.assets_path import getAssetPath

__author__ = "Ivan Sipiran"
__license__ = "MIT"

# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.showAxis = True
        self.viewPos = np.array([10,10,10])
        self.camUp = np.array([0, 1, 0])
        self.distance = 10


controller = Controller()

def setPlot(pipeline, mvpPipeline):
    projection = tr.perspective(45, float(width)/float(height), 0.1, 100)

    glUseProgram(mvpPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

    glUseProgram(pipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
    
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.9, 0.9, 0.9)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), 5, 5, 5)
    
    glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 1000)
    glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.001)
    glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.1)
    glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.01)

def setView(pipeline, mvpPipeline):
    view = tr.lookAt(
            controller.viewPos,
            np.array([0,0,0]),
            controller.camUp
        )

    glUseProgram(mvpPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)

    glUseProgram(pipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), controller.viewPos[0], controller.viewPos[1], controller.viewPos[2])
    

def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_LEFT_CONTROL:
        controller.showAxis = not controller.showAxis

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)
    
    elif key == glfw.KEY_1:
        controller.viewPos = np.array([controller.distance,controller.distance,controller.distance]) #Vista diagonal 1
        controller.camUp = np.array([0,1,0])
    
    elif key == glfw.KEY_2:
        controller.viewPos = np.array([0,0,controller.distance]) #Vista frontal
        controller.camUp = np.array([0,1,0])

    elif key == glfw.KEY_3:
        controller.viewPos = np.array([controller.distance,0,controller.distance]) #Vista lateral
        controller.camUp = np.array([0,1,0])

    elif key == glfw.KEY_4:
        controller.viewPos = np.array([0,controller.distance,0]) #Vista superior
        controller.camUp = np.array([1,0,0])
    
    elif key == glfw.KEY_5:
        controller.viewPos = np.array([controller.distance,controller.distance,-controller.distance]) #Vista diagonal 2
        controller.camUp = np.array([0,1,0])
    
    elif key == glfw.KEY_6:
        controller.viewPos = np.array([-controller.distance,controller.distance,-controller.distance]) #Vista diagonal 2
        controller.camUp = np.array([0,1,0])
    
    elif key == glfw.KEY_7:
        controller.viewPos = np.array([-controller.distance,controller.distance,controller.distance]) #Vista diagonal 2
        controller.camUp = np.array([0,1,0])
    
    else:
        print('Unknown key')

def createGPUShape(pipeline, shape):
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)

    return gpuShape

#NOTA: Aqui creas tu escena. En escencia, sólo tendrías que modificar esta función.
def createScene(pipeline): #agregando todas las figuras necesarias para el diseño del modelo
    detalle = createGPUShape(pipeline, bs.createColorSphereTarea2(0.5, 0.5, 0.5)) #tapas grises que van arriba de las alas y al frontis del avión
    chasis = createGPUShape(pipeline, bs.createColorConeTarea2(0.0,1.0,0.0))
    afirma = createGPUShape(pipeline, bs.createColorCylinderTarea2(1.0,1.0,1.0)) #cilindro que va entre las ruedas del avion
    ala = createGPUShape(pipeline, bs.createColorCubeTarea2(0.0,1.0,0.0))
    tapa = createGPUShape(pipeline, bs.createColorCylinderTarea2(0.0,1.0,0.0)) #cilindro que tapa la punta del cono para el chasis
    rueda = createGPUShape(pipeline, bs.createColorCylinderTarea2(0.5,0.5,0.5))
    sujeta = createGPUShape(pipeline, bs.createColorConeTarea2(0.905, 0.529, 0.137)) #conos que unen las ruedas al chasis
    helice = createGPUShape(pipeline, bs.createColorCubeTarea2(0.5,0.5,0.5))
    helice2 = createGPUShape(pipeline, bs.createColorCylinderTarea2(0.5,0.5,0.5)) #pieza que une la helice al chasis
    tubo = createGPUShape(pipeline, bs.createColorCylinderTarea2(0.905, 0.529, 0.137)) 
    ventana = createGPUShape(pipeline, bs.createColorSphereTarea2(0.5, 0.5, 0.5))
    estabilizadorh1 = createGPUShape(pipeline, bs.createColorConeTarea2(0.0,1.0,0.0)) 
    estabilizadorh2 = createGPUShape(pipeline, bs.createColorConeTarea2(0.0,1.0,0.0))
    estabilizadorv1 = createGPUShape(pipeline, bs.createColorConeTarea2(0.5,0.5,0.5))
    estabilizadorv2 = createGPUShape(pipeline, bs.createColorConeTarea2(0.5,0.5,0.5))

    estabilizadorh1Node = sg.SceneGraphNode('cone')
    estabilizadorh1Node.transform = tr.matmul([tr.translate(0.6, 0.5, 2.2) , tr.scale(0.3,0.01,0.3),tr.rotationZ((np.pi)/2)]) #se mueven y escalan los estabilizadores a la parte trasera del modelo
    estabilizadorh1Node.childs += [estabilizadorh1]

    estabilizadorh2Node = sg.SceneGraphNode('cone')
    estabilizadorh2Node.transform = tr.matmul([tr.translate(1.4, 0.5, 2.2) , tr.scale(0.3,0.01,0.3),tr.rotationZ(-(np.pi)/2)])
    estabilizadorh2Node.childs += [estabilizadorh2]

    estabilizadorv1Node = sg.SceneGraphNode('cone')
    estabilizadorv1Node.transform = tr.matmul([tr.translate(1.0, 0.9, 2.2) , tr.scale(0.01,0.3,0.3)])
    estabilizadorv1Node.childs += [estabilizadorv1]

    estabilizadorv2Node = sg.SceneGraphNode('cone')
    estabilizadorv2Node.transform = tr.matmul([tr.translate(1.0, 0.2, 2.3) , tr.scale(0.01,0.15,0.15),tr.rotationZ((np.pi))])
    estabilizadorv2Node.childs += [estabilizadorv2]
 
    VentanaNode = sg.SceneGraphNode('sphere')
    VentanaNode.transform = tr.matmul([tr.translate(1.0, 0.9, -0.1), tr.scale(0.2,0.2,0.02)]) #se pone en el medio del chasis el parabrisas del piloto
    VentanaNode.childs += [ventana]

    detalleNode = sg.SceneGraphNode('sphere')
    detalleNode.transform = tr.matmul([tr.translate(2.5, 1.6, -1.0), tr.scale(0.8,0.01,0.8)]) #circulo que va encima del ala
    detalleNode.childs += [detalle]

    SujetaNode = sg.SceneGraphNode('cone')
    SujetaNode.transform = tr.matmul([tr.translate(0.6, -0.5, -1.0) , tr.scale(0.01,0.5,0.5),tr.rotationZ((np.pi))]) #cono achatado que une la rueda al chasis
    SujetaNode.childs += [sujeta]

    SujetaNode2 = sg.SceneGraphNode('cone')
    SujetaNode2.transform = tr.matmul([tr.translate(1.4, -0.5, -1.0) , tr.scale(0.01,0.5,0.5),tr.rotationZ((np.pi))]) #cono achatado que une la rueda al chasis
    SujetaNode2.childs += [sujeta]

    detalle2Node = sg.SceneGraphNode('sphere')
    detalle2Node.transform = tr.matmul([tr.translate(-0.5, 1.6, -1.0), tr.scale(0.8,0.01,0.8)]) #circulo que va encima del ala
    detalle2Node.childs += [detalle]

    detalle3Node = sg.SceneGraphNode('sphere')
    detalle3Node.transform = tr.matmul([tr.translate(1.0, 0.5, -2.5), tr.scale(0.6,0.6,0.01)]) #circulo que va en el frontis del chasis
    detalle3Node.childs += [detalle]

    HeliceNode = sg.SceneGraphNode('helice')
    HeliceNode.transform = tr.matmul([tr.translate(1.0, 0.5, -2.8) , tr.scale(0.8,0.05,0.01),tr.rotationZ((np.pi)/4)]) #helice del avion
    HeliceNode.childs += [helice] 

    Helice2Node = sg.SceneGraphNode('cylinder')
    Helice2Node.transform = tr.matmul([tr.translate(1.0, 0.5, -2.5) , tr.scale(0.07,0.07,0.3),tr.rotationX((np.pi)/2)]) #cilindro que une la helice al chasis
    Helice2Node.childs += [helice2]

    TuboNode = sg.SceneGraphNode('cylinder')
    TuboNode.transform = tr.matmul([tr.translate(-1.0, 0.75, -1.8) , tr.scale(0.03,0.75,0.03)]) #tubos que unen las alas
    TuboNode.childs += [tubo]

    Tubo2Node = sg.SceneGraphNode('cylinder')
    Tubo2Node.transform = tr.matmul([tr.translate(-1.0, 0.75, -1.0) , tr.scale(0.03,0.75,0.03)])
    Tubo2Node.childs += [tubo]

    Tubo3Node = sg.SceneGraphNode('cylinder')
    Tubo3Node.transform = tr.matmul([tr.translate(3.0, 0.75, -1.0) , tr.scale(0.03,0.75,0.03)])
    Tubo3Node.childs += [tubo]

    Tubo4Node = sg.SceneGraphNode('cylinder')
    Tubo4Node.transform = tr.matmul([tr.translate(3.0, 0.75, -1.8) , tr.scale(0.03,0.75,0.03)])
    Tubo4Node.childs += [tubo]

    Tubo5Node = sg.SceneGraphNode('cylinder')
    Tubo5Node.transform = tr.matmul([tr.translate(3.0, 0.75, -1.8) , tr.scale(0.03,0.85,0.03)])
    Tubo5Node.childs += [tubo]

    Tubo6Node = sg.SceneGraphNode('cylinder')
    Tubo6Node.transform = tr.matmul([tr.translate(3.0, 0.75, -0.8) , tr.scale(0.03,0.85,0.03)])
    Tubo6Node.childs += [tubo]

    Tubo7Node = sg.SceneGraphNode('cylinder')
    Tubo7Node.transform = tr.matmul([tr.translate(3.0, 0.75, -1.8) , tr.scale(0.03,0.85,0.03)])
    Tubo7Node.childs += [tubo]

    Tubo8Node = sg.SceneGraphNode('cylinder')
    Tubo8Node.transform = tr.matmul([tr.translate(3.0, 0.75, -0.8) , tr.scale(0.03,0.85,0.03)])
    Tubo8Node.childs += [tubo]

    EnDiag=sg.SceneGraphNode('tubos en diagonal')
    EnDiag.transform=tr.matmul([tr.translate(-1.2,-1.8,0.3),tr.rotationZ((np.pi)/4)]) #nodo para poner en diagonal los tubos que van en diagonal como en el modelo
    EnDiag.childs += [Tubo5Node]
    EnDiag.childs += [Tubo6Node]

    EnDiag2=sg.SceneGraphNode('tubos en diagonal')
    EnDiag2.transform=tr.matmul([tr.translate(-1.0,2.5,0.3),tr.rotationZ(-(np.pi)/4)]) #nodo para poner en diagonal los tubos que van en diagonal como en el modelo pero hacia el lado opuesto
    EnDiag2.childs += [Tubo7Node]
    EnDiag2.childs += [Tubo8Node]
     
    Ala1Node = sg.SceneGraphNode('cube')
    Ala1Node.transform = tr.matmul([tr.translate(1.0, 0.0, -1.0) , tr.scale(2.5,0.1,1.0)]) #ala inferior
    Ala1Node.childs += [ala]

    Ala2Node = sg.SceneGraphNode('cube')
    Ala2Node.transform = tr.matmul([tr.translate(1.0, 1.5, -1.0) , tr.scale(2.5,0.1,1.0)]) #ala superior
    Ala2Node.childs += [ala]

    TapaNode = sg.SceneGraphNode('cylinder')
    TapaNode.transform = tr.matmul([tr.translate(1.0, 0.5, 1.9) , tr.scale(0.17,0.17,0.6),tr.rotationX((np.pi)/2)]) #cilindro que esconde la punta del cono que es el chasis
    TapaNode.childs += [tapa]

    AfirmaNode = sg.SceneGraphNode('cylinder')
    AfirmaNode.transform = tr.matmul([tr.translate(1.0, -1.0, -1.0) , tr.scale(0.5,0.05,0.05),tr.rotationZ((np.pi)/2)]) #cilindro que une las ruedas del avion
    AfirmaNode.childs += [afirma]

    RuedaNode = sg.SceneGraphNode('cylinder')
    RuedaNode.transform = tr.matmul([tr.translate(0.5, -1.0, -1.0) , tr.scale(0.1,0.4,0.4),tr.rotationZ((np.pi)/2)]) #rueda 1
    RuedaNode.childs += [rueda]

    RuedaNode2 = sg.SceneGraphNode('cylinder')
    RuedaNode2.transform = tr.matmul([tr.translate(1.5, -1.0, -1.0) , tr.scale(0.1,0.4,0.4),tr.rotationZ((np.pi)/2)]) #rueda 2
    RuedaNode2.childs += [rueda]
    
    ChasisNode = sg.SceneGraphNode('cone')
    ChasisNode.transform = tr.matmul([tr.translate(1.0, 0.5, 0.0) , tr.scale(0.7,0.7,2.5),tr.rotationX((np.pi)/2)]) #chasis del avion
    ChasisNode.childs += [chasis]
    
    avion = sg.SceneGraphNode('avion') #se anexan los hijos para crear el avion
    avion.childs += [ChasisNode]
    avion.childs += [detalleNode]
    avion.childs += [detalle2Node]
    avion.childs += [detalle3Node]
    avion.childs += [Ala1Node]
    avion.childs += [Ala2Node]
    avion.childs += [TapaNode]
    avion.childs += [RuedaNode]
    avion.childs += [RuedaNode2]
    avion.childs += [SujetaNode]
    avion.childs += [SujetaNode2]
    avion.childs += [AfirmaNode]
    avion.childs += [HeliceNode]
    avion.childs += [Helice2Node]
    avion.childs += [TuboNode]
    avion.childs += [Tubo2Node]
    avion.childs += [Tubo3Node]
    avion.childs += [Tubo4Node]
    avion.childs += [EnDiag]
    avion.childs += [EnDiag2]
    avion.childs += [VentanaNode]
    avion.childs += [estabilizadorh1Node]
    avion.childs += [estabilizadorh2Node]
    avion.childs += [estabilizadorv1Node]
    avion.childs += [estabilizadorv2Node]

    avion1 = sg.SceneGraphNode('avion1') #avion 1
    avion1.transform=tr.matmul([tr.translate(3.0,0.0,0.0),tr.uniformScale(0.5)])
    avion1.childs +=[avion]

    avion2 = sg.SceneGraphNode('avion2') #avion 2
    avion2.transform=tr.matmul([tr.translate(0.0,0.0,0.0),tr.uniformScale(0.5)])
    avion2.childs +=[avion]

    avion3 = sg.SceneGraphNode('avion3') #avion 3
    avion3.childs +=[avion]

    scene= sg.SceneGraphNode('system') #scene final 
    scene.childs += [avion1]
    scene.childs += [avion2]
    scene.childs += [avion3]    
    return scene
window=None
if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 800
    height = 800
    title = "Tarea 2"
    window = glfw.create_window(width, height, title, None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shader program (pipeline) with both shaders
    mvpPipeline = es.SimpleModelViewProjectionShaderProgram()
    pipeline = ls.SimpleGouraudShaderProgram()
    
    # Telling OpenGL to use our shader program
    glUseProgram(mvpPipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    cpuAxis = bs.createAxis(7)
    gpuAxis = es.GPUShape().initBuffers()
    mvpPipeline.setupVAO(gpuAxis)
    gpuAxis.fillBuffers(cpuAxis.vertices, cpuAxis.indices, GL_STATIC_DRAW)

    #NOTA: Aqui creas un objeto con tu escena
    dibujo = createScene(pipeline)

    setPlot(pipeline, mvpPipeline)

    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)

    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)

    while not glfw.window_should_close(window):

        # Measuring performance
        perfMonitor.update(glfw.get_time())
        glfw.set_window_title(window, title + str(perfMonitor))

        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        setView(pipeline, mvpPipeline)

        if controller.showAxis:
            glUseProgram(mvpPipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
            mvpPipeline.drawCall(gpuAxis, GL_LINES)

        HeliceRot=sg.findNode(dibujo,"helice") 
        HeliceRot.transform=tr.matmul([tr.translate(1.0, 0.5, -2.8) ,tr.rotationZ(glfw.get_time()*-20), tr.scale(0.8,0.05,0.01)]) #animacion para hacer rotar la helice
        avion1Node=sg.findNode(dibujo,"avion1")
        avion1Node.transform=tr.matmul([tr.translate(3.0,-np.sin(glfw.get_time())/2,0.0),tr.uniformScale(0.5),tr.rotationZ(np.sin( glfw.get_time())/4)]) #animacion para mover los 3 aviones de manera independiente
        avion2Node=sg.findNode(dibujo,"avion2")
        avion2Node.transform=tr.matmul([tr.translate(0.0,np.sin( glfw.get_time())/2,0.0),tr.uniformScale(0.5),tr.rotationZ(-np.sin( glfw.get_time())/4)]) 
        avion3Node=sg.findNode(dibujo,"avion3")
        avion3Node.transform=tr.matmul([tr.translate(-3.0,-np.cos( glfw.get_time())/2,0.0),tr.uniformScale(0.5),tr.rotationZ(np.cos( glfw.get_time())/4)])
        dibujo.transform=tr.matmul([tr.rotationY(np.pi),tr.translate(-1.0,0.0,0.0)]) #se ubican en el centro la escena completa y se rota 
        #NOTA: Aquí dibujas tu objeto de escena
        glUseProgram(pipeline.shaderProgram)
        sg.drawSceneGraphNode(dibujo, pipeline, "model")
        

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuAxis.clear()
    dibujo.clear()
    

    glfw.terminate()