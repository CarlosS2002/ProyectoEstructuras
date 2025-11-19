"""
Módulo para análisis de correlaciones y covarianza
"""
import pandas as pd
import numpy as np
from scipy.stats import spearmanr, pearsonr
import seaborn as sns
import matplotlib.pyplot as plt


def correlacion_pearson(df, columna1, columna2):
    """
    Calcula la correlación de Pearson entre dos variables
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columna1 (str): Primera columna
        columna2 (str): Segunda columna
        
    Returns:
        dict: Coeficiente de correlación y p-valor
    """
    if columna1 not in df.columns or columna2 not in df.columns:
        print(f"✗ Una o ambas columnas no encontradas")
        return None
    
    # Eliminar valores nulos
    df_limpio = df[[columna1, columna2]].dropna()
    
    if len(df_limpio) < 2:
        print(f"✗ No hay suficientes datos para calcular correlación")
        return None
    
    coef, p_valor = pearsonr(df_limpio[columna1], df_limpio[columna2])
    
    print(f"\n--- Correlación de Pearson ---")
    print(f"Variables: {columna1} vs {columna2}")
    print(f"Coeficiente: {coef:.4f}")
    print(f"P-valor: {p_valor:.4f}")
    print(f"Interpretación: ", end="")
    
    if abs(coef) < 0.3:
        print("Correlación débil")
    elif abs(coef) < 0.7:
        print("Correlación moderada")
    else:
        print("Correlación fuerte")
    
    return {'coeficiente': coef, 'p_valor': p_valor}


def correlacion_spearman(df, columna1, columna2):
    """
    Calcula la correlación de Spearman (no paramétrica) entre dos variables
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columna1 (str): Primera columna
        columna2 (str): Segunda columna
        
    Returns:
        dict: Coeficiente de correlación y p-valor
    """
    if columna1 not in df.columns or columna2 not in df.columns:
        print(f"✗ Una o ambas columnas no encontradas")
        return None
    
    # Eliminar valores nulos
    df_limpio = df[[columna1, columna2]].dropna()
    
    if len(df_limpio) < 2:
        print(f"✗ No hay suficientes datos para calcular correlación")
        return None
    
    coef, p_valor = spearmanr(df_limpio[columna1], df_limpio[columna2])
    
    print(f"\n--- Correlación de Spearman ---")
    print(f"Variables: {columna1} vs {columna2}")
    print(f"Coeficiente: {coef:.4f}")
    print(f"P-valor: {p_valor:.4f}")
    print(f"Interpretación: ", end="")
    
    if abs(coef) < 0.3:
        print("Correlación débil")
    elif abs(coef) < 0.7:
        print("Correlación moderada")
    else:
        print("Correlación fuerte")
    
    if p_valor < 0.05:
        print("Correlación estadísticamente significativa (p < 0.05)")
    else:
        print("Correlación NO estadísticamente significativa (p >= 0.05)")
    
    return {'coeficiente': coef, 'p_valor': p_valor}


def matriz_correlacion(df, columnas=None, metodo='pearson'):
    """
    Calcula la matriz de correlación para múltiples variables
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columnas (list): Lista de columnas a analizar (opcional)
        metodo (str): 'pearson' o 'spearman'
        
    Returns:
        pd.DataFrame: Matriz de correlación
    """
    if columnas is None:
        columnas = df.select_dtypes(include=[np.number]).columns.tolist()
    
    df_subset = df[columnas].dropna()
    
    if metodo == 'pearson':
        matriz = df_subset.corr(method='pearson')
    elif metodo == 'spearman':
        matriz = df_subset.corr(method='spearman')
    else:
        print(f"✗ Método '{metodo}' no válido. Use 'pearson' o 'spearman'")
        return None
    
    print(f"\n--- Matriz de Correlación ({metodo.capitalize()}) ---")
    print(matriz)
    
    return matriz


def matriz_covarianza(df, columnas=None):
    """
    Calcula la matriz de covarianza para múltiples variables
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columnas (list): Lista de columnas a analizar (opcional)
        
    Returns:
        pd.DataFrame: Matriz de covarianza
    """
    if columnas is None:
        columnas = df.select_dtypes(include=[np.number]).columns.tolist()
    
    df_subset = df[columnas].dropna()
    matriz = df_subset.cov()
    
    print(f"\n--- Matriz de Covarianza ---")
    print(matriz)
    
    return matriz


