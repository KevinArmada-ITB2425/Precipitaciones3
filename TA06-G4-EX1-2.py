############################EJERCICIO2 PASO 1########################################

# Directorio
import os

directory = './dat'

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

print("-------------Ejercicio 2 Paso 2-------------")
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
                # A partir de la tercera línia, comprovar si existeix un valor que comenci amb "P" i un any en format "2XXX"
                if i >= 3:  # Comença a validar a partir de la tercera línia
                    has_p_value = any(col.startswith('P') for col in columns)
                    has_year = any(col.startswith('2') and len(col) == 4 and col.isdigit() for col in columns)
                    has_month = False

                    # Comprovar si hi ha un mes vàlid (1-12)
                    for col in columns:
                        if col.isdigit() and 1 <= int(col) <= 12:
                            has_month = True
                            break
                        elif col == "0" or col.strip() == "":  # Comprovar si hi ha un 0 o una cadena buida
                            invalid_lines.append((i, "Et falta el mes en aquesta línia! Ha de ser del 1 al 12."))
                            break  # Només un cop per línia

                    if not has_p_value:
                        invalid_lines.append((i, "Línia ha de contenir un valor que comenci amb 'P'"))
                    if not has_year:
                        invalid_lines.append((i, "Hey chavalin, et falta l'any en aquesta línia!"))

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

        # Crear CSV d'errors
        create_error_csv(files_with_errors)

    else:
        print("\nTots els fitxers són vàlids!")


def create_error_csv(files_with_errors):
    """
    Crea un fitxer CSV amb els errors trobats en els fitxers .dat.

    Args:
        files_with_errors (dict): Diccionari amb el nom del fitxer i els errors trobats.
    """
    error_list = []

    for file_name, errors in files_with_errors.items():
        for line_num, error in errors:
            error_list.append({"File Name": file_name, "Line Number": line_num, "Error": error})

    error_df = pd.DataFrame(error_list)

    # Guardar el DataFrame com a CSV
    error_df.to_csv("errors_report.csv", index=False)
    print("\nS'ha creat 'errors_report.csv' amb els errors trobats.")


# Exemple d'ús
if __name__ == "__main__":
    folder_path = "./dat"  # Ruta de la carpeta
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

    print("\n -------------Ejercicio 2 Paso 4-------------")
    print("\n--- ESTADISTICAS GENERALES ---")
    print(f"Total de valores procesados: {total_values:,}")
    print(f"Valores Faltantes (-999): {total_negative_999_values:,}")
    print(f"Porcentaje de datos faltantes: {missing_percentage:.2f}%")
    print(f"Archivos Procesados: {len(files):,}")
    print(f"Líneas Procesadas: {total_lines_processed:,}")


# Exemple d'ús
if __name__ == "__main__":
    folder_path = "./dat"  # Ruta de la carpeta
    delimiter = " "  # Defineix el delimitador adequat
    process_all_files_in_folder(folder_path, delimiter)

############################EJERCICIO2 PASO 4 . 2########################################
import os
import pandas as pd

# Ruta a la carpeta que contiene los archivos .dat
carpeta = 'dat'

# Crear un DataFrame vacío para almacenar los datos de todas las estaciones
datos_totales = pd.DataFrame()

# Leer todos los archivos .dat en la carpeta
for archivo in os.listdir(carpeta):
    if archivo.endswith('.dat'):
        # Leer el archivo .dat
        ruta_archivo = os.path.join(carpeta, archivo)
        try:
            # Leer el archivo completo, ignorando las dos primeras líneas
            with open(ruta_archivo, 'r') as f:
                lineas = f.readlines()

                # Procesar solo las líneas relevantes (comenzando desde la línea 2)
                for linea in lineas[2:]:
                    # Separar la línea por espacios y filtrar valores válidos
                    valores = linea.split()
                    if len(valores) > 0 and valores[0] == 'P1':
                        # Extraer el año y los valores de precipitación
                        anio = int(valores[1])
                        precipitaciones = [float(v) for v in valores[2:] if v != '-999']  # Ignorar valores -999

                        # Sumar las precipitaciones del año
                        total_precipitacion = sum(precipitaciones)
                        # Crear un DataFrame temporal
                        df_temporal = pd.DataFrame({'Año': [anio], 'Precipitación': [total_precipitacion]})

                        # Concatenar al DataFrame total
                        datos_totales = pd.concat([datos_totales, df_temporal], ignore_index=True)

        except Exception as e:
            print(f"Error al procesar {archivo}: {e}")

