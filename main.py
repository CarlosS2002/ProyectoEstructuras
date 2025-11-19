"""
PROYECTO DE ANÁLISIS DE FACTURACIÓN MÉDICA
==========================================
Análisis completo de episodios de facturación médica en formato JSON

Componentes:
- Carga de datos (JSON, CSV, Excel)
- Procesamiento (normalización, estandarización, imputación)
- Filtros y búsqueda
- Estadísticas descriptivas
- Correlaciones (Pearson y Spearman)
- Visualizaciones (Matplotlib y Seaborn)
- Estadísticas inferenciales
- Matriz de covarianza
"""

import sys
import os

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from carga_datos import cargar_json, exportar_a_csv, exportar_a_excel, info_dataframe
from procesamiento import imputar_media, normalizar_datos, estandarizar_datos
from filtros import filtrar_por_rango, filtrar_por_categoria, filtrar_top_n, resumen_filtros
from estadisticas import resumen_estadistico_completo, analisis_dispersion
from correlaciones import analisis_correlacion_completo, correlacion_spearman
from visualizaciones import dashboard_completo, grafica_distribucion, diagrama_cajas, grafica_dispersion
from inferencia import test_normalidad, test_anova, intervalo_confianza

import warnings
warnings.filterwarnings('ignore')


def banner():
    """Muestra el banner del proyecto"""
    print("\n" + "="*80)
    print(" " * 15 + "ANÁLISIS DE FACTURACIÓN MÉDICA")
    print(" " * 20 + "Proyecto de Estructuras")
    print("="*80 + "\n")


def expandir_prestaciones(df):
    """
    Expande las prestaciones de cada episodio en filas separadas
    
    Args:
        df: DataFrame con episodios y prestaciones anidadas
        
    Returns:
        DataFrame con prestaciones expandidas
    """
    import pandas as pd
    
    prestaciones_list = []
    
    for idx, row in df.iterrows():
        try:
            if 'prestaciones' in df.columns:
                prestaciones = row['prestaciones']
                if isinstance(prestaciones, list) and len(prestaciones) > 0:
                    for prestacion in prestaciones:
                        if isinstance(prestacion, dict):
                            prestacion_row = row.to_dict()
                            prestacion_row.update(prestacion)
                            prestaciones_list.append(prestacion_row)
        except:
            continue
    
    if prestaciones_list:
        df_prestaciones = pd.DataFrame(prestaciones_list)
        print(f"✓ Prestaciones expandidas: {len(df_prestaciones)} registros")
        return df_prestaciones
    else:
        print("✗ No se encontraron prestaciones para expandir")
        return None


def analisis_episodios(df):
    """Análisis de los episodios de facturación"""
    print("\n" + "="*80)
    print("1. ANÁLISIS DE EPISODIOS")
    print("="*80)
    
    # Información general
    info_dataframe(df)
    
    # Estadísticas por aseguradora
    print("\n--- Distribución por Aseguradora ---")
    print(df['aseguradora'].value_counts().head(10))
    
    # Estadísticas por clase de episodio
    print("\n--- Distribución por Clase de Episodio ---")
    print(df['clasE_EPISODIO'].value_counts())
    
    # Estadísticas por estado de factura
    print("\n--- Distribución por Estado de Factura ---")
    print(df['staT_FACTURA'].value_counts())


def analisis_estadistico(df):
    """Análisis estadístico completo"""
    print("\n" + "="*80)
    print("2. ANÁLISIS ESTADÍSTICO")
    print("="*80)
    
    # Columnas numéricas principales
    columnas_numericas = ['montO_TOTAL', 'montO_CONSULTA', 'montO_MEDICAMENTOS', 
                         'montO_EXAMENES', 'edaD_PACIENTE', 'duracioN_MINUTOS']
    
    # Filtrar columnas que existen
    columnas_validas = [col for col in columnas_numericas if col in df.columns]
    
    # Imputación de valores nulos
    print("\n--- IMPUTACIÓN DE DATOS ---")
    columnas_imputar = [col for col in ['montO_MEDICAMENTOS', 'montO_EXAMENES'] if col in df.columns]
    if columnas_imputar:
        df = imputar_media(df, columnas_imputar)
    
    # Resumen estadístico completo
    resumen_estadistico_completo(df, columnas_validas)
    
    return df


