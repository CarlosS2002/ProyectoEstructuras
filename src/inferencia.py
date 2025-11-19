"""
Módulo para estadísticas inferenciales
"""
import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import chi2_contingency, mannwhitneyu, kruskal, f_oneway, ttest_ind


def test_normalidad(df, columna):
    """
    Prueba de normalidad usando Shapiro-Wilk y Kolmogorov-Smirnov
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columna (str): Columna a analizar
        
    Returns:
        dict: Resultados de las pruebas
    """
    if columna not in df.columns:
        print(f"✗ Columna '{columna}' no encontrada")
        return None
    
    datos = df[columna].dropna()
    
    if len(datos) < 3:
        print(f"✗ No hay suficientes datos para realizar la prueba")
        return None
    
    # Shapiro-Wilk (mejor para muestras < 5000)
    if len(datos) <= 5000:
        stat_shapiro, p_shapiro = stats.shapiro(datos)
    else:
        stat_shapiro, p_shapiro = None, None
    
    # Kolmogorov-Smirnov
    stat_ks, p_ks = stats.kstest(datos, 'norm', args=(datos.mean(), datos.std()))
    
    print(f"\n--- Pruebas de Normalidad: {columna} ---")
    if stat_shapiro is not None:
        print(f"Shapiro-Wilk: estadístico={stat_shapiro:.4f}, p-valor={p_shapiro:.4f}")
        print(f"  Interpretación: {'Distribución NORMAL' if p_shapiro > 0.05 else 'Distribución NO NORMAL'}")
    
    print(f"Kolmogorov-Smirnov: estadístico={stat_ks:.4f}, p-valor={p_ks:.4f}")
    print(f"  Interpretación: {'Distribución NORMAL' if p_ks > 0.05 else 'Distribución NO NORMAL'}")
    
    return {
        'shapiro_stat': stat_shapiro,
        'shapiro_p': p_shapiro,
        'ks_stat': stat_ks,
        'ks_p': p_ks
    }


def test_t_student(df, columna, grupo1_filtro, grupo2_filtro):
    """
    Prueba t de Student para comparar medias de dos grupos
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columna (str): Columna con valores numéricos
        grupo1_filtro (pd.Series): Filtro booleano para grupo 1
        grupo2_filtro (pd.Series): Filtro booleano para grupo 2
        
    Returns:
        dict: Resultados de la prueba
    """
    grupo1 = df[grupo1_filtro][columna].dropna()
    grupo2 = df[grupo2_filtro][columna].dropna()
    
    if len(grupo1) < 2 or len(grupo2) < 2:
        print(f"✗ No hay suficientes datos en los grupos")
        return None
    
    # t-test independiente
    stat, p_valor = ttest_ind(grupo1, grupo2)
    
    print(f"\n--- Prueba t de Student: {columna} ---")
    print(f"Grupo 1: n={len(grupo1)}, media={grupo1.mean():.2f}, std={grupo1.std():.2f}")
    print(f"Grupo 2: n={len(grupo2)}, media={grupo2.mean():.2f}, std={grupo2.std():.2f}")
    print(f"Estadístico t: {stat:.4f}")
    print(f"P-valor: {p_valor:.4f}")
    print(f"Interpretación: {'Diferencia SIGNIFICATIVA' if p_valor < 0.05 else 'NO hay diferencia significativa'}")
    
    return {
        't_stat': stat,
        'p_valor': p_valor,
        'media_grupo1': grupo1.mean(),
        'media_grupo2': grupo2.mean()
    }


def test_mann_whitney(df, columna, grupo1_filtro, grupo2_filtro):
    """
    Prueba U de Mann-Whitney (alternativa no paramétrica a t-test)
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columna (str): Columna con valores numéricos
        grupo1_filtro (pd.Series): Filtro booleano para grupo 1
        grupo2_filtro (pd.Series): Filtro booleano para grupo 2
        
    Returns:
        dict: Resultados de la prueba
    """
    grupo1 = df[grupo1_filtro][columna].dropna()
    grupo2 = df[grupo2_filtro][columna].dropna()
    
    if len(grupo1) < 2 or len(grupo2) < 2:
        print(f"✗ No hay suficientes datos en los grupos")
        return None
    
    stat, p_valor = mannwhitneyu(grupo1, grupo2, alternative='two-sided')
    
    print(f"\n--- Prueba U de Mann-Whitney: {columna} ---")
    print(f"Grupo 1: n={len(grupo1)}, mediana={grupo1.median():.2f}")
    print(f"Grupo 2: n={len(grupo2)}, mediana={grupo2.median():.2f}")
    print(f"Estadístico U: {stat:.4f}")
    print(f"P-valor: {p_valor:.4f}")
    print(f"Interpretación: {'Diferencia SIGNIFICATIVA' if p_valor < 0.05 else 'NO hay diferencia significativa'}")
    
    return {
        'u_stat': stat,
        'p_valor': p_valor,
        'mediana_grupo1': grupo1.median(),
        'mediana_grupo2': grupo2.median()
    }


