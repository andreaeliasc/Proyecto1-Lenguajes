### Disenio de Lenguajes de Programacion
### Andrea Estefania Elias Cobar
### Carnet 17048

### Programa Main que ejecuta las siguientes tareas:
### - Generar y simular un AFN dada una expresion y una cadena
### - Generar y simular un AFD dado un AFN y una cadena
### - Generar y simular un AFN Directo dada una expresion aumentada y una cadena
### - Generar y simular un AFN Minimizado dado un AFD y una cadena

### Se importan librerias para
### - Graphviz: Generacion de diagramas de automatas
### - Random: Generacion de documentos PDF con correlativos random para los diagramas
### - Copy: Copiar listas para no tener conflicto de apuntar a una misma direccion de memoria para referencia
from graphviz import Digraph
import random
import copy
from timeit import default_timer as timer
import time


### Se importan los distintos modulos creados para realizar las distintas tareas del proyecto
### - lectorExpresionesMejorado: Modulo Final Lector para traducir expresiones a una estructura de listas que se utilizará como arbol
### - traductorExpresion_a_AFN: Modulo para transformar una expresion dada (en la estructura de listas) a un AFN en forma de NODO
### - traductorAFN_a_AFD: Modulo para transformar un AFN en forma de NODO a un AFD en forma de NODO
### - traductorExpresion_a_AFD: Generacion de documentos PDF con correlativos random para los diagramas
### - traductorADF_a_AFDMinimizado: Copiar listas para no tener conflicto de apuntar a una misma direccion de memoria para referencia
### - simulaciones:

import lectorExpresionesMejorado
import traductorExpresion_a_AFN
import traductorAFN_a_AFD
import traductorExpresion_a_AFD
import simulaciones

### Se importa el modulo Nodo para utilizar la estructura definida para nodos
from Nodo import Nodo

### Iniciamos con las entradas del usuario
pasar = False

while not pasar:
    ### Ingreso de la expresion
    expresion = input('Ingrese su expresion: ')

    ### Ingreso de cadena de caracteres a evaluar
    cadena = input('Ingrese su input de caracteres a evaluar: ')
    cadena = cadena.replace(' ', '')

    ### Se convierte la expresion regular a una estructura de arbol (listas agrupadas)
    arbolExpresionRegular, pasar, mensaje = lectorExpresionesMejorado.conversionExpresionRegular('(' + expresion + ')')
    ### Se convierte la expresion regular aumentada a una estructura de arbol (listas agrupadas)
    arbolExpresionRegularAFD, pasar, mensaje = lectorExpresionesMejorado.conversionExpresionRegular('(' + expresion + ')#')

    if not pasar:
        print(mensaje)

#print(arbolExpresionRegularAFD)

###---------------------------------------------AFN---------------------------------------------###
### Se convierten los nodos que no son operandos en Nodos para almacenar
### Conjunto estados, transiciones, estado inicial, estado final
arbolNodosExpresionRegular, correlativo = traductorExpresion_a_AFN.traduccionBase(arbolExpresionRegular, 0)

### Uso de Thompson para generar un nodo final con el conjunto de estados, simbolos, transiciones, estado inicial y estados finales
afn, correlativo = traductorExpresion_a_AFN.traduccionAFN(arbolNodosExpresionRegular, correlativo, 0)

### Descomentar siguientes lineas para imprimir simbolos, estados, estado Inicial, estados finales y transiciones del AFN generado
#print(afn)
#print(afn.simbolos)
#print(afn.estados)
#print(afn.estadoInicial)
#print(afn.estadosFinales)
#print(afn.transiciones)

### Simulacion AFN
start = timer()

resultadoAFN = simulaciones.simulacionAFN(afn, cadena)
end = timer()

print(end-start)
if resultadoAFN:
    print(f"AFN: La cadena de caracteres ingresada \'{cadena}\' SI es parte del lenguaje generado por la expresion \'{expresion}\'")
else:
    print(f"AFN: La cadena de caracteres ingresada \'{cadena}\' NO es parte del lenguaje generado por la expresion \'{expresion}\'")

### Generar diagrama AFN
f = Digraph('Automata Finito No Determinista', filename='Automata Finito No Determinista'+str(random.random()))
f.attr(rankdir='LR', size='8,5')

f.attr('node', shape='doublecircle')
for estadoFinal in afn.estadosFinales:
    f.node(str(estadoFinal))

f.attr('node', shape='circle')
for estadoInicial in afn.estadoInicial:
    f.node(str(estadoInicial))

f.attr('node', shape='none')
f.node('')
for estadoInicial in afn.estadoInicial:
    f.edge('', str(estadoInicial), label='')

f.attr('node', shape='circle')
for transicion in afn.transiciones:
    f.edge(str(transicion[0]), str(transicion[2]), label=str(transicion[1]))

f.view()

###---------------------------------------------AFD---------------------------------------------###
### Creacion de subconjuntos para pasar de AFN -> AFD 
dStates, dTrans = traductorAFN_a_AFD.traduccionAFD(afn)

### Descomentar siguientes lineas para observar los estados (SUBCONJUNTOS) y transiciones generados a partir del AFN para el AFD
# print("-------------")
# print("Subconjuntos")
# print(dStates)
# print("-------------")
# print("Transiciones")
# print(dTrans)
# print("-------------")

### Creamos una estructura de Nodo para simular el AFD
afd = traductorAFN_a_AFD.convertirAFDNodo(afn, dStates, dTrans)

### Descomentar siguientes lineas para imprimir simbolos, estados, estado Inicial, estados finales y transiciones del AFD generado
# print(afd)
# print(afd.simbolos)
# print(afd.estados)
# print(afd.estadoInicial)
# print(afd.estadosFinales)
# print(afd.transiciones)