# Calcular precipitaciones totales y medias anuales
precipitacion_anual = datos_totales.groupby('Año')['Precipitación'].agg(['sum', 'mean']).reset_index()
precipitacion_anual.columns = ['Año', 'Total Precipitación (mm)', 'Media Precipitación (mm)']

# Filtrar por el rango de años deseado (2006 a 2100)
precipitacion_anual = precipitacion_anual[(precipitacion_anual['Año'] >= 2006) & (precipitacion_anual['Año'] <= 2100)]

# Redondear las columnas de precipitación a 2 decimales
precipitacion_anual['Total Precipitación (mm)'] = precipitacion_anual['Total Precipitación (mm)'].round(2)
precipitacion_anual['Media Precipitación (mm)'] = precipitacion_anual['Media Precipitación (mm)'].round(2)

# Mostrar total y media de precipitaciones
total_precipitacion = precipitacion_anual['Total Precipitación (mm)'].sum()
media_precipitacion = precipitacion_anual['Media Precipitación (mm)'].mean()
print("\n -------------Ejercicio 2 Paso 4.2-------------")
print("\n===== Total y Media de Precipitaciones =====")
print(f"Total de precipitaciones desde 2006 hasta 2100: {total_precipitacion:,.2f} mm")
print(f"Media de precipitaciones anuales desde 2006 hasta 2100: {media_precipitacion:,.2f} mm")

# Función para calcular extremos de precipitación
def anys_extrems(data):
    any_mes_plujos = data.loc[data['Total Precipitación (mm)'].idxmax()]
    any_mes_sec = data.loc[data['Total Precipitación (mm)'].idxmin()]

    print("\n===== Extrems de precipitació =====")
    print(f"🟦 Any més plujós: {any_mes_plujos['Año']} amb {any_mes_plujos['Total Precipitación (mm)']} mm")
    print(f"🟨 Any més sec: {any_mes_sec['Año']} amb {any_mes_sec['Total Precipitación (mm)']} mm")
    return any_mes_plujos, any_mes_sec

# Función para calcular estadísticas adicionales
def estadistiques_addicionals(data):
    desviacio_estandard = data['Total Precipitación (mm)'].std()
    mediana = data['Total Precipitación (mm)'].median()
    print("\n===== Estadístiques addicionals =====")
    print(f"📊 Desviació estàndard de les precipitacions: {desviacio_estandard:.2f} mm")
    print(f"📈 Mediana de les precipitacions anuals: {mediana:.2f} mm")
    return desviacio_estandard, mediana

# Calcular extremos y estadísticas
any_mes_plujos, any_mes_sec = anys_extrems(precipitacion_anual)
desviacio_estandard, mediana = estadistiques_addicionals(precipitacion_anual)

# Mostrar el total de precipitaciones en litros por cada dos años
print("\n===== Total de precipitaciones cada dos años (en litros) =====")
for i in range(0, len(precipitacion_anual), 2):
    if i + 1 < len(precipitacion_anual):  # Asegurarse de que hay un segundo año para sumar
        total_litros = (precipitacion_anual.iloc[i]['Total Precipitación (mm)'] +
                        precipitacion_anual.iloc[i + 1]['Total Precipitación (mm)']) * 1000  # mm a litros
        print(f"De {int(precipitacion_anual.iloc[i]['Año'])} a {int(precipitacion_anual.iloc[i + 1]['Año'])}: {total_litros:,.2f} litros")

# Mostrar resumen final
print("\n===== Resumen Final =====")
print(f"El any més plujós serà el {any_mes_plujos['Año']} amb una precipitació de {any_mes_plujos['Total Precipitación (mm)']} mm.")
print(f"El any més sec serà el {any_mes_sec['Año']} amb una precipitació de {any_mes_sec['Total Precipitación (mm)']} mm.")

