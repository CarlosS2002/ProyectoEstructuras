"""
Módulo para búsqueda y filtrado de datos
"""
import pandas as pd
import numpy as np


def filtrar_por_rango(df, columna, min_valor, max_valor):
    """
    Filtra registros por rango de valores
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columna (str): Columna a filtrar
        min_valor: Valor mínimo
        max_valor: Valor máximo
        
    Returns:
        pd.DataFrame: DataFrame filtrado
    """
    if columna not in df.columns:
        print(f"✗ Columna '{columna}' no encontrada")
        return df
    
    df_filtrado = df[(df[columna] >= min_valor) & (df[columna] <= max_valor)]
    print(f"✓ Filtrado por rango en '{columna}': {len(df_filtrado)} registros de {len(df)}")
    return df_filtrado


def filtrar_por_categoria(df, columna, valores):
    """
    Filtra registros por valores categóricos específicos
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columna (str): Columna a filtrar
        valores (list): Lista de valores a incluir
        
    Returns:
        pd.DataFrame: DataFrame filtrado
    """
    if columna not in df.columns:
        print(f"✗ Columna '{columna}' no encontrada")
        return df
    
    if not isinstance(valores, list):
        valores = [valores]
    
    df_filtrado = df[df[columna].isin(valores)]
    print(f"✓ Filtrado por categoría en '{columna}': {len(df_filtrado)} registros de {len(df)}")
    return df_filtrado


def buscar_texto(df, columna, texto, case_sensitive=False):
    """
    Busca texto en una columna
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columna (str): Columna donde buscar
        texto (str): Texto a buscar
        case_sensitive (bool): Si la búsqueda distingue mayúsculas
        
    Returns:
        pd.DataFrame: DataFrame con resultados
    """
    if columna not in df.columns:
        print(f"✗ Columna '{columna}' no encontrada")
        return df
    
    df_filtrado = df[df[columna].astype(str).str.contains(texto, case=case_sensitive, na=False)]
    print(f"✓ Búsqueda de '{texto}' en '{columna}': {len(df_filtrado)} registros encontrados")
    return df_filtrado


def filtrar_top_n(df, columna, n=10, ascendente=False):
    """
    Obtiene los top N registros según una columna
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columna (str): Columna para ordenar
        n (int): Número de registros a obtener
        ascendente (bool): Orden ascendente o descendente
        
    Returns:
        pd.DataFrame: DataFrame con top N registros
    """
    if columna not in df.columns:
        print(f"✗ Columna '{columna}' no encontrada")
        return df
    
    df_top = df.nlargest(n, columna) if not ascendente else df.nsmallest(n, columna)
    orden = "menores" if ascendente else "mayores"
    print(f"✓ Top {n} {orden} valores en '{columna}'")
    return df_top


def filtrar_outliers(df, columna, metodo='iqr', umbral=1.5):
    """
    Filtra outliers usando el método IQR o Z-score
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columna (str): Columna a analizar
        metodo (str): 'iqr' o 'zscore'
        umbral (float): Umbral para detección (1.5 para IQR, 3 para Z-score)
        
    Returns:
        pd.DataFrame: DataFrame sin outliers
    """
    if columna not in df.columns:
        print(f"✗ Columna '{columna}' no encontrada")
        return df
    
    if not pd.api.types.is_numeric_dtype(df[columna]):
        print(f"✗ Columna '{columna}' no es numérica")
        return df
    
    df_filtrado = df.copy()
    
    if metodo == 'iqr':
        Q1 = df[columna].quantile(0.25)
        Q3 = df[columna].quantile(0.75)
        IQR = Q3 - Q1
        limite_inferior = Q1 - umbral * IQR
        limite_superior = Q3 + umbral * IQR
        df_filtrado = df[(df[columna] >= limite_inferior) & (df[columna] <= limite_superior)]
        
    elif metodo == 'zscore':
        media = df[columna].mean()
        std = df[columna].std()
        z_scores = np.abs((df[columna] - media) / std)
        df_filtrado = df[z_scores < umbral]
    
    outliers_removidos = len(df) - len(df_filtrado)
    print(f"✓ Outliers removidos de '{columna}': {outliers_removidos} registros")
    return df_filtrado


def filtrar_multiples_condiciones(df, condiciones):
    """
    Aplica múltiples condiciones de filtrado
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        condiciones (dict): Diccionario con condiciones
            Ejemplo: {'monto_total': {'min': 100, 'max': 1000},
                     'categoria': ['Emergencia', 'Quirófano']}
        
    Returns:
        pd.DataFrame: DataFrame filtrado
    """
    df_filtrado = df.copy()
    
    for columna, condicion in condiciones.items():
        if columna not in df.columns:
            print(f"✗ Columna '{columna}' no encontrada")
            continue
        
        if isinstance(condicion, dict):
            # Filtro por rango
            if 'min' in condicion:
                df_filtrado = df_filtrado[df_filtrado[columna] >= condicion['min']]
            if 'max' in condicion:
                df_filtrado = df_filtrado[df_filtrado[columna] <= condicion['max']]
        elif isinstance(condicion, list):
            # Filtro por categorías
            df_filtrado = df_filtrado[df_filtrado[columna].isin(condicion)]
        else:
            # Filtro por valor único
            df_filtrado = df_filtrado[df_filtrado[columna] == condicion]
    
    print(f"✓ Filtrado con múltiples condiciones: {len(df_filtrado)} registros de {len(df)}")
    return df_filtrado


def resumen_filtros(df, columna_agrupacion=None):
    """
    Muestra resumen de los datos con posibilidad de agrupación
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columna_agrupacion (str): Columna para agrupar (opcional)
    """
    print("\n" + "="*60)
    print("RESUMEN DE DATOS")
    print("="*60)
    print(f"Total de registros: {len(df)}")
    
    if columna_agrupacion and columna_agrupacion in df.columns:
        print(f"\nAgrupación por '{columna_agrupacion}':")
        print(df[columna_agrupacion].value_counts())
    
    print("\nEstadísticas numéricas:")
    print(df.describe())
    print("="*60 + "\n")


if __name__ == "__main__":
    from carga_datos import cargar_json
    
    # Cargar datos
    df = cargar_json('../data/facturacion_medica.json')
    
    if df is not None:
        print("\n--- EJEMPLOS DE FILTRADO ---\n")
        
        # Filtrar por rango de monto
        df_rango = filtrar_por_rango(df, 'monto_total', 200, 2000)
        
        # Filtrar por categoría
        df_emergencias = filtrar_por_categoria(df, 'categoria', ['Emergencia', 'Quirófano'])
        
        # Top 5 montos más altos
        df_top5 = filtrar_top_n(df, 'monto_total', n=5)
        
        # Búsqueda de texto
        df_cirugia = buscar_texto(df, 'diagnostico', 'Cirugía')
        
        # Resumen
        resumen_filtros(df, 'categoria')