### Simulacion AFD
startAFD = timer()
resultadoAFD = simulaciones.simulacionAFD(afd, cadena)
endAFD = timer()

print(endAFD-startAFD)

print
if resultadoAFD:
    print(f"AFD: La cadena de caracteres ingresada \'{cadena}\' SI es parte del lenguaje generado por la expresion \'{expresion}\'")
else:
    print(f"AFD: La cadena de caracteres ingresada \'{cadena}\' NO es parte del lenguaje generado por la expresion \'{expresion}\'")

### Generar diagrama AFD
f = Digraph('Automata Finito Determinista', filename='Automata Finito Determinista'+str(random.random()))
f.attr(rankdir='LR', size='8,5')

f.attr('node', shape='doublecircle')
for estadoFinal in afd.estadosFinales:
    f.node(str(estadoFinal))

f.attr('node', shape='circle')
for estadoInicial in afd.estadoInicial:
    f.node(str(estadoInicial))

f.attr('node', shape='none')
f.node('')
for estadoInicial in afd.estadoInicial:
    f.edge('', str(estadoInicial), label='')

f.attr('node', shape='circle')
for transicion in afd.transiciones:
    f.edge(str(transicion[0]), str(transicion[2]), label=str(transicion[1]))

f.view()

###------------------------------------------AFD-DIRECTO----------------------------------------###
### Se hace una sustitucion previa para las expresiones 
arbolNodosExpresionRegularSustituido = traductorExpresion_a_AFD.sustitucionPrevia(arbolExpresionRegularAFD)

### Se convierten los nodos que no son operandos en Nodos para almacenar
### Conjunto estados, transiciones, estado inicial, estado final
### Aqui el arbol ya esta en modo nodos para procesarse los nodos Complejos
### Las correspondencias las tendremos guardadas para referencias de la construccion de subconjuntos
arbolNodosExpresionRegularAFD, _, correspondencias = traductorExpresion_a_AFD.traduccionBase(arbolNodosExpresionRegularSustituido, 1, [])

### Obtenemos los nodos hojas que ya poseen sus posiciones
nodosHoja = traductorExpresion_a_AFD.devolverNodosHoja(arbolNodosExpresionRegularAFD, [])

### Se realiza la definicion de nodos que no son hojas con sus operaciones nullable, firstpos, lastpos
nodoRoot, nodos = traductorExpresion_a_AFD.definirNodosAFD(arbolNodosExpresionRegularAFD, 0, [])

### Unimos los nodos en un solo arreglo
nodosFinales = nodosHoja + nodos

### Descomentar siguientes lineas para imprimir los Nodos del Arbol generados para el metodo de contruccion de AFD Directa
# print("---------------------------------------------")
# print("Posicion|Tipo Nodo|Nullable|Firstpos|Lastpos")
# for nodo in nodosFinales:
#     print(nodo.posicion,nodo.tipoNodo,nodo.nullable,nodo.firstpos,nodo.lastpos)
# print("---------------------------------------------")

### Se calcula la tabla de followpos con los nodosFinales resultantes
tablaFollowpos = traductorExpresion_a_AFD.followpos(nodosFinales, correspondencias)


### Descomentar siguientes lineas para imprimir la tabla Followpos creada en la construccion de AFD Directa
# print("---------------------------------------------")
# print("------------Followpos----------------")
# print(tablaFollowpos)
# print("---------------------------------------------")

### Obtener el conjunto de simbolos
simbolos = traductorExpresion_a_AFD.simbolosAFDDirecta(correspondencias)

### Obtener las transiciones y estados (el primer estado es el estado inicial)
dStatesAFD, dTransAFD  = traductorExpresion_a_AFD.traduccionAFDDirecta(nodoRoot, simbolos, tablaFollowpos, correspondencias)

### Posicion para determinar que estados son finales
posicionFinal = correspondencias[-1][1]

### Creamos una estructura de Nodo para simular el AFD
afdd = traductorExpresion_a_AFD.convertirAFDDirectaNodo(dStatesAFD, dTransAFD, simbolos, posicionFinal)

## Descomentar siguientes lineas para imprimir simbolos, estados, estado Inicial, estados finales y transiciones del AFD Directo generado
# print(afdd)
# print(afdd.simbolos)
# print(afdd.estados)
# print(afdd.estadoInicial)
# print(afdd.estadosFinales)
# print(afdd.transiciones)

### Simulacion AFD Directa
AFDDstart = timer()
resultadoAFDD = simulaciones.simulacionAFD(afdd, cadena)
AFDDend = timer()
print(AFDDend-AFDDstart)
if resultadoAFDD:
    print(f"AFD Directa: La cadena de caracteres ingresada \'{cadena}\' SI es parte del lenguaje generado por la expresion \'{expresion}\'")
else:
    print(f"AFD Directa: La cadena de caracteres ingresada \'{cadena}\' NO es parte del lenguaje generado por la expresion \'{expresion}\'")

### Generar diagrama AFD
f = Digraph('Automata Finito Determinista (Directa)', filename='Automata Finito Determinista (Directa)'+str(random.random()))
f.attr(rankdir='LR', size='8,5')

f.attr('node', shape='doublecircle')
for estadoFinal in afdd.estadosFinales:
    f.node(str(estadoFinal))

f.attr('node', shape='circle')
for estadoInicial in afdd.estadoInicial:
    f.node(str(estadoInicial))

f.attr('node', shape='none')
f.node('')
for estadoInicial in afdd.estadoInicial:
    f.edge('', str(estadoInicial), label='')

f.attr('node', shape='circle')
for transicion in afdd.transiciones:
    f.edge(str(transicion[0]), str(transicion[2]), label=str(transicion[1]))

f.view()


