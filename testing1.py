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