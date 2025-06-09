import pandas as pd
import time

# --------- Configuración y carga de datos ---------
DATA_FILE = 'listado_abogados_programacion.xlsx'

def cargar_datos():
    try:
        df = pd.read_excel(DATA_FILE)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{DATA_FILE}'.")
        exit()
    return df

# Paso 1: Definir especialidades disponibles
especialidades = [
    "Derecho Civil", "Amparos de Salud", "Nuevas tecnologías", "Derecho Penal",
    "Derecho Tributario", "Derecho de Familia", "Derecho Laboral",
    "Derecho Internacional Público", "Derecho Internacional Privado",
    "Derecho Constitucional", "Derecho Administrativo", "Derecho Comercial",
    "Defensa del Consumidor", "Derechos de incidencia colectiva",
    "Derecho aduanero", "Derecho previsional"
]

# --------- Algoritmos de búsqueda y ordenamiento ---------
def busqueda_lineal(lista, elemento):
    # O(n)
    for i, v in enumerate(lista):
        if elemento.lower() in v.lower():
            return i
    return -1


def busqueda_binaria(lista, elemento):
    # O(log n), requiere lista ordenada
    izquierda, derecha = 0, len(lista) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        if lista[medio].lower() == elemento.lower():
            return medio
        elif lista[medio].lower() < elemento.lower():
            izquierda = medio + 1
        else:
            derecha = medio - 1
    return -1


def ordenamiento_burbuja(lista):
    # O(n^2)
    arr = lista.copy()
    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            if arr[j].lower() > arr[j+1].lower():
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr


def ordenamiento_seleccion(lista):
    # O(n^2)
    arr = lista.copy()
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j].lower() < arr[min_idx].lower():
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

# --------- Utilidades de interacción ---------
def get_choice(prompt, min_val, max_val):
    while True:
        try:
            choice = int(input(prompt))
            if choice < min_val or choice > max_val:
                raise ValueError
            return choice
        except ValueError:
            print(f"Debe seleccionar una opción entre {min_val} y {max_val}!")

# --------- Mostrar resultados ordenados automáticamente ---------
def mostrar_resultados(df, campo_valor, campo_nombre='Nombre'):
    if df.empty:
        print("No se encontraron resultados que coincidan con el filtro.")
        return

    # Preparar lista de nombres y mapeo a filas
    items = [(row[campo_nombre], row) for _, row in df.iterrows()]
    nombres = [nombre for nombre, _ in items]
    # Elegir algoritmo de ordenamiento según cantidad
    if len(nombres) < 50:
        nombres_ordenados = ordenamiento_burbuja(nombres)
    else:
        nombres_ordenados = ordenamiento_seleccion(nombres)
    # Imprimir resultados en orden alfabético
    print(f"Cantidad de letrados encontrados con el criterio seleccionado: {len(nombres_ordenados)}")
    print("Lista con los datos de contacto:")
    for idx, nombre in enumerate(nombres_ordenados, 1):
        # Recuperar fila original
        row = next(row for nom, row in items if nom == nombre)
        valor = row[campo_valor] if pd.notna(row[campo_valor]) else 'No especificado'
        telefono = row['Teléfono'] if pd.notna(row['Teléfono']) else 'No especificado'
        direccion = row['Dirección'] if pd.notna(row['Dirección']) else 'No especificado'
        etiqueta = campo_valor.replace('_', ' ')
        print(f"{idx}) {nombre} - {etiqueta}: {valor}\n   Tel: {telefono} | Dir: {direccion}")

# --------- Lógica de filtrado ---------
def filtrar_abogados(df):
    print("En base a qué parámetros desea filtrar:")
    print("1) Especialidad en el Derecho")
    print("2) Años de experiencia")
    print("3) Volumen de casos")
    print("4) Formación académica (posgrados)")
    filtro = get_choice("Seleccione una opción (1-4): ", 1, 4)

    if filtro == 1:
        for idx, esp in enumerate(especialidades, 1):
            print(f"{idx}) {esp}")
        seleccion = especialidades[get_choice(f"Ingrese número de 1 a {len(especialidades)}: ", 1, len(especialidades)) - 1]
        df_filtrado = df[df['Especialidad'] == seleccion]
        mostrar_resultados(df_filtrado, 'Especialidad')

    elif filtro == 2:
        min_exp = get_choice("Años mínimos de experiencia: ", 0, 100)
        df_filtrado = df[df['Años de experiencia'] >= min_exp]
        mostrar_resultados(df_filtrado, 'Años de experiencia')

    elif filtro == 3:
        min_casos = get_choice("Volumen mínimo de casos: ", 0, 10000)
        if 'Volumen de casos' in df.columns:
            df['Volumen de casos'] = pd.to_numeric(df['Volumen de casos'], errors='coerce').fillna(0)
            df_filtrado = df[df['Volumen de casos'] >= min_casos]
            df_filtrado = df_filtrado.sort_values(by='Volumen de casos', ascending=False)
            mostrar_resultados(df_filtrado, 'Volumen de casos')
        else:
            print("La columna 'Volumen de casos' no existe en el archivo.")

    else:
        posibles_columnas = [col for col in df.columns if 'posgrado' in col.lower() or 'formación' in col.lower()]
        if posibles_columnas:
            columna = posibles_columnas[0]
            print("¿Formación de posgrado en qué área del Derecho desea?")
            for idx, esp in enumerate(especialidades, 1):
                print(f"{idx}) {esp}")
            area = especialidades[get_choice(f"Seleccione área (1-{len(especialidades)}): ", 1, len(especialidades)) - 1]
            df_filtrado = df[df[columna].str.contains(area, case=False, na=False)]
            mostrar_resultados(df_filtrado, columna)
        else:
            print("No se encontró una columna de títulos de posgrado en los datos.")

# --------- Búsqueda automática y despedida ---------
def busqueda_automatica(df):
    nombres = df['Nombre'].dropna().tolist()
    palabra = input("\nIngrese nombre o parte del nombre para búsqueda automática: ")
    # Intentar búsqueda binaria en lista ordenada
    sorted_nombres = sorted(nombres)
    idx = busqueda_binaria(sorted_nombres, palabra)
    if idx != -1:
        print(f"Encontrado en posición {idx+1}: {sorted_nombres[idx]}")
    else:
        idx = busqueda_lineal(nombres, palabra)
        if idx != -1:
            print(f"Encontrado en posición {idx+1}: {nombres[idx]}")
        else:
            print("No se encontró el abogado.")

# --------- Ejecución principal ---------
if __name__ == "__main__":
    df = cargar_datos()
    if df.empty:
        print("No se encontraron datos en el archivo.")
        exit()

    filtrar_abogados(df)
    busqueda_automatica(df)
    print("\nGracias por utilizar el sistema de búsqueda de abogados.\n¡Hasta luego!")
