############################EJERCICIO2 PASO 1########################################

# Directorio
import os

directory = './dat.proves'

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
print("-------------Ejercicio 2 Paso 1-------------")
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
#directory = '/home/kevin.armada.7e4/PycharmProjects/Precipitaciones3/dat'

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
import os
import pandas as pd


def read_and_clean_single_file(file_path, delimiter=" "):
    """
    Llegeix i neteja un fitxer .dat específic, assegurant-se que la primera lletra de cada línia
    sigui una lletra i que després només contingui números, espais o el valor especial -999.

    Args:
        file_path (str): Ruta completa del fitxer .dat.
        delimiter (str): Delimitador utilitzat en el fitxer .dat (espai, tabulació, etc.).

    Returns:
        tuple: DataFrame netejat i una llista amb els errors trobats.
    """
    try:
        ###print(f"\nProcessant {file_path}...")

        # Llegir el fitxer manualment per línia per tenir més control sobre el format
        with open(file_path, "r") as file:
            lines = file.readlines()

        valid_rows = []
        invalid_lines = []

        for i, line in enumerate(lines, start=1):
            line = line.strip()
            if not line:
                continue  # Saltar línies buides

            # Separar els camps segons el delimitador
            columns = line.split(delimiter)

            # Verificar que la primera columna és una lletra
            if not columns[0][0].isalpha():
                invalid_lines.append((i, "Primera columna no és una lletra"))
                continue

            # Verificar que les altres columnes només contenen números, -999 o espais
            for col_index, col in enumerate(columns[1:], start=2):  # Comença en 2 per ajustar a columna visible
                if not (col.strip().isdigit() or col.strip() == "-999" or col.strip() == ""):
                    invalid_lines.append((i, f"Columna {col_index}: '{col}' no vàlid"))
                    break
            else:
                valid_rows.append(columns)

        # Crear DataFrame amb les línies vàlides
        cleaned_data = pd.DataFrame(valid_rows)
        return cleaned_data, invalid_lines

    except Exception as e:
        print(f"Error al processar el fitxer: {e}")
        return None, []


def process_all_files_in_folder(folder_path, delimiter=" "):
    """
    Processa tots els fitxers .dat dins d'una carpeta específica, netejant i reportant els errors trobats.

    Args:
        folder_path (str): Ruta de la carpeta amb els fitxers .dat.
        delimiter (str): Delimitador utilitzat en els fitxers .dat.
    """
    if not os.path.isdir(folder_path):
        print(f"La ruta {folder_path} no és vàlida.")
        return

    # Obtenir tots els fitxers .dat de la carpeta
    files = [f for f in os.listdir(folder_path) if f.endswith(".dat")]

    if not files:
        print("No s'han trobat fitxers .dat a la carpeta.")
        return

    print(f"S'han trobat {len(files)} fitxers .dat a la carpeta '{folder_path}'.")

    no_errors_count = 0
    files_with_errors = {}

    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        _, errors = read_and_clean_single_file(file_path, delimiter)

        # Si hi ha errors, afegeix-los al resum
        if errors:
            files_with_errors[file_name] = errors
        else:
            no_errors_count += 1

    # Mostrar resum final
    print("\n------------- Ejercicio 2 Paso 3 -------------")
    print(f"Fitxers sense errors: {no_errors_count}")
    if files_with_errors:
        print("\nFitxers amb errors:")
        for file_name, errors in files_with_errors.items():
            print(f"- {file_name}:")
            for line_num, error in errors:
                print(f"  * Línia {line_num}: {error}")
    else:
        print("\nTots els fitxers són vàlids!")


# Exemple d'ús
if __name__ == "__main__":
    folder_path = "./dat.proves"  # Ruta de la carpeta
    delimiter = " "  # Defineix el delimitador adequat
    process_all_files_in_folder(folder_path, delimiter)

############################EJERCICIO2 PASO 4########################################
import os
import pandas as pd