def test_anova(df, columna, columna_grupos):
    """
    Análisis de Varianza (ANOVA) para comparar medias de múltiples grupos
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columna (str): Columna con valores numéricos
        columna_grupos (str): Columna categórica que define los grupos
        
    Returns:
        dict: Resultados de la prueba
    """
    if columna not in df.columns or columna_grupos not in df.columns:
        print(f"✗ Una o ambas columnas no encontradas")
        return None
    
    grupos = []
    nombres_grupos = df[columna_grupos].unique()
    
    for nombre_grupo in nombres_grupos:
        grupo_datos = df[df[columna_grupos] == nombre_grupo][columna].dropna()
        if len(grupo_datos) > 0:
            grupos.append(grupo_datos)
    
    if len(grupos) < 2:
        print(f"✗ Se necesitan al menos 2 grupos para ANOVA")
        return None
    
    stat, p_valor = f_oneway(*grupos)
    
    print(f"\n--- ANOVA: {columna} por {columna_grupos} ---")
    print(f"Número de grupos: {len(grupos)}")
    for i, (nombre, grupo) in enumerate(zip(nombres_grupos, grupos)):
        print(f"  {nombre}: n={len(grupo)}, media={grupo.mean():.2f}, std={grupo.std():.2f}")
    print(f"Estadístico F: {stat:.4f}")
    print(f"P-valor: {p_valor:.4f}")
    print(f"Interpretación: {'Diferencia SIGNIFICATIVA entre grupos' if p_valor < 0.05 else 'NO hay diferencia significativa'}")
    
    return {
        'f_stat': stat,
        'p_valor': p_valor,
        'n_grupos': len(grupos)
    }


def test_kruskal_wallis(df, columna, columna_grupos):
    """
    Prueba de Kruskal-Wallis (alternativa no paramétrica a ANOVA)
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columna (str): Columna con valores numéricos
        columna_grupos (str): Columna categórica que define los grupos
        
    Returns:
        dict: Resultados de la prueba
    """
    if columna not in df.columns or columna_grupos not in df.columns:
        print(f"✗ Una o ambas columnas no encontradas")
        return None
    
    grupos = []
    nombres_grupos = df[columna_grupos].unique()
    
    for nombre_grupo in nombres_grupos:
        grupo_datos = df[df[columna_grupos] == nombre_grupo][columna].dropna()
        if len(grupo_datos) > 0:
            grupos.append(grupo_datos)
    
    if len(grupos) < 2:
        print(f"✗ Se necesitan al menos 2 grupos para Kruskal-Wallis")
        return None
    
    stat, p_valor = kruskal(*grupos)
    
    print(f"\n--- Kruskal-Wallis: {columna} por {columna_grupos} ---")
    print(f"Número de grupos: {len(grupos)}")
    for i, (nombre, grupo) in enumerate(zip(nombres_grupos, grupos)):
        print(f"  {nombre}: n={len(grupo)}, mediana={grupo.median():.2f}")
    print(f"Estadístico H: {stat:.4f}")
    print(f"P-valor: {p_valor:.4f}")
    print(f"Interpretación: {'Diferencia SIGNIFICATIVA entre grupos' if p_valor < 0.05 else 'NO hay diferencia significativa'}")
    
    return {
        'h_stat': stat,
        'p_valor': p_valor,
        'n_grupos': len(grupos)
    }


def test_chi_cuadrado(df, columna1, columna2):
    """
    Prueba Chi-cuadrado para independencia entre variables categóricas
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columna1 (str): Primera variable categórica
        columna2 (str): Segunda variable categórica
        
    Returns:
        dict: Resultados de la prueba
    """
    if columna1 not in df.columns or columna2 not in df.columns:
        print(f"✗ Una o ambas columnas no encontradas")
        return None
    
    tabla_contingencia = pd.crosstab(df[columna1], df[columna2])
    
    chi2, p_valor, dof, expected = chi2_contingency(tabla_contingencia)
    
    print(f"\n--- Prueba Chi-cuadrado: {columna1} vs {columna2} ---")
    print(f"Tabla de contingencia:")
    print(tabla_contingencia)
    print(f"\nEstadístico Chi²: {chi2:.4f}")
    print(f"Grados de libertad: {dof}")
    print(f"P-valor: {p_valor:.4f}")
    print(f"Interpretación: {'Variables DEPENDIENTES' if p_valor < 0.05 else 'Variables INDEPENDIENTES'}")
    
    return {
        'chi2_stat': chi2,
        'p_valor': p_valor,
        'dof': dof,
        'tabla_contingencia': tabla_contingencia
    }


def intervalo_confianza(df, columna, nivel_confianza=0.95):
    """
    Calcula el intervalo de confianza para la media
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columna (str): Columna a analizar
        nivel_confianza (float): Nivel de confianza (default 0.95)
        
    Returns:
        dict: Intervalo de confianza
    """
    if columna not in df.columns:
        print(f"✗ Columna '{columna}' no encontrada")
        return None
    
    datos = df[columna].dropna()
    
    if len(datos) < 2:
        print(f"✗ No hay suficientes datos")
        return None
    
    media = datos.mean()
    std_error = stats.sem(datos)
    intervalo = stats.t.interval(nivel_confianza, len(datos)-1, loc=media, scale=std_error)
    
    print(f"\n--- Intervalo de Confianza ({nivel_confianza*100}%): {columna} ---")
    print(f"Media: {media:.2f}")
    print(f"Error estándar: {std_error:.2f}")
    print(f"Intervalo: [{intervalo[0]:.2f}, {intervalo[1]:.2f}]")
    
    return {
        'media': media,
        'std_error': std_error,
        'limite_inferior': intervalo[0],
        'limite_superior': intervalo[1]
    }


if __name__ == "__main__":
    from carga_datos import cargar_json
    
    # Cargar datos
    df = cargar_json('../data/facturacion_medica.json')
    
    if df is not None:
        print("\n--- ESTADÍSTICAS INFERENCIALES ---\n")
        
        # Prueba de normalidad
        if 'montO_TOTAL' in df.columns:
            test_normalidad(df, 'montO_TOTAL')
        
        # Intervalo de confianza
        if 'montO_TOTAL' in df.columns:
            intervalo_confianza(df, 'montO_TOTAL')
        
        # ANOVA por clase de episodio
        if 'montO_TOTAL' in df.columns and 'clasE_EPISODIO' in df.columns:
            test_anova(df, 'montO_TOTAL', 'clasE_EPISODIO')
