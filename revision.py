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

print(f"Resultados guardados en {output_file}")
print(f"Cantidad de archivos verificados correctamente: {verified_count}")

if not file_details:
    print("No se encontraron archivos con el formato esperado.")