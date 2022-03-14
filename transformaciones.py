import bpy

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
        bpy.ops.mesh.primitive_cube_add(size=0.5, location=(0, 0, 0))
        Activo.renombrar(objName)

    def crearEsfera(objName):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, 0, 0))
        Activo.renombrar(objName)

    def crearCono(objName):
        bpy.ops.mesh.primitive_cone_add(radius1=0.5, location=(0, 0, 0))
        Activo.renombrar(objName)
    
    def crearCilindro(objName):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=1, location=(0, 0, 0))
        Activo.renombrar(objName)

def crearRueda(x, y, nombre):
    Objeto.crearCilindro(nombre)
    Seleccionado.escalar((0.5, 0.5, 0.05))
    Seleccionado.rotarX(3.1415/2)
    Seleccionado.mover((0, y, 0))
    
    Objeto.crearCilindro('PerimetroRueda1')
    Seleccionado.escalar((0.6, 0.6, 0.05))
    Seleccionado.rotarX(3.1415/2)
    Seleccionado.mover((0, y+0.05, 0))
    
    Objeto.crearCilindro('PerimetroRueda2')
    Seleccionado.escalar((0.6, 0.6, 0.05))
    Seleccionado.rotarX(3.1415/2)
    Seleccionado.mover((0, y-0.05, 0))
    
    seleccionarObjetos(['PerimetroRueda1', 'PerimetroRueda2', nombre])
    bpy.ops.object.join()
    
'''************'''
''' M  A  I  N '''
'''************'''
if __name__ == "__main__":
    
    borrarObjetosExcepto(['Camera', 'Light'])
    Objeto.crearCilindro('Eje')
    Seleccionado.rotarX(3.1415/2)
    Seleccionado.escalar((0.15, 1, 0.15))
    
    crearRueda(0, 0.45, 'Rueda 1')
    
    
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
