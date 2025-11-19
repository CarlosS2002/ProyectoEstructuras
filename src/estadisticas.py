"""
Módulo para cálculo de estadísticas: centralidad, dispersión y cuartiles
"""
import pandas as pd
import numpy as np
from scipy import stats


def medidas_centralidad(df, columna):
    """
    Calcula medidas de centralidad (media, mediana, moda)
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columna (str): Columna a analizar
        
    Returns:
        dict: Diccionario con las medidas de centralidad
    """
    if columna not in df.columns:
        print(f"✗ Columna '{columna}' no encontrada")
        return None
    
    if not pd.api.types.is_numeric_dtype(df[columna]):
        print(f"✗ Columna '{columna}' no es numérica")
        return None
    
    resultados = {
        'media': df[columna].mean(),
        'mediana': df[columna].median(),
        'moda': df[columna].mode()[0] if not df[columna].mode().empty else None
    }
    
    print(f"\n--- Medidas de Centralidad: {columna} ---")
    print(f"Media: {resultados['media']:.2f}")
    print(f"Mediana: {resultados['mediana']:.2f}")
    print(f"Moda: {resultados['moda']:.2f}" if resultados['moda'] is not None else "Moda: No disponible")
    
    return resultados


def medidas_dispersion(df, columna):
    """
    Calcula medidas de dispersión (varianza, desviación estándar, rango, coeficiente de variación)
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columna (str): Columna a analizar
        
    Returns:
        dict: Diccionario con las medidas de dispersión
    """
    if columna not in df.columns:
        print(f"✗ Columna '{columna}' no encontrada")
        return None
    
    if not pd.api.types.is_numeric_dtype(df[columna]):
        print(f"✗ Columna '{columna}' no es numérica")
        return None
    
    resultados = {
        'varianza': df[columna].var(),
        'desviacion_estandar': df[columna].std(),
        'rango': df[columna].max() - df[columna].min(),
        'rango_intercuartilico': df[columna].quantile(0.75) - df[columna].quantile(0.25),
        'coeficiente_variacion': (df[columna].std() / df[columna].mean()) * 100 if df[columna].mean() != 0 else 0
    }
    
    print(f"\n--- Medidas de Dispersión: {columna} ---")
    print(f"Varianza: {resultados['varianza']:.2f}")
    print(f"Desviación Estándar: {resultados['desviacion_estandar']:.2f}")
    print(f"Rango: {resultados['rango']:.2f}")
    print(f"Rango Intercuartílico (IQR): {resultados['rango_intercuartilico']:.2f}")
    print(f"Coeficiente de Variación: {resultados['coeficiente_variacion']:.2f}%")
    
    return resultados


def calcular_cuartiles(df, columna):
    """
    Calcula cuartiles y percentiles de una columna
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columna (str): Columna a analizar
        
    Returns:
        dict: Diccionario con los cuartiles
    """
    if columna not in df.columns:
        print(f"✗ Columna '{columna}' no encontrada")
        return None
    
    if not pd.api.types.is_numeric_dtype(df[columna]):
        print(f"✗ Columna '{columna}' no es numérica")
        return None
    
    resultados = {
        'minimo': df[columna].min(),
        'Q1': df[columna].quantile(0.25),
        'Q2_mediana': df[columna].quantile(0.50),
        'Q3': df[columna].quantile(0.75),
        'maximo': df[columna].max(),
        'P10': df[columna].quantile(0.10),
        'P90': df[columna].quantile(0.90)
    }
    
    print(f"\n--- Cuartiles y Percentiles: {columna} ---")
    print(f"Mínimo: {resultados['minimo']:.2f}")
    print(f"Q1 (25%): {resultados['Q1']:.2f}")
    print(f"Q2 (Mediana 50%): {resultados['Q2_mediana']:.2f}")
    print(f"Q3 (75%): {resultados['Q3']:.2f}")
    print(f"Máximo: {resultados['maximo']:.2f}")
    print(f"P10: {resultados['P10']:.2f}")
    print(f"P90: {resultados['P90']:.2f}")
    
    return resultados


