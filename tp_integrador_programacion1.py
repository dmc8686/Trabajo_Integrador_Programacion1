import random
import time

# Algoritmos de búsqueda
def busqueda_lineal(lista, elemento):
    comparaciones = 0
    tiempo_inicial = time.time() #registro del tiempo inicial
    for i in range(len(lista)):
        comparaciones += 1      #contador de comparaciones
        if lista[i] == elemento:  #comparacion elemento a elemento
            tiempo_final = time.time() #registro del tiempo final
            tiempo_empleado = tiempo_final-tiempo_inicial #calculo del tiempo empleado
            return i, comparaciones, tiempo_empleado
    tiempo_final = time.time()
    tiempo_empleado = tiempo_final-tiempo_inicial    #tiempo empleado en el caso de no encontrar objetivo
    return -1, comparaciones,tiempo_empleado

def busqueda_binaria(lista, elemento):
    comparaciones = 0 #contador de comparaciones
    izquierda, derecha = 0, len(lista) - 1 #inicializo los extremos de busqueda
    tiempo_inicial = time.time() #registro tiempo
    while izquierda <= derecha: #condicion de ciclo
        comparaciones += 1 #incremento comparaciones
        medio = (izquierda + derecha) // 2 #calculo la posicion media de la lista
        if lista[medio] == elemento: #pregunto si el valor del elemento del medio coincide con la busqueda
            tiempo_final = time.time()
            tiempo_empleado = tiempo_final-tiempo_inicial #calculo tiempo empleado
            return medio, comparaciones, tiempo_empleado
        elif lista[medio] < elemento: #en caso de que el valor de del elemento del medio sea menor
            izquierda = medio + 1   #modifico el extremo izquierdo del rango de busqueda
        else:
            derecha = medio - 1 #modifico el extremo derecho del rango de busqueda
    tiempo_final = time.time()
    tiempo_empleado = tiempo_final-tiempo_inicial #calculo el tiempo empleado
    return -1, comparaciones,tiempo_empleado

# Algoritmos de ordenamiento
def ordenamiento_de_burbuja(lista):
    n = len(lista) #obtengo el tamano de la lista
    operaciones = 0 #inicializo contador
    print('Lista original', lista)
    tiempo_inicial = time.time()#registra el tiempo inicial de la operacion
    for i in range(n):
        for j in range(0, n-i-1):
            operaciones += 1
            if lista[j] > lista[j+1]: #si el primero es mayor al adyacente
                lista[j], lista[j+1] = lista[j+1], lista[j] #intercambia posicion - metodo particular para python
        print(f"Paso {i+1}: {lista}")#muestro avance de ordenamiento
    tiempo_final = time.time()
    tiempo_empleado = tiempo_final-tiempo_inicial #calculo el tiempo empleado
    return lista, operaciones, tiempo_empleado

def ordenamiento_por_seleccion(lista):
    operaciones = 0
    tiempo_inicial = time.time() #registra el tiempo inicial de la operacion
    for i in range(len(lista)):#recorre la lista en toda su longitud
        minimo_posicion = i #toma la posicion minimo
        for j in range(i+1, len(lista)):#recorre el resto de la lista
            operaciones += 1 #incrementa contador
            if lista[minimo_posicion] > lista[j]:#pregunta si el valor de la posicion asignada como minimo es realmente menor
                minimo_posicion = j #cuando no lo es reasigna la posicion
        lista[i], lista[minimo_posicion] = lista[minimo_posicion], lista[i] #para luego cambiarla al lugar correcto 
        print(f"Paso {i+1}: {lista}")#muestro progreso
    tiempo_final = time.time()
    tiempo_empleado = tiempo_final-tiempo_inicial #calculo tiempo empleado   
    return lista, operaciones, tiempo_empleado

def crea_lista_numeros_aleatorios(tamano):
      #los numeros no se repiten
      lista = random.sample(range(1, tamano+1), tamano)  # Lista de números únicos sin repetir
      return lista

def menu_ordenamiento():
    while True:
            print("\nMENÚ ORDENAMIENTO")
            print("1. Ordenamiento de burbuja.")
            print("2. Ordenamiento por seleccion.")
            print("3. Salir")
            
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                #
                lista_ordenada, operaciones, tiempo_usado = ordenamiento_de_burbuja(lista_de_trabajo)
                print(f'El proceso de Ordenamiento de Burbuja realizo {operaciones} operaciones.')
                print(f'Ocupo un tiempo de {tiempo_usado}')
                print('La lista ordenada resultante es: ', lista_ordenada)

            elif opcion == "2":
                #
                lista_ordenada, operaciones, tiempo_usado = ordenamiento_por_seleccion(lista_de_trabajo)
                print(f'El proceso de Ordenamiento por Seleccion realizo {operaciones} operaciones.')
                print(f'Ocupo un tiempo de {tiempo_usado}')
                print('La lista ordenada resultante es: ', lista_ordenada)
                
            elif opcion == "3":
                break
            
            else:
                print("Opción no válida")

#menu busqueda
def menu_busqueda():
    while True:
            print("\nMENÚ BUSQUEDA")
            print("1. Búsqueda Lineal")
            print("2. Busqueda Binaria (requiere lista ordenada)")
            print("3. Salir")
            
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                ingreso = int(input('Ingrese un numero a buscar:'))
                posicion, comparaciones, tiempo_usado = busqueda_lineal(lista_ordenada,ingreso) #lista elemento
                if posicion == -1:
                    print(f'Elemento {ingreso} No encontrado. Tiempo: {tiempo_usado}')
                print(f'posicion {posicion}, comparaciones {comparaciones}, tiempo_usado {tiempo_usado}')
            
            elif opcion == "2":
                ingreso = int(input('Ingrese un numero a buscar:'))
                posicion, comparaciones, tiempo_usado = busqueda_binaria(lista_ordenada,ingreso) #lista elemento
                if posicion == -1:
                    print(f'Elemento {ingreso} No encontrado. Tiempo: {tiempo_usado}')
                print(f'posicion {posicion}, comparaciones {comparaciones}, tiempo_usado {tiempo_usado}')
            
            elif opcion == "3":
                break
            
            else:
                print("Opción no válida")    


# Menú principal
titulo = '''
##############################################
Bienvenidos al Tp Integrador de Programacion 1
##############################################
'''
print(titulo)
print('El programa trabajara con una lista desordenada.')
print('Ingrese el tamano de la lista con la que quiere trabajar: ')
tamano_lista = int(input())
lista_de_trabajo = crea_lista_numeros_aleatorios(tamano_lista)
lista_ordenada = lista_de_trabajo

while True:
    print("\nMENÚ PRINCIPAL")
    print("1. Algoritmos de Búsqueda")
    print("2. Algoritmos de Ordenamiento")
    print("m. Mostrar lista actual de trabajo")
    print("3. Salir")
    
    opcion = input("Seleccione una opción: ")
    
    if opcion == "1":
        menu_busqueda()
    elif opcion == "2":
        menu_ordenamiento()
    elif opcion == "m":
        print(lista_de_trabajo)
    elif opcion == "3":
        break
    else:
        print("Opción no válida")
