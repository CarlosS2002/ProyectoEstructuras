"""
Paquete de análisis de facturación médica
"""

__version__ = "1.0.0"
__author__ = "Proyecto Estructuras"

# Importaciones principales
from .carga_datos import (
    cargar_json,
    cargar_csv,
    cargar_excel,
    exportar_a_csv,
    exportar_a_excel,
    info_dataframe
)

from .procesamiento import (
    normalizar_datos,
    estandarizar_datos,
    imputar_media,
    imputar_mediana,
    imputar_moda,
    ciclar_categorias
)

from .filtros import (
    filtrar_por_rango,
    filtrar_por_categoria,
    buscar_texto,
    filtrar_top_n,
    filtrar_outliers,
    filtrar_multiples_condiciones,
    resumen_filtros
)

from .estadisticas import (
    medidas_centralidad,
    medidas_dispersion,
    calcular_cuartiles,
    detectar_outliers,
    resumen_estadistico_completo,
    analisis_dispersion
)

from .correlaciones import (
    correlacion_pearson,
    correlacion_spearman,
    matriz_correlacion,
    matriz_covarianza,
    analisis_correlacion_completo
)

from .visualizaciones import (
    grafica_distribucion,
    diagrama_cajas,
    grafica_dispersion,
    grafica_relacional_seaborn,
    grafica_barras_categorias,
    pairplot_seaborn,
    dashboard_completo
)

from .inferencia import (
    test_normalidad,
    test_t_student,
    test_mann_whitney,
    test_anova,
    test_kruskal_wallis,
    test_chi_cuadrado,
    intervalo_confianza
)

__all__ = [
    # Carga de datos
    'cargar_json', 'cargar_csv', 'cargar_excel',
    'exportar_a_csv', 'exportar_a_excel', 'info_dataframe',
    
    # Procesamiento
    'normalizar_datos', 'estandarizar_datos',
    'imputar_media', 'imputar_mediana', 'imputar_moda', 'ciclar_categorias',
    
    # Filtros
    'filtrar_por_rango', 'filtrar_por_categoria', 'buscar_texto',
    'filtrar_top_n', 'filtrar_outliers', 'filtrar_multiples_condiciones', 'resumen_filtros',
    
    # Estadísticas
    'medidas_centralidad', 'medidas_dispersion', 'calcular_cuartiles',
    'detectar_outliers', 'resumen_estadistico_completo', 'analisis_dispersion',
    
    # Correlaciones
    'correlacion_pearson', 'correlacion_spearman', 'matriz_correlacion',
    'matriz_covarianza', 'analisis_correlacion_completo',
    
    # Visualizaciones
    'grafica_distribucion', 'diagrama_cajas', 'grafica_dispersion',
    'grafica_relacional_seaborn', 'grafica_barras_categorias',
    'pairplot_seaborn', 'dashboard_completo',
    
    # Inferencia
    'test_normalidad', 'test_t_student', 'test_mann_whitney',
    'test_anova', 'test_kruskal_wallis', 'test_chi_cuadrado', 'intervalo_confianza'
]
