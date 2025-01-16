
############################EJERCICIO2 PASO 1########################################
# Directorio
import os

directory = '/home/kevin.armada.7e4/PycharmProjects/Precipitaciones3/dat'


# verificar el formato del archivo
def check_file_format(filepath):
    try:
        with open(filepath, 'r') as file:
            # Leer las primeras líneas para verificar el formato
            header = file.readline()
            first_data_line = file.readline()

            # Verificar que el archivo no esté vacío y tenga al menos dos líneas (header y una línea de datos)
            if not header or not first_data_line:
                return False

            # Aquí puedes agregar más verificaciones basadas en el contenido específico de los archivos .dat
            return True
    except Exception as e:
        print(f"Error al leer el archivo {filepath}: {e}")
        return False


# Verificar todos los archivos en el directorio
all_files = os.listdir(directory)
incorrect_files = []
correct_files_count = 0
incorrect_files_count = 0

for filename in all_files:
    filepath = os.path.join(directory, filename)
    if filename.endswith('.dat') and check_file_format(filepath):
        correct_files_count += 1
    else:
        incorrect_files.append(filename)
        incorrect_files_count += 1

# Mostrar resultados
print(f"Archivos con formato correcto (.dat): {correct_files_count}")
print(f"Archivos con formato incorrecto: {incorrect_files_count}")
if incorrect_files:
    print(f"Archivos incorrectos: {incorrect_files}")
else:
    print("Todos los archivos tienen el formato correcto.")

############################EJERCICIO2 PASO 2########################################

import os
import pandas as pd

# Directorio de la carpeta con los archivos
directory = '/home/kevin.armada.7e4/PycharmProjects/Precipitaciones3/dat'

# Información esperada
expected_fields = [
    lambda x: x.startswith("P"),  # Identificador de la estación (ej: "P1")
    lambda x: isinstance(float(x), float),  # Latitud del punto de medición
    lambda x: isinstance(float(x), float),  # Longitud del punto de medición
    lambda x: isinstance(int(x), int),  # Altitud en metros del punto de medición
    lambda x: x == "geo",  # Tipo de dato
    lambda x: x == "2006",  # Año de inicio
    lambda x: x == "2100",  # Año de fin
    lambda x: x == "-1"  # Código para "sin datos"
]

# Función para verificar si un valor cumple con el formato esperado
def is_valid_field(field, validate_func):
    try:
        return validate_func(field)
    except:
        return False

# Función para leer y verificar las dos primeras líneas de un archivo
def read_and_verify_first_two_lines(filepath):
    try:
        with open(filepath, 'r') as file:
            lines = [file.readline().strip(), file.readline().strip()]
            if len(lines) < 2 or not lines[0] or not lines[1]:
                return False, lines
            # Verificar que cada campo está en el formato esperado
            fields = lines[1].split()  # Verificamos la segunda línea
            if len(fields) != len(expected_fields):
                return False, lines
            for i, field in enumerate(fields):
                if not is_valid_field(field, expected_fields[i]):
                    return False, lines
            return True, lines
    except Exception as e:
        print(f"Error al leer el archivo {filepath}: {e}")
        return False, []

# Verificar todos los archivos en el directorio
all_files = os.listdir(directory)
file_details = []
verified_count = 0

for idx, filename in enumerate(all_files, start=1):
    if filename.endswith('.dat'):
        filepath = os.path.join(directory, filename)
        is_valid, lines = read_and_verify_first_two_lines(filepath)
        if is_valid:
            verified_count += 1
        if lines[0] and lines[1]:
            file_details.append({
                'index': idx,
                'line1': lines[0],
                'line2': lines[1],
                'station_id': lines[1].split()[0],  # Extraer el identificador de estación
                'is_valid': is_valid
            })

# Ordenar los detalles por el identificador de la estación numéricamente
file_details = sorted(file_details, key=lambda x: int(x['station_id'][1:]))