def visualizar_matriz_correlacion(df, columnas=None, metodo='pearson', archivo_salida=None):
    """
    Visualiza la matriz de correlación como un mapa de calor
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columnas (list): Lista de columnas a analizar (opcional)
        metodo (str): 'pearson' o 'spearman'
        archivo_salida (str): Ruta para guardar la imagen (opcional)
    """
    matriz = matriz_correlacion(df, columnas, metodo)
    
    if matriz is None:
        return
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(matriz, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                square=True, linewidths=1, cbar_kws={"shrink": 0.8})
    plt.title(f'Matriz de Correlación ({metodo.capitalize()})', fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    if archivo_salida:
        plt.savefig(archivo_salida, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfica guardada en: {archivo_salida}")
    
    plt.show()


def visualizar_matriz_covarianza(df, columnas=None, archivo_salida=None):
    """
    Visualiza la matriz de covarianza como un mapa de calor
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columnas (list): Lista de columnas a analizar (opcional)
        archivo_salida (str): Ruta para guardar la imagen (opcional)
    """
    matriz = matriz_covarianza(df, columnas)
    
    if matriz is None:
        return
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(matriz, annot=True, fmt='.2e', cmap='viridis',
                square=True, linewidths=1, cbar_kws={"shrink": 0.8})
    plt.title('Matriz de Covarianza', fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    if archivo_salida:
        plt.savefig(archivo_salida, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfica guardada en: {archivo_salida}")
    
    plt.show()


def analisis_correlacion_completo(df, columnas=None):
    """
    Realiza un análisis completo de correlaciones
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columnas (list): Lista de columnas a analizar (opcional)
    """
    if columnas is None:
        columnas = df.select_dtypes(include=[np.number]).columns.tolist()
    
    print("\n" + "="*80)
    print("ANÁLISIS DE CORRELACIONES COMPLETO")
    print("="*80)
    
    # Matriz de correlación Pearson
    print("\n" + "-"*80)
    matriz_pearson = matriz_correlacion(df, columnas, 'pearson')
    
    # Matriz de correlación Spearman
    print("\n" + "-"*80)
    matriz_spearman = matriz_correlacion(df, columnas, 'spearman')
    
    # Matriz de covarianza
    print("\n" + "-"*80)
    matriz_cov = matriz_covarianza(df, columnas)
    
    # Correlaciones más fuertes
    print("\n" + "-"*80)
    print("CORRELACIONES MÁS FUERTES (Pearson)")
    print("-"*80)
    
    # Obtener pares de correlaciones más altas (excluyendo diagonal)
    correlaciones = []
    for i in range(len(matriz_pearson.columns)):
        for j in range(i+1, len(matriz_pearson.columns)):
            col1 = matriz_pearson.columns[i]
            col2 = matriz_pearson.columns[j]
            coef = matriz_pearson.iloc[i, j]
            correlaciones.append((col1, col2, coef))
    
    # Ordenar por valor absoluto
    correlaciones.sort(key=lambda x: abs(x[2]), reverse=True)
    
    print(f"\nTop 5 correlaciones:")
    for i, (col1, col2, coef) in enumerate(correlaciones[:5], 1):
        print(f"{i}. {col1} vs {col2}: {coef:.4f}")
    
    print("\n" + "="*80 + "\n")
    
    return {
        'pearson': matriz_pearson,
        'spearman': matriz_spearman,
        'covarianza': matriz_cov
    }


if __name__ == "__main__":
    from carga_datos import cargar_json
    
    # Cargar datos
    df = cargar_json('../data/facturacion_medica.json')
    
    if df is not None:
        # Análisis de correlaciones completo
        columnas = ['montO_TOTAL', 'montO_CONSULTA', 'montO_MEDICAMENTOS', 
                   'montO_EXAMENES', 'edaD_PACIENTE', 'duracioN_MINUTOS']
        
        # Filtrar columnas que existen y no tienen todos nulos
        columnas_validas = [col for col in columnas if col in df.columns and df[col].notna().sum() > 0]
        
        resultados = analisis_correlacion_completo(df, columnas_validas)
        
        # Correlación específica de Spearman
        print("\n" + "="*80)
        correlacion_spearman(df, 'edaD_PACIENTE', 'montO_TOTAL')
        correlacion_spearman(df, 'duracioN_MINUTOS', 'montO_TOTAL')
