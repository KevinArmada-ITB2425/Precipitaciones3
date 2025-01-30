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
plt.show()

print("El resumen estadístico ha sido exportado a 'resumen_precipitacion.csv'")
