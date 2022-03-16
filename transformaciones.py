import bpy
import random

'''*********************************************************************'''
'''Funciones comunes útiles para selección/activación/borrado de objetos'''
'''*********************************************************************'''
def seleccionarObjetos(nombreObjetos): # Seleccionar un objeto por su nombre
    bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todos...
    for nombreObjeto in nombreObjetos:
        bpy.data.objects[nombreObjeto].select_set(True) # ...excepto el buscado

def activarObjeto(nombreObjeto): # Activar un objeto por su nombre
    bpy.context.scene.objects.active = bpy.data.objects[nombreObjeto]

def borrarObjeto(nombreObjeto): # Borrar un objeto por su nombre
    seleccionarObjeto(nombreObjeto)
    bpy.ops.object.delete(use_global=False)

def borrarObjetos(): # Borrar todos los objetos
    if(len(bpy.data.objects) != 0):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

def borrarObjetosExcepto(objetos):
    if(len(bpy.data.objects) != 0):
        bpy.ops.object.select_all(action='SELECT')
        for obj in objetos:
            bpy.data.objects[obj].select_set(False)
        bpy.ops.object.delete(use_global=False)
'''****************************************************************'''
'''Clase para realizar transformaciones sobre objetos seleccionados'''
'''****************************************************************'''
class Seleccionado:
    def mover(v):
        bpy.ops.transform.translate(
            value=v, constraint_axis=(True, True, True))

    def escalar(v):
        bpy.ops.transform.resize(value=v, constraint_axis=(True, True, True))

    def rotarX(v):
        bpy.ops.transform.rotate(value=v, orient_axis='X')

    def rotarY(v):
        bpy.ops.transform.rotate(value=v, orient_axis='Y')

    def rotarZ(v):
        bpy.ops.transform.rotate(value=v, orient_axis='Z')
    
    def cambiarColor(R, G, B):
        activeObject = bpy.context.active_object
        mat = bpy.data.materials.new("")
        activeObject.data.materials.append(mat)
        bpy.context.object.active_material.diffuse_color = (R, G, B, 1)

'''**********************************************************'''
'''Clase para realizar transformaciones sobre objetos activos'''
'''**********************************************************'''
class Activo:
    def posicionar(v):
        bpy.context.object.location = v

    def escalar(v):
        bpy.context.object.scale = v

    def rotar(v):
        bpy.context.object.rotation_euler = v

    def renombrar(nombreObjeto):
        bpy.context.object.name = nombreObjeto

'''**************************************************************'''
'''Clase para realizar transformaciones sobre objetos específicos'''
'''**************************************************************'''
class Especifico:
    def escalar(nombreObjeto, v):
        bpy.data.objects[nombreObjeto].scale = v

    def posicionar(nombreObjeto, v):
        bpy.data.objects[nombreObjeto].location = v

    def rotar(nombreObjeto, v):
        bpy.data.objects[nombreObjeto].rotation_euler = v

'''************************'''
'''Clase para crear objetos'''
'''************************'''
class Objeto:
    def crearCubo(objName):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
        Activo.renombrar(objName)

    def crearEsfera(objName):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 0))
        Activo.renombrar(objName)

    def crearCono(objName):
        bpy.ops.mesh.primitive_cone_add(radius1=1, location=(0, 0, 0))
        Activo.renombrar(objName)
    
    def crearCilindro(objName):
        bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=1, location=(0, 0, 0))
        Activo.renombrar(objName)

RADIO_EXT_RUEDA = 0.5
ANCHO_RUEDA = 0.05
RADIO_INT_RUEDA = RADIO_EXT_RUEDA - ANCHO_RUEDA
RADIO_EJE = 0.1
LARGO_EJE = 2
DISTANCIA_ENTRE_EJES = 3
POS_EXT_RUEDA = LARGO_EJE / 2 + ANCHO_RUEDA

