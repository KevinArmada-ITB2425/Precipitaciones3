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

    no_errors_count = 0
    files_with_errors = {}
    total_values = 0
    total_negative_999_values = 0
    total_lines_processed = 0

    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        cleaned_data, errors = read_and_clean_single_file(file_path, delimiter)

        # Si hi ha errors, afegeix-los al resum
        if errors:
            files_with_errors[file_name] = errors
        else:
            no_errors_count += 1

        # Comptar valors totals i valors amb -999
        if cleaned_data is not None:
            total_values += cleaned_data.size
            total_negative_999_values += (cleaned_data == "-999").sum().sum()
            total_lines_processed += len(cleaned_data)

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
    folder_path = "/home/kevin.armada.7e4/PycharmProjects/Precipitaciones3/dat"  # Ruta de la carpeta
    delimiter = " "  # Defineix el delimitador adequat
    process_all_files_in_folder(folder_path, delimiter)