def analisis_correlaciones(df):
    """Análisis de correlaciones"""
    print("\n" + "="*80)
    print("3. ANÁLISIS DE CORRELACIONES")
    print("="*80)
    
    columnas = ['montO_TOTAL', 'montO_CONSULTA', 'montO_MEDICAMENTOS', 
               'montO_EXAMENES', 'edaD_PACIENTE', 'duracioN_MINUTOS']
    
    # Filtrar columnas que existen y tienen datos
    columnas_validas = [col for col in columnas if col in df.columns and df[col].notna().sum() > 0]
    
    if len(columnas_validas) >= 2:
        resultados = analisis_correlacion_completo(df, columnas_validas)
        
        # Correlaciones de Spearman específicas
        print("\n" + "="*80)
        print("CORRELACIONES DE SPEARMAN DETALLADAS")
        print("="*80)
        
        if 'edaD_PACIENTE' in columnas_validas and 'montO_TOTAL' in columnas_validas:
            correlacion_spearman(df, 'edaD_PACIENTE', 'montO_TOTAL')
        
        if 'duracioN_MINUTOS' in columnas_validas and 'montO_TOTAL' in columnas_validas:
            correlacion_spearman(df, 'duracioN_MINUTOS', 'montO_TOTAL')


def analisis_filtros(df):
    """Análisis con filtros"""
    print("\n" + "="*80)
    print("4. BÚSQUEDA Y FILTROS")
    print("="*80)
    
    # Filtrar episodios de alto costo
    if 'montO_TOTAL' in df.columns:
        print("\n--- Episodios de Alto Costo (> 2,000,000) ---")
        df_alto_costo = filtrar_por_rango(df, 'montO_TOTAL', 2000000, float('inf'))
        if len(df_alto_costo) > 0:
            print(df_alto_costo[['episodio', 'noM_PACIENTE', 'montO_TOTAL', 'aseguradora']].head())
    
    # Top 10 episodios más costosos
    if 'montO_TOTAL' in df.columns:
        print("\n--- Top 10 Episodios Más Costosos ---")
        df_top10 = filtrar_top_n(df, 'montO_TOTAL', n=10)
        print(df_top10[['episodio', 'noM_PACIENTE', 'montO_TOTAL', 'clasE_EPISODIO']].head(10))
    
    # Filtrar por aseguradora
    if 'aseguradora' in df.columns:
        print("\n--- Filtro por Aseguradora (NUEVA EPS) ---")
        df_nueva_eps = filtrar_por_categoria(df, 'aseguradora', ['NUEVA EPS SA SUBSIDIADO'])
        if len(df_nueva_eps) > 0:
            resumen_filtros(df_nueva_eps, 'clasE_EPISODIO')


def analisis_inferencial(df):
    """Análisis de estadísticas inferenciales"""
    print("\n" + "="*80)
    print("5. ESTADÍSTICAS INFERENCIALES")
    print("="*80)
    
    # Prueba de normalidad
    if 'montO_TOTAL' in df.columns:
        test_normalidad(df, 'montO_TOTAL')
    
    if 'edaD_PACIENTE' in df.columns:
        test_normalidad(df, 'edaD_PACIENTE')
    
    # Intervalo de confianza
    if 'montO_TOTAL' in df.columns:
        intervalo_confianza(df, 'montO_TOTAL', 0.95)
    
    # ANOVA por clase de episodio
    if 'montO_TOTAL' in df.columns and 'clasE_EPISODIO' in df.columns:
        test_anova(df, 'montO_TOTAL', 'clasE_EPISODIO')
    
    # ANOVA por estado de factura
    if 'montO_TOTAL' in df.columns and 'staT_FACTURA' in df.columns:
        test_anova(df, 'montO_TOTAL', 'staT_FACTURA')