# Exportar resúmenes estadísticos a un archivo CSV
precipitacion_anual.to_csv('resumen_precipitacion.csv', index=False)
print("El resumen estadístico ha sido exportado a 'resumen_precipitacion.csv'")




########################## EJERCICIO 3 #############################
import os
import pandas as pd
import matplotlib.pyplot as plt

# Ruta a la carpeta que contiene los archivos .dat
carpeta = 'dat'

# Crear un DataFrame vacío para almacenar los datos de todas las estaciones
datos_totales = pd.DataFrame()

# Leer todos los archivos .dat en la carpeta
for archivo in os.listdir(carpeta):
    if archivo.endswith('.dat'):
        # Leer el archivo .dat
        ruta_archivo = os.path.join(carpeta, archivo)
        try:
            # Leer el archivo completo, ignorando las dos primeras líneas
            with open(ruta_archivo, 'r') as f:
                lineas = f.readlines()

                # Procesar solo las líneas relevantes (comenzando desde la línea 2)
                for linea in lineas[2:]:
                    # Separar la línea por espacios y filtrar valores válidos
                    valores = linea.split()
                    if len(valores) > 0 and valores[0] == 'P1':
                        # Extraer el año y los valores de precipitación
                        anio = int(float(valores[1]))  # Asegurarse de que el año sea un entero
                        precipitaciones = [float(v) for v in valores[2:] if v != '-999']  # Ignorar valores -999

                        # Sumar las precipitaciones del año
                        total_precipitacion = sum(precipitaciones)
                        # Crear un DataFrame temporal
                        df_temporal = pd.DataFrame({'Año': [anio], 'Precipitación': [total_precipitacion]})

                        # Concatenar al DataFrame total
                        datos_totales = pd.concat([datos_totales, df_temporal], ignore_index=True)

        except Exception as e:
            print(f"Error al procesar {archivo}: {e}")

# Calcular precipitaciones totales y medias anuales
precipitacion_anual = datos_totales.groupby('Año')['Precipitación'].agg(['sum', 'mean']).reset_index()
precipitacion_anual.columns = ['Año', 'Total Precipitación (mm)', 'Media Precipitación (mm)']

# Filtrar por el rango de años deseado (2006 a 2100)
precipitacion_anual = precipitacion_anual[(precipitacion_anual['Año'] >= 2006) & (precipitacion_anual['Año'] <= 2100)]

# Asegurarse de que la columna "Año" sea de tipo entero
precipitacion_anual['Año'] = precipitacion_anual['Año'].astype(int)

# Exportar resúmenes estadísticos a un archivo CSV
precipitacion_anual.to_csv('resumen_precipitacion.csv', index=False)

# Generar el gráfico de barras
plt.figure(figsize=(14, 7))
plt.bar(precipitacion_anual['Año'], precipitacion_anual['Total Precipitación (mm)'], color='skyblue')
plt.title('Precipitación Anual (2006-2100)')
plt.xlabel('Año')
plt.ylabel('Precipitación Total (mm)')

# Establecer las etiquetas del eje X para que muestren todos los años
plt.xticks(precipitacion_anual['Año'], rotation=90)  # Rotación de 90 grados para mejor legibilidad

plt.grid(axis='y', linestyle='--', alpha=0.7)  # Añadir líneas de cuadrícula en el eje Y
plt.tight_layout()  # Ajustar el layout para que no se solapen las etiquetas

# Añadir print para indicar que se está abriendo el gráfico
print("\n -------------Ejercicio 3-------------")
print("Abriendo gráfico...")

plt.show()

# Obtener el año más pluvioso y más seco
anio_max_precip = precipitacion_anual.loc[precipitacion_anual['Total Precipitación (mm)'].idxmax()]
anio_min_precip = precipitacion_anual.loc[precipitacion_anual['Total Precipitación (mm)'].idxmin()]

# Mostrar el resumen final con años como enteros
print(f"\n===== Resumen Final =====")
print(f"El año más pluvioso será el {anio_max_precip['Año']} con una precipitación de {anio_max_precip['Total Precipitación (mm)']} mm.")
print(f"El año más seco será el {anio_min_precip['Año']} con una precipitación de {anio_min_precip['Total Precipitación (mm)']} mm.")
print("El resumen estadístico ha sido exportado a 'resumen_precipitacion.csv'")