def detectar_outliers(df, columna):
    """
    Detecta outliers usando el método IQR
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columna (str): Columna a analizar
        
    Returns:
        pd.DataFrame: DataFrame con los outliers detectados
    """
    if columna not in df.columns:
        print(f"✗ Columna '{columna}' no encontrada")
        return None
    
    if not pd.api.types.is_numeric_dtype(df[columna]):
        print(f"✗ Columna '{columna}' no es numérica")
        return None
    
    Q1 = df[columna].quantile(0.25)
    Q3 = df[columna].quantile(0.75)
    IQR = Q3 - Q1
    
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR
    
    outliers = df[(df[columna] < limite_inferior) | (df[columna] > limite_superior)]
    
    print(f"\n--- Detección de Outliers: {columna} ---")
    print(f"Límite Inferior: {limite_inferior:.2f}")
    print(f"Límite Superior: {limite_superior:.2f}")
    print(f"Outliers detectados: {len(outliers)} de {len(df)} ({(len(outliers)/len(df)*100):.2f}%)")
    
    return outliers


def resumen_estadistico_completo(df, columnas_numericas=None):
    """
    Genera un resumen estadístico completo de las columnas numéricas
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columnas_numericas (list): Lista de columnas a analizar (opcional)
    """
    if columnas_numericas is None:
        columnas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
    
    print("\n" + "="*80)
    print("RESUMEN ESTADÍSTICO COMPLETO")
    print("="*80)
    
    for col in columnas_numericas:
        print(f"\n{'='*80}")
        print(f"COLUMNA: {col}")
        print(f"{'='*80}")
        
        medidas_centralidad(df, col)
        medidas_dispersion(df, col)
        calcular_cuartiles(df, col)
        
        # Detectar outliers
        outliers = detectar_outliers(df, col)
        if outliers is not None and len(outliers) > 0:
            print(f"\nEjemplos de outliers:")
            print(outliers[[col]].head())
    
    print("\n" + "="*80 + "\n")


def analisis_dispersion(df, columna_x, columna_y):
    """
    Analiza la dispersión entre dos variables
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columna_x (str): Primera columna
        columna_y (str): Segunda columna
        
    Returns:
        dict: Métricas de dispersión
    """
    if columna_x not in df.columns or columna_y not in df.columns:
        print(f"✗ Una o ambas columnas no encontradas")
        return None
    
    if not pd.api.types.is_numeric_dtype(df[columna_x]) or not pd.api.types.is_numeric_dtype(df[columna_y]):
        print(f"✗ Ambas columnas deben ser numéricas")
        return None
    
    # Eliminar valores nulos
    df_limpio = df[[columna_x, columna_y]].dropna()
    
    resultados = {
        'n_observaciones': len(df_limpio),
        'media_x': df_limpio[columna_x].mean(),
        'media_y': df_limpio[columna_y].mean(),
        'std_x': df_limpio[columna_x].std(),
        'std_y': df_limpio[columna_y].std(),
        'rango_x': df_limpio[columna_x].max() - df_limpio[columna_x].min(),
        'rango_y': df_limpio[columna_y].max() - df_limpio[columna_y].min()
    }
    
    print(f"\n--- Análisis de Dispersión: {columna_x} vs {columna_y} ---")
    print(f"N° Observaciones: {resultados['n_observaciones']}")
    print(f"\n{columna_x}:")
    print(f"  Media: {resultados['media_x']:.2f}")
    print(f"  Desv. Est.: {resultados['std_x']:.2f}")
    print(f"  Rango: {resultados['rango_x']:.2f}")
    print(f"\n{columna_y}:")
    print(f"  Media: {resultados['media_y']:.2f}")
    print(f"  Desv. Est.: {resultados['std_y']:.2f}")
    print(f"  Rango: {resultados['rango_y']:.2f}")
    
    return resultados


if __name__ == "__main__":
    from carga_datos import cargar_json
    
    # Cargar datos
    df = cargar_json('../data/facturacion_medica.json')
    
    if df is not None:
        # Realizar análisis estadístico completo
        columnas = ['montO_TOTAL', 'edaD_PACIENTE', 'duracioN_MINUTOS']
        resumen_estadistico_completo(df, columnas)
        
        # Análisis de dispersión
        analisis_dispersion(df, 'edaD_PACIENTE', 'montO_TOTAL')
