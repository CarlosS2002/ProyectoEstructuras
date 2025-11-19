"""
Módulo para procesamiento de datos: normalización, estandarización e imputación
"""
import pandas as pd
import numpy as np


def normalizar_datos(df, columnas):
    """
    Normaliza datos usando Min-Max Scaling (valores entre 0 y 1)
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columnas (list): Lista de columnas a normalizar
        
    Returns:
        pd.DataFrame: DataFrame con columnas normalizadas
    """
    df_normalizado = df.copy()
    
    for col in columnas:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            min_val = df[col].min()
            max_val = df[col].max()
            if max_val > min_val:
                df_normalizado[f'{col}_normalizado'] = (df[col] - min_val) / (max_val - min_val)
                print(f"✓ Columna '{col}' normalizada")
            else:
                print(f"✗ Columna '{col}' tiene valores constantes")
        else:
            print(f"✗ Columna '{col}' no encontrada o no es numérica")
    
    return df_normalizado


def estandarizar_datos(df, columnas):
    """
    Estandariza datos usando Z-score (media=0, desviación estándar=1)
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columnas (list): Lista de columnas a estandarizar
        
    Returns:
        pd.DataFrame: DataFrame con columnas estandarizadas
    """
    df_estandarizado = df.copy()
    
    for col in columnas:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            media = df[col].mean()
            std = df[col].std()
            if std > 0:
                df_estandarizado[f'{col}_estandarizado'] = (df[col] - media) / std
                print(f"✓ Columna '{col}' estandarizada")
            else:
                print(f"✗ Columna '{col}' tiene desviación estándar 0")
        else:
            print(f"✗ Columna '{col}' no encontrada o no es numérica")
    
    return df_estandarizado


def imputar_media(df, columnas):
    """
    Imputa valores faltantes usando la media
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columnas (list): Lista de columnas a imputar
        
    Returns:
        pd.DataFrame: DataFrame con valores imputados
    """
    df_imputado = df.copy()
    
    for col in columnas:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            media = df[col].mean()
            valores_nulos = df[col].isnull().sum()
            df_imputado[col].fillna(media, inplace=True)
            print(f"✓ Columna '{col}': {valores_nulos} valores imputados con media={media:.2f}")
        else:
            print(f"✗ Columna '{col}' no encontrada o no es numérica")
    
    return df_imputado


def imputar_mediana(df, columnas):
    """
    Imputa valores faltantes usando la mediana
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columnas (list): Lista de columnas a imputar
        
    Returns:
        pd.DataFrame: DataFrame con valores imputados
    """
    df_imputado = df.copy()
    
    for col in columnas:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            mediana = df[col].median()
            valores_nulos = df[col].isnull().sum()
            df_imputado[col].fillna(mediana, inplace=True)
            print(f"✓ Columna '{col}': {valores_nulos} valores imputados con mediana={mediana:.2f}")
        else:
            print(f"✗ Columna '{col}' no encontrada o no es numérica")
    
    return df_imputado


def imputar_moda(df, columnas):
    """
    Imputa valores faltantes usando la moda (más frecuente)
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columnas (list): Lista de columnas a imputar
        
    Returns:
        pd.DataFrame: DataFrame con valores imputados
    """
    df_imputado = df.copy()
    
    for col in columnas:
        if col in df.columns:
            moda = df[col].mode()[0] if not df[col].mode().empty else None
            valores_nulos = df[col].isnull().sum()
            if moda is not None:
                df_imputado[col].fillna(moda, inplace=True)
                print(f"✓ Columna '{col}': {valores_nulos} valores imputados con moda={moda}")
            else:
                print(f"✗ No se pudo calcular la moda para '{col}'")
        else:
            print(f"✗ Columna '{col}' no encontrada")
    
    return df_imputado


def ciclar_categorias(df, columna):
    """
    Convierte categorías en variables numéricas cíclicas
    Útil para datos temporales o categóricos con orden circular
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columna (str): Columna a ciclar
        
    Returns:
        pd.DataFrame: DataFrame con columnas sin y cos para representación cíclica
    """
    df_ciclado = df.copy()
    
    if columna in df.columns:
        # Convertir categoría a numérico
        categorias_unicas = df[columna].unique()
        n_categorias = len(categorias_unicas)
        
        mapeo = {cat: i for i, cat in enumerate(categorias_unicas)}
        df_ciclado[f'{columna}_numerico'] = df[columna].map(mapeo)
        
        # Crear representación cíclica
        df_ciclado[f'{columna}_sin'] = np.sin(2 * np.pi * df_ciclado[f'{columna}_numerico'] / n_categorias)
        df_ciclado[f'{columna}_cos'] = np.cos(2 * np.pi * df_ciclado[f'{columna}_numerico'] / n_categorias)
        
        print(f"✓ Columna '{columna}' ciclada ({n_categorias} categorías)")
    else:
        print(f"✗ Columna '{columna}' no encontrada")
    
    return df_ciclado


def resumen_procesamiento(df_original, df_procesado):
    """
    Muestra resumen del procesamiento de datos
    
    Args:
        df_original (pd.DataFrame): DataFrame original
        df_procesado (pd.DataFrame): DataFrame procesado
    """
    print("\n" + "="*60)
    print("RESUMEN DEL PROCESAMIENTO")
    print("="*60)
    print(f"Columnas originales: {df_original.shape[1]}")
    print(f"Columnas procesadas: {df_procesado.shape[1]}")
    print(f"Nuevas columnas: {df_procesado.shape[1] - df_original.shape[1]}")
    print(f"\nValores nulos originales: {df_original.isnull().sum().sum()}")
    print(f"Valores nulos procesados: {df_procesado.isnull().sum().sum()}")
    print("="*60 + "\n")


if __name__ == "__main__":
    from carga_datos import cargar_json
    
    # Cargar datos
    df = cargar_json('../data/facturacion_medica.json')
    
    if df is not None:
        print("\n--- PROCESAMIENTO DE DATOS ---\n")
        
        # Imputación
        columnas_imputar = ['monto_medicamentos', 'monto_examenes']
        df = imputar_media(df, columnas_imputar)
        
        # Normalización
        columnas_normalizar = ['monto_total', 'duracion_minutos']
        df = normalizar_datos(df, columnas_normalizar)
        
        # Estandarización
        columnas_estandarizar = ['edad_paciente']
        df = estandarizar_datos(df, columnas_estandarizar)
        
        print("\n✓ Procesamiento completado")
