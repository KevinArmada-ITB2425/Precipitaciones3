import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


# Función para leer los archivos .dat de una carpeta
def read_dat_files(folder_path):
    data_frames = []

    if not os.path.isdir(folder_path):
        print(f"La ruta {folder_path} no es válida.")
        return None

    files = [f for f in os.listdir(folder_path) if f.endswith('.dat')]

    if not files:
        print("No se han encontrado archivos .dat en la carpeta.")
        return None

    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        try:
            # Leer el archivo omitiendo las dos primeras líneas
            df = pd.read_csv(file_path, sep='\s+', header=None, skiprows=2)

            # Comprobar que el DataFrame tiene datos
            if df.empty:
                print(f"El archivo {file_name} no contiene datos útiles después de las líneas omitidas.")
                continue

            # Asegurarse de que las columnas sean correctas
            # Asegúrate de ajustar los índices según tus necesidades
            df.columns = ['Tipo', 'Año', 'Mes'] + [f'Dia_{i}' for i in range(1, df.shape[1] - 2)]
            data_frames.append(df)

            print(f"Datos del archivo {file_name} leídos con éxito.")
        except Exception as e:
            print(f"Error al leer el archivo {file_name}: {e}")

    if data_frames:
        return pd.concat(data_frames, ignore_index=True)
    else:
        return None


# 1. Mitjanes i totals anuals
def mitjanes_i_totals_anuals(data):
    if data is None or data.empty:
        print("No hay datos para calcular.")
        return None, None

    # Suponiendo que el segundo índice corresponde a la columna del año
    totals = data['Dia_1'].sum()  # Reemplazar 'Dia_1' con la columna correspondiente a la precipitación
    mitjana = data['Dia_1'].mean()
    print(f"Precipitació total: {totals} mm")
    print(f"Precipitació mitjana anual: {mitjana:.2f} mm")
    return totals, mitjana


# 2. Tendència de canvi (taxa de variació anual)
def tendencia_canvi(data):
    data['variacio_anual'] = data[
                                 'Dia_1'].pct_change() * 100  # Reemplazar 'Dia_1' con la columna correspondiente a la precipitación
    print("\nTaxa de variació anual de les precipitacions (%):")
    print(data[['Año', 'variacio_anual']].dropna())

    plt.figure(figsize=(20, 10))
    plt.bar(data['Año'], data['Dia_1'], color='skyblue', label='Precipitació (mm)')  # Reemplazar 'Dia_1'
    plt.title('Precipitació anual', fontsize=16)
    plt.xlabel('Any', fontsize=14)
    plt.ylabel('Precipitació (mm)', fontsize=14)
    plt.xticks(data['Año'], rotation=90, fontsize=8)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()


# 3. Extrems (anys més plujosos i més secs)
def anys_extrems(data):
    any_mes_plujos = data.loc[data['Dia_1'].idxmax()]  # Reemplazar 'Dia_1'
    any_mes_sec = data.loc[data['Dia_1'].idxmin()]

    print("\n===== Extrems de precipitació =====")
    print(f"🟦 Any més plujós: {any_mes_plujos['Año']} amb {any_mes_plujos['Dia_1']} mm")  # Reemplazar 'Dia_1'
    print(f"🟨 Any més sec: {any_mes_sec['Año']} amb {any_mes_sec['Dia_1']} mm")  # Reemplazar 'Dia_1'
    return any_mes_plujos, any_mes_sec


# 4. Estadístiques addicionals
def estadistiques_addicionals(data):
    desviacio_estandard = data['Dia_1'].std()  # Reemplazar 'Dia_1'
    mediana = data['Dia_1'].median()
    print("\n===== Estadístiques addicionals =====")
    print(f"📊 Desviació estàndard de les precipitacions: {desviacio_estandard:.2f} mm")
    print(f"📈 Mediana de les precipitacions anuals: {mediana:.2f} mm")
    return desviacio_estandard, mediana


# Ejecutar el código principal
if __name__ == "__main__":
    folder_path = "./dat.proves"  # Cambia esto a la ruta real de tu carpeta
    df = read_dat_files(folder_path)

    # Ejecutar las funciones
    totals, mitjana = mitjanes_i_totals_anuals(df)
    tendencia_canvi(df)
    any_mes_plujos, any_mes_sec = anys_extrems(df)
    desviacio_estandard, mediana = estadistiques_addicionals(df)

    # Mostrar resumen final
    print("\n===== Resumen Final =====")
    print(
        f"El any més plujós serà el {any_mes_plujos['Año']} amb una precipitació de {any_mes_plujos['Dia_1']} mm.")  # Reemplazar 'Dia_1'
    print(
        f"El any més sec serà el {any_mes_sec['Año']} amb una precipitació de {any_mes_sec['Dia_1']} mm.")  # Reemplazar 'Dia_1'
