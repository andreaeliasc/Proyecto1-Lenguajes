### Disenio de Lenguajes de Programacion
### Andrea Estefania Elias Cobar
### Carnet 17048

### Programa que permite la traduccion de un AFN en forma de Nodo a un AFD en forma de Nodo (AFD)

### Se importan librerias para
### - Copy: Copiar listas para no tener conflicto de apuntar a una misma direccion de memoria para referencia
import copy

### Se importa el modulo Nodo para utilizar la estructura definida para nodos
from Nodo import Nodo

### Funcion para poder determinar si dentro de Dstates hay al menos un nodo NO MARCADO
def there_is_unmarked(Dstates):
    for i in Dstates:
        if i[1] == 0:
            return True
    return False

### Funcion para poder devolver el primer estado NO MARCADO dentro de Dstates
def return_first_unmarked(Dstates):
    for i in Dstates:
        if i[1] == 0:
            return i
    return False

### Funcion para poder obtener la lista de estados que almacena Dstates
def return_states_D(Dstates):
    estados = []
    for estado in Dstates:
        estados.append(estado[0])

    return estados

### Funcion para determinar si un conjunto de estados se encuenta dentro de Dstates (a manera de conjuntos)
def state_in_states(estado, Dstates):
    for Dstate in Dstates:
        if len(estado) == len(Dstate):
            keep = True
            for elemento in estado:
                if elemento not in Dstate:
                    keep = False
                    break
            if keep:
                return True
    return False

### Funcion que devuelve un estado especifico que contiene Dstates
def return_state_in_states(estado, Dstates):
    for Dstate in Dstates:
        if len(estado) == len(Dstate[0]):
            keep = True
            for elemento in estado:
                if elemento not in Dstate[0]:
                    keep = False
                    break
            if keep:
                return Dstate
    return False

### Funcion que permite la traduccion a un AFD a partir de la creacion de Subconjuntos (Dstates) y sus transiciones (Dtran)
def traduccionAFD(afn):
    Dstates = []
    Dtran = []
    contador = 0
    ### Unmarked = 0 | Marked = 1
    ### Estructura [EstadosAFN, Mark, EstadoAFD]
    Dstates.append([afn.cerraduraE(afn.estadoInicial), 0, contador])
    while there_is_unmarked(Dstates):
        ### Marcar un estado T
        estadoT = return_first_unmarked(Dstates)
        estadoT[1] = 1
        ### Ciclo para cada simbolo del Nodo
        simbolos = copy.deepcopy(afn.simbolos)
        if 'ε' in simbolos:
            simbolos.remove('ε')
        for simbolo in simbolos:
            ### Se hace la cerradura E a partir del move
            U = afn.cerraduraE(afn.move(estadoT[0], simbolo))
            ### Obtener los estados de U
            DOnlyStates = return_states_D(Dstates)
            nuevoEstado = []
            if U:
                if not state_in_states(U, DOnlyStates):
                    contador = contador + 1
                    nuevoEstado = [U, 0, contador]
                    Dstates.append([U, 0, contador])
                else:
                    nuevoEstado = return_state_in_states(U, Dstates)

                ### Agregar U a Dtran como una lista [estadoAFD, simboloTransicion, estadoAFD]
                Dtran.append([estadoT[2], simbolo, nuevoEstado[2]])

    return Dstates, Dtran

### Funcion que permite generar un AFD en forma de Nodo a partir de un AFN, Dstates y Dtran
def convertirAFDNodo(afn, Dstates, Dtran):
    nodo = Nodo('')

    ### Agregar simbolos de AFD
    simbolos = copy.deepcopy(afn.simbolos)

    if 'ε' in simbolos:
        simbolos.remove('ε')
    nodo.simbolos = simbolos

    ### Agregar estados de AFD
    for estado in Dstates:
        nodo.estados.append(estado[2])
    
    ### Agregar estados iniciales de AFD
    for estado in Dstates:
        for estadoInicial in afn.estadoInicial:
            if estadoInicial in estado[0]:
                nodo.estadoInicial.append(estado[2])

    ### Agregar estados finales de AFD
    for estado in Dstates:
        for estadoFinal in afn.estadosFinales:
            if estadoFinal in estado[0]:
                nodo.estadosFinales.append(estado[2])

    ### Agregar transiciones de AFD
    nodo.transiciones = copy.deepcopy(Dtran)

    return nodo


            
        