def analisis_prestaciones(df_prestaciones):
    """Análisis de las prestaciones"""
    if df_prestaciones is None:
        print("\n✗ No hay prestaciones para analizar")
        return
    
    print("\n" + "="*80)
    print("6. ANÁLISIS DE PRESTACIONES")
    print("="*80)
    
    # Información general de prestaciones
    print(f"\nTotal de prestaciones: {len(df_prestaciones)}")
    
    # Top prestaciones por frecuencia
    if 'noM_PRESTACION' in df_prestaciones.columns:
        print("\n--- Top 10 Prestaciones Más Frecuentes ---")
        print(df_prestaciones['noM_PRESTACION'].value_counts().head(10))
    
    # Top prestaciones por valor
    if 'valoR_NETO' in df_prestaciones.columns:
        print("\n--- Top 10 Prestaciones de Mayor Valor ---")
        df_prestaciones['valoR_NETO_NUM'] = pd.to_numeric(df_prestaciones['valoR_NETO'], errors='coerce')
        top_valor = df_prestaciones.nlargest(10, 'valoR_NETO_NUM')[['noM_PRESTACION', 'valoR_NETO', 'episodio']]
        print(top_valor)
    
    # Distribución por tipo de prestación
    if 'tipO_PRESTACION' in df_prestaciones.columns:
        print("\n--- Distribución por Tipo de Prestación ---")
        print(df_prestaciones['tipO_PRESTACION'].value_counts())


def main():
    """Función principal"""
    banner()
    
    try:
        # 1. Cargar datos
        print("="*80)
        print("CARGANDO DATOS")
        print("="*80 + "\n")
        
        ruta_json = os.path.join('data', 'facturacion_medica.json')
        df = cargar_json(ruta_json)
        
        if df is None:
            print("✗ Error al cargar los datos. Verifica la ruta del archivo.")
            return
        
        # Exportar a otros formatos
        exportar_a_csv(df, os.path.join('data', 'facturacion_medica.csv'))
        exportar_a_excel(df, os.path.join('data', 'facturacion_medica.xlsx'))
        
        # 2. Análisis de episodios
        analisis_episodios(df)
        
        # 3. Expandir prestaciones
        df_prestaciones = expandir_prestaciones(df)
        
        # 4. Análisis estadístico
        df = analisis_estadistico(df)
        
        # 5. Análisis de correlaciones
        analisis_correlaciones(df)
        
        # 6. Búsqueda y filtros
        analisis_filtros(df)
        
        # 7. Estadísticas inferenciales
        analisis_inferencial(df)
        
        # 8. Análisis de prestaciones
        if df_prestaciones is not None:
            analisis_prestaciones(df_prestaciones)
        
        # 9. Visualizaciones (opcional - comentado para no abrir ventanas)
        print("\n" + "="*80)
        print("7. VISUALIZACIONES")
        print("="*80)
        print("\nPara generar visualizaciones, ejecuta:")
        print("  python -c \"from src.visualizaciones import *; from src.carga_datos import cargar_json; df = cargar_json('data/facturacion_medica.json'); dashboard_completo(df)\"")
        
        # Descomentar para generar visualizaciones automáticamente:
        # dashboard_completo(df)
        # grafica_distribucion(df, 'montO_TOTAL')
        # diagrama_cajas(df, ['montO_TOTAL', 'edaD_PACIENTE', 'duracioN_MINUTOS'])
        
        print("\n" + "="*80)
        print("✓ ANÁLISIS COMPLETADO EXITOSAMENTE")
        print("="*80 + "\n")
        
        print("Los datos han sido exportados a:")
        print("  - data/facturacion_medica.csv")
        print("  - data/facturacion_medica.xlsx")
        print("\nPara más análisis, explora los módulos en la carpeta 'src/'")
        
    except Exception as e:
        print(f"\n✗ Error durante el análisis: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import pandas as pd
    main()