# Guardar resultados en un archivo CSV para su revisión
output_file = 'file_validation_results.csv'
with open(output_file, 'w') as f:
    for details in file_details:
        f.write(f"{details['index']} - {details['line1']}\n{details['line2']}\n")

print("------------------------------------------------------------------------")
print(f"Resultados guardados en {output_file}")
print(f"Cantidad de archivos verificados correctamente: {verified_count}")

if not file_details:
    print("No se encontraron archivos con el formato esperado.")

############################EJERCICIO2 PASO 3########################################
import pandas as pd
print("------------------------------------------------------------------------")
# Ruta del archivo .dat
file_path = '/home/kevin.armada.7e4/PycharmProjects/Precipitaciones3/dat/precip.P1.MIROC5.RCP60.2006-2100.REGRESION.dat'


# Función para detectar errores en los datos
def detect_errors(filepath):
    try:
        # Leer el archivo utilizando pandas, ignorando líneas con un número incorrecto de campos
        df = pd.read_csv(filepath, sep='\s+', header=None, on_bad_lines='skip')

        # Asumimos que el archivo tiene las siguientes columnas:
        # Columna 0: Identificador
        # Columna 1: Latitud
        # Columna 2: Longitud
        # Columna 3: Altitud
        # Columna 4: Tipo de dato
        # Columna 5: Año de inicio
        # Columna 6: Año de fin
        # Columna 7: Código para "sin datos"

        # Nombrar las columnas
        df.columns = ['Identificador', 'Latitud', 'Longitud', 'Altitud', 'Tipo_de_dato', 'Año_de_inicio', 'Año_de_fin',
                      'Codigo_sin_datos']

        # Inicializar el diccionario de errores
        errors = {
            'identificador': [],
            'latitud': [],
            'longitud': [],
            'altitud': [],
            'tipo_de_dato': [],
            'año_de_inicio': [],
            'año_de_fin': [],
            'codigo_sin_datos': [],
            'missing_values': [],
        }

        # Verificar la consistencia de las columnas
        if not all(df['Identificador'].str.startswith('P')):
            errors['identificador'].append("Identificadores no válidos")

        if not pd.api.types.is_numeric_dtype(df['Latitud']) or (df['Latitud'] < -90).any() or (
                df['Latitud'] > 90).any():
            errors['latitud'].append("Latitudes fuera del rango -90 a 90")

        if not pd.api.types.is_numeric_dtype(df['Longitud']) or (df['Longitud'] < -180).any() or (
                df['Longitud'] > 180).any():
            errors['longitud'].append("Longitudes fuera del rango -180 a 180")

        if not pd.api.types.is_numeric_dtype(df['Altitud']) or (df['Altitud'] < 0).any():
            errors['altitud'].append("Altitudes negativas")

        if not all(df['Tipo_de_dato'] == 'geo'):
            errors['tipo_de_dato'].append("Tipos de dato no válidos")

        if not all(df['Año_de_inicio'] == 2006):
            errors['año_de_inicio'].append("Años de inicio diferentes de 2006")

        if not all(df['Año_de_fin'] == 2100):
            errors['año_de_fin'].append("Años de fin diferentes de 2100")

        if not all(df['Codigo_sin_datos'] == -1):
            errors['codigo_sin_datos'].append("Código para 'sin datos' diferente de -1")

        # Verificar valores faltantes o corruptos
        if df.isnull().values.any():
            errors['missing_values'].append("Valores faltantes en el archivo")

        # Imprimir errores encontrados
        for key, value in errors.items():
            if value:
                print(f"Errores en {key}: {value}")

        # Verificar si no hay errores
        if all(not value for value in errors.values()):
            print("No se encontraron errores en el archivo.")

    except Exception as e:
        print(f"Error al leer o verificar el archivo {filepath}: {e}")


# Detectar errores en el archivo especificado
detect_errors(file_path)