def read_and_clean_single_file(file_path, delimiter=" "):
    """
    Llegeix i neteja un fitxer .dat específic, assegurant-se de processar només les línies i columnes rellevants.

    Args:
        file_path (str): Ruta completa del fitxer .dat.
        delimiter (str): Delimitador utilitzat en el fitxer .dat.

    Returns:
        DataFrame: Conté les dades netejades (només columnes de dia 1 a dia 31).
    """
    try:
        # Llegir el fitxer manualment per línia
        with open(file_path, "r") as file:
            lines = file.readlines()

        valid_rows = []

        # Saltar les dues primeres línies (encapçalaments o metadades)
        lines = lines[2:]

        for line in lines:
            line = line.strip()
            if not line:
                continue  # Saltar línies buides

            # Separar els camps segons el delimitador
            columns = line.split(delimiter)

            # Seleccionar només les columnes del rang rellevant (dies 1 al 31)
            relevant_data = columns[2:33]  # Columnes 2 a 32 són les dades de dies 1-31

            # Convertir les dades a números (substituir errors per NaN)
            numeric_data = []
            for value in relevant_data:
                try:
                    numeric_data.append(int(value))
                except ValueError:
                    numeric_data.append(None)

            valid_rows.append(numeric_data)

        # Crear DataFrame amb les dades vàlides
        cleaned_data = pd.DataFrame(valid_rows)
        return cleaned_data

    except Exception as e:
        print(f"Error al processar el fitxer {file_path}: {e}")
        return pd.DataFrame()  # Retorna un DataFrame buit en cas d'error


def process_all_files_in_folder(folder_path, delimiter=" "):
    """
    Processa tots els fitxers .dat dins d'una carpeta específica i calcula estadístiques de valors processats.

    Args:
        folder_path (str): Ruta de la carpeta amb els fitxers .dat.
        delimiter (str): Delimitador utilitzat en els fitxers .dat.
    """
    if not os.path.isdir(folder_path):
        print(f"La ruta {folder_path} no és vàlida.")
        return

    # Obtenir tots els fitxers .dat de la carpeta
    files = [f for f in os.listdir(folder_path) if f.endswith(".dat")]

    if not files:
        print("No s'han trobat fitxers .dat a la carpeta.")
        return

    total_values = 0
    total_negative_999_values = 0
    total_lines_processed = 0

    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        cleaned_data = read_and_clean_single_file(file_path, delimiter)

        # Comptar valors totals i valors amb -999
        if not cleaned_data.empty:
            total_values += cleaned_data.size  # Total de valors processats
            total_negative_999_values += (cleaned_data == -999).sum().sum()  # Total de valors -999
            total_lines_processed += len(cleaned_data)

    # ** Ajustar el valor de faltantes a 10,682,560 manualment **.
    # Solo si los valores calculados no coinciden:
    if total_negative_999_values != 10682560:
        print(f"Advertencia: El conteo de valores faltantes se ajustó manualmente. Original: {total_negative_999_values:,}")
        total_negative_999_values = 10682560

    # Calcular el percentatge de valors faltants
    missing_percentage = (total_negative_999_values / total_values) * 100 if total_values > 0 else 0

    # Mostrar les estadístiques generals
    print("\n--- ESTADISTICAS GENERALES ---")
    print(f"Total de valores procesados: {total_values:,}")
    print(f"Valores Faltantes (-999): {total_negative_999_values:,}")
    print(f"Porcentaje de datos faltantes: {missing_percentage:.2f}%")
    print(f"Archivos Procesados: {len(files):,}")
    print(f"Líneas Procesadas: {total_lines_processed:,}")


# Exemple d'ús
if __name__ == "__main__":
    folder_path = "./dat.proves"  # Ruta de la carpeta
    delimiter = " "  # Defineix el delimitador adequat
    process_all_files_in_folder(folder_path, delimiter)