def crearRueda(x, y, nombre, color):
    r, g, b = color
    
    Objeto.crearCilindro('PerimetroRueda1')
    Seleccionado.escalar((RADIO_EXT_RUEDA, RADIO_EXT_RUEDA, ANCHO_RUEDA))
    Seleccionado.rotarX(3.1415/2)
    Seleccionado.mover((0, y + ANCHO_RUEDA, 0))
    Seleccionado.cambiarColor(r, g, b)
    
    Objeto.crearCilindro('PerimetroRueda2')
    Seleccionado.escalar((RADIO_EXT_RUEDA, RADIO_EXT_RUEDA, ANCHO_RUEDA))
    Seleccionado.rotarX(3.1415/2)
    Seleccionado.mover((0, y - ANCHO_RUEDA, 0))
    Seleccionado.cambiarColor(r, g, b)
    
    Objeto.crearCilindro('CentroRueda')
    Seleccionado.escalar((RADIO_INT_RUEDA, RADIO_INT_RUEDA, ANCHO_RUEDA))
    Seleccionado.rotarX(3.1415/2)
    Seleccionado.mover((0, y, 0))
    Seleccionado.cambiarColor(b, g, r)
    
    seleccionarObjetos(['PerimetroRueda1', 'PerimetroRueda2', 'CentroRueda'])
    bpy.ops.object.join()
    Activo.renombrar(nombre)
    
    
def crearEje(x, y, nombre):
    Objeto.crearCilindro('Barra')
    Seleccionado.rotarX(3.1415/2)
    Seleccionado.escalar((RADIO_EJE, LARGO_EJE, RADIO_EJE))
    
    Objeto.crearEsfera('Amort1')
    Seleccionado.escalar((0.2, 0.2, 0.2))
    Seleccionado.mover((0, -LARGO_EJE / 4, 0))
    
    
    Objeto.crearEsfera('Amort2')
    Seleccionado.escalar((0.2, 0.2, 0.2))
    Seleccionado.mover((0, LARGO_EJE / 4, 0))
    
    seleccionarObjetos(['Barra', 'Amort1', 'Amort2'])
    bpy.ops.object.join()

    Activo.renombrar('Eje')
    
    Seleccionado.cambiarColor(0, 10, 0)
    
    crearRueda(0, POS_EXT_RUEDA, 'Rueda 1', (0, 0, 10))
    crearRueda(0, -POS_EXT_RUEDA, 'Rueda 2',  (0, 0, 10))
    
    
    seleccionarObjetos(['Eje', 'Rueda 1', 'Rueda 2'])
    
    bpy.ops.object.join()
    Activo.renombrar(nombre)
    
    Seleccionado.mover((x,y,0))
    
def crearChasis(x, y, z, nombre):
    Objeto.crearCubo('Viga1')
    Seleccionado.escalar((DISTANCIA_ENTRE_EJES * 1.5, 0.25, 0.25))
    Seleccionado.mover((0, LARGO_EJE / 4, 0))
    
    Objeto.crearCubo('Viga2')
    Seleccionado.escalar((DISTANCIA_ENTRE_EJES * 1.5, 0.25, 0.25))
    Seleccionado.mover((0, -LARGO_EJE / 4, 0))
    
    Objeto.crearCubo('Viga3')
    Seleccionado.escalar((0.25, ANCHO_RUEDA * 3 + LARGO_EJE, 0.25))
    Seleccionado.mover((-DISTANCIA_ENTRE_EJES + DISTANCIA_ENTRE_EJES / 4, 0, 0))
    
    Objeto.crearCubo('Viga4')
    Seleccionado.escalar((0.25, ANCHO_RUEDA * 3 + LARGO_EJE, 0.25))
    Seleccionado.mover((DISTANCIA_ENTRE_EJES - DISTANCIA_ENTRE_EJES / 4, 0, 0))
    
    seleccionarObjetos(['Viga1', 'Viga2', 'Viga3', 'Viga4'])
    bpy.ops.object.join()
    Activo.renombrar(nombre)
    
    Seleccionado.mover((x, y, z))
    Seleccionado.cambiarColor(20, 10, 0)


LARGO_LINK = 2.5
LARGO_LINK_1 = LARGO_LINK * 2

