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