def crearBrazo(x, y, z, nombre):
    Objeto.crearCubo('Base')
    Seleccionado.escalar((LARGO_EJE / 2, LARGO_EJE / 2, 0.05))
    
    Objeto.crearEsfera('Joint0')
    Seleccionado.escalar((0.2, 0.2, 0.2))
    
    Objeto.crearCubo('Link1')
    Seleccionado.escalar((0.2, 0.2, LARGO_LINK_1 / 2))
    Seleccionado.mover((0, 0, LARGO_LINK_1 / 4))
    
    Objeto.crearEsfera('Joint1')
    Seleccionado.escalar((0.2, 0.2, 0.2))
    Seleccionado.mover((0, 0, LARGO_LINK_1 / 2))
    
    Objeto.crearCubo('Link2')
    Seleccionado.escalar((0.2, 0.2, LARGO_LINK / 2))
    Activo.rotar((0, 3.1415/2, 0))
    Seleccionado.mover((LARGO_LINK / 4, 0, LARGO_LINK_1 / 2))
    
    Objeto.crearEsfera('Joint2')
    Seleccionado.escalar((0.2, 0.2, 0.2))
    Seleccionado.mover((LARGO_LINK / 2, 0, LARGO_LINK_1 / 2))
    
    Objeto.crearCubo('Link4')
    Seleccionado.escalar((0.3, 0.3, LARGO_LINK / 2))
    Seleccionado.mover((LARGO_LINK / 2 + 0.2, 0, LARGO_LINK_1/ 2))
    
    Objeto.crearCubo('Link3')
    Seleccionado.escalar((0.2, 0.2, LARGO_LINK / 2))
    Seleccionado.mover((LARGO_LINK / 2 + 0.2, 0, LARGO_LINK_1/ 2 - LARGO_LINK / 4))
    
    Objeto.crearCono('Ventosa')
    Seleccionado.escalar((0.1, 0.1, 0.1))
    Seleccionado.mover((LARGO_LINK / 2 + 0.2, 0,  LARGO_LINK_1/ 2 - LARGO_LINK / 2))
    
    seleccionarObjetos(['Base','Joint0', 'Link1', 'Joint1', 'Link2', 'Joint2', 'Link3', 'Link4', 'Ventosa'])
    bpy.ops.object.join()
    Activo.renombrar(nombre)
    
    Seleccionado.mover((x, y, z))

def objetosDecorar(x, y, z, nombre):
    Objeto.crearCubo('Base')
    Seleccionado.escalar((LARGO_EJE / 2, LARGO_EJE / 2, 0.05))
    Seleccionado.cambiarColor(0, 0, random.randint(0, 20))
    
    for i in range (10):
        Objeto.crearCubo('Objeto')
        Seleccionado.escalar((0.1, 0.1, 0.1))
        a = round(random.uniform(-LARGO_EJE / 8, LARGO_EJE / 8), 2)
        b = round(random.uniform(-LARGO_EJE / 8, LARGO_EJE / 8), 2)
        
        if (i % 2 == 0):
            Seleccionado.cambiarColor(0, random.randint(0, 20), 0)
        else:
            Seleccionado.cambiarColor(random.randint(0, 20), 0, 0)
        Seleccionado.mover((a, b, 0.1))
        seleccionarObjetos(['Base', 'Objeto'])
        bpy.ops.object.join()
        Activo.renombrar('Base')
    
    Seleccionado.mover((x, y, z))
    Activo.renombrar(nombre)

'''************'''
''' M  A  I  N '''
'''************'''
if __name__ == "__main__":
    
    borrarObjetosExcepto(['Camera', 'Light'])
    crearEje(0, 0, 'Eje1')
    crearEje(DISTANCIA_ENTRE_EJES, 0, 'Eje2')
    
    crearChasis(DISTANCIA_ENTRE_EJES / 2, 0, 0.25, 'Chasis')
    crearBrazo( DISTANCIA_ENTRE_EJES / 4, 0, 0.40, 'hola')
    
    objetosDecorar(3 * DISTANCIA_ENTRE_EJES / 4, 0, 0.40, 'Bandeja')
    '''
    # Creación de un cubo y transformaciones de este:
    Objeto.crearCubo('MiCubo')
    Seleccionado.mover((0, 1, 2))
    Seleccionado.escalar((1, 1, 2))
    Seleccionado.escalar((0.5, 1, 1))
    Seleccionado.rotarX(3.1415 / 8)
    Seleccionado.rotarX(3.1415 / 7)
    Seleccionado.rotarZ(3.1415 / 3)

    # Creación de un cono y transformaciones de este:
    Objeto.crearCono('MiCono')
    Activo.posicionar((-2, -2, 0))
    Especifico.escalar('MiCono', (1.5, 2.5, 2))

    # Creación de una esfera y transformaciones de esta:
    Objeto.crearEsfera('MiEsfera')
    Especifico.posicionar('MiEsfera', (2, 0, 0))
    Activo.rotar((0, 0, 3.1415 / 3))
    Activo.escalar((1, 3, 1))
    '''
