# GUÍA DE USO - Proyecto de Análisis de Facturación Médica

## 📋 Descripción General

Este proyecto realiza un análisis completo de episodios de facturación médica en formato JSON, incluyendo:
- ✅ Carga de datos (JSON, CSV, Excel)
- ✅ Normalización y Estandarización
- ✅ Imputación de datos faltantes
- ✅ Búsqueda y Filtros
- ✅ Pandas y DataFrames
- ✅ Medidas de centralidad
- ✅ Cuartiles
- ✅ Medidas de dispersión
- ✅ Correlación de Spearman
- ✅ Análisis de dispersión
- ✅ Estadísticas inferenciales
- ✅ Matriz de covarianza
- ✅ Matplotlib para visualizaciones
- ✅ Distribución de datos
- ✅ Diagrama de cajas (boxplot)
- ✅ Gráficas relacionales (Seaborn)

## 🚀 Instalación

### 1. Requisitos previos
- Python 3.8 o superior

### 2. Instalar dependencias
```powershell
pip install -r requirements.txt
```

Las dependencias incluyen:
- pandas (manejo de datos)
- numpy (operaciones numéricas)
- matplotlib (visualizaciones)
- seaborn (gráficas estadísticas)
- scipy (estadísticas avanzadas)
- openpyxl (soporte para Excel)

## 📂 Estructura del Proyecto

```
ProyectoEstructuras/
│
├── data/                           # Datos del proyecto
│   ├── facturacion_medica.json     # Datos originales (episodios + prestaciones)
│   ├── facturacion_medica.csv      # Exportado automáticamente
│   └── facturacion_medica.xlsx     # Exportado automáticamente
│
├── src/                            # Código fuente
│   ├── __init__.py                 # Inicializador del paquete
│   ├── carga_datos.py              # Carga y exportación de datos
│   ├── procesamiento.py            # Normalización e imputación
│   ├── filtros.py                  # Búsqueda y filtrado
│   ├── estadisticas.py             # Centralidad, dispersión, cuartiles
│   ├── correlaciones.py            # Pearson, Spearman, covarianza
│   ├── visualizaciones.py          # Gráficas con Matplotlib/Seaborn
│   └── inferencia.py               # Estadísticas inferenciales
│
├── main.py                         # Programa principal
├── requirements.txt                # Dependencias
├── README.md                       # Documentación general
└── GUIA_USO.md                     # Esta guía
```

## 🎯 Ejecución Rápida

### Ejecutar análisis completo
```powershell
python main.py
```

Este comando ejecutará:
1. Carga de datos desde JSON
2. Análisis de episodios de facturación
3. Expansión de prestaciones
4. Estadísticas descriptivas
5. Análisis de correlaciones
6. Filtros y búsquedas
7. Estadísticas inferenciales
8. Análisis de prestaciones

## 📊 Estructura de Datos

### Episodio (nivel principal)
```json
{
    "centrO_SANITARIO": "1000",
    "episodio": "0008034508",
    "clasE_EPISODIO": "2",
    "doC_PACIENTE": "7589711",
    "staT_FACTURA": "2",
    "fechA_CREACION": "20250705",
    "estadO_EPISODIO": "A",
    "noM_PACIENTE": "FERNANDEZ DORYS",
    "aseguradora": "NUEVA EPS SA SUBSIDIADO",
    "montO_TOTAL": 850250.50,
    "edaD_PACIENTE": 45,
    "prestaciones": [...]
}
```

### Prestaciones (detalles de facturación)
```json
{
    "coD_PRESTACION": "0000890701",
    "noM_PRESTACION": "CONSULTA DE URGENCIAS",
    "fechA_PRESTACION": "2025-07-05T00:00:00",
    "tipO_PRESTACION": "01-COUR",
    "valoR_NETO": "450000.00"
}
```

## 💡 Ejemplos de Uso

### 1. Cargar y explorar datos
```python
from src.carga_datos import cargar_json, info_dataframe

# Cargar datos
df = cargar_json('data/facturacion_medica.json')

# Ver información
info_dataframe(df)
```

### 2. Filtros y búsqueda
```python
from src.filtros import filtrar_por_rango, filtrar_por_categoria, filtrar_top_n

# Episodios de alto costo
df_alto_costo = filtrar_por_rango(df, 'montO_TOTAL', 2000000, float('inf'))

# Filtrar por aseguradora
df_nueva_eps = filtrar_por_categoria(df, 'aseguradora', ['NUEVA EPS SA SUBSIDIADO'])

# Top 10 más costosos
df_top10 = filtrar_top_n(df, 'montO_TOTAL', n=10)
```

### 3. Análisis estadístico
```python
from src.estadisticas import medidas_centralidad, medidas_dispersion, calcular_cuartiles

# Medidas de centralidad
medidas_centralidad(df, 'montO_TOTAL')

# Medidas de dispersión
medidas_dispersion(df, 'montO_TOTAL')

# Cuartiles
calcular_cuartiles(df, 'edaD_PACIENTE')
```

### 4. Correlaciones
```python
from src.correlaciones import correlacion_spearman, matriz_correlacion, matriz_covarianza

# Correlación de Spearman
correlacion_spearman(df, 'edaD_PACIENTE', 'montO_TOTAL')

# Matriz de correlación
columnas = ['montO_TOTAL', 'edaD_PACIENTE', 'duracioN_MINUTOS']
matriz = matriz_correlacion(df, columnas, metodo='spearman')

# Matriz de covarianza
cov_matriz = matriz_covarianza(df, columnas)
```

### 5. Visualizaciones
```python
from src.visualizaciones import (
    dashboard_completo,
    grafica_distribucion,
    diagrama_cajas,
    grafica_dispersion
)

# Dashboard completo
dashboard_completo(df)

# Distribución de montos
grafica_distribucion(df, 'montO_TOTAL')

# Diagrama de cajas
diagrama_cajas(df, ['montO_TOTAL', 'edaD_PACIENTE'])

# Gráfica de dispersión
grafica_dispersion(df, 'edaD_PACIENTE', 'montO_TOTAL')
```

### 6. Estadísticas inferenciales
```python
from src.inferencia import test_normalidad, test_anova, intervalo_confianza

# Prueba de normalidad
test_normalidad(df, 'montO_TOTAL')

# ANOVA
test_anova(df, 'montO_TOTAL', 'clasE_EPISODIO')

# Intervalo de confianza
intervalo_confianza(df, 'montO_TOTAL', nivel_confianza=0.95)
```

### 7. Procesamiento de datos
```python
from src.procesamiento import (
    imputar_media,
    normalizar_datos,
    estandarizar_datos
)

# Imputar valores faltantes
df = imputar_media(df, ['montO_MEDICAMENTOS', 'montO_EXAMENES'])

# Normalizar datos (0-1)
df = normalizar_datos(df, ['montO_TOTAL'])

# Estandarizar datos (z-score)
df = estandarizar_datos(df, ['edaD_PACIENTE'])
```

## 📈 Resultados Esperados

Al ejecutar `python main.py`, obtendrás:

1. **Resumen de datos**: Total de episodios, distribuciones por aseguradora, clase y estado
2. **Estadísticas descriptivas**: Media, mediana, moda, varianza, desviación estándar, cuartiles
3. **Correlaciones**: Matrices de correlación (Pearson y Spearman) y covarianza
4. **Análisis inferencial**: Pruebas de normalidad, ANOVA, intervalos de confianza
5. **Archivos exportados**: CSV y Excel con los datos procesados

## 🔍 Casos de Uso

### Análisis de costos por aseguradora
```python
# Filtrar por aseguradora
df_sanitas = filtrar_por_categoria(df, 'aseguradora', ['SANITAS EPS'])

# Estadísticas de costos
medidas_centralidad(df_sanitas, 'montO_TOTAL')
```

### Detectar episodios atípicos (outliers)
```python
from src.filtros import filtrar_outliers

# Remover outliers usando IQR
df_sin_outliers = filtrar_outliers(df, 'montO_TOTAL', metodo='iqr')
```

### Comparar costos por clase de episodio
```python
# ANOVA para comparar medias
test_anova(df, 'montO_TOTAL', 'clasE_EPISODIO')

# Visualización
grafica_barras_categorias(df, 'clasE_EPISODIO', 'montO_TOTAL', agregacion='mean')
```

## 🛠️ Personalización

### Agregar nuevos datos
1. Editar `data/facturacion_medica.json` siguiendo la estructura existente
2. Ejecutar `python main.py` para procesar los nuevos datos

### Modificar análisis
- Editar los módulos en `src/` según tus necesidades
- Los cambios se reflejarán automáticamente en `main.py`

## 📝 Notas Importantes

1. **Valores nulos**: El sistema imputa automáticamente valores faltantes en `montO_MEDICAMENTOS` y `montO_EXAMENES` usando la media
2. **Prestaciones**: Cada episodio puede tener múltiples prestaciones asociadas
3. **Formatos**: Los datos se exportan automáticamente a CSV y Excel
4. **Visualizaciones**: Algunas gráficas están comentadas en `main.py` para evitar abrir múltiples ventanas. Descoméntalas según necesidad

## ⚠️ Solución de Problemas

### Error: "Module not found"
```powershell
pip install -r requirements.txt
```

### Error: "File not found"
Verifica que estés en el directorio correcto:
```powershell
cd ProyectoEstructuras
python main.py
```

### Visualizaciones no aparecen
Descomenta las líneas en `main.py` (líneas 280-282) o ejecuta:
```python
python -c "from src.visualizaciones import *; from src.carga_datos import cargar_json; df = cargar_json('data/facturacion_medica.json'); dashboard_completo(df)"
```

## 📞 Soporte

Para preguntas o problemas:
1. Revisa esta guía
2. Consulta la documentación en cada módulo (`src/*.py`)
3. Revisa los comentarios en el código

## ✅ Checklist de Componentes

- [x] Categorías: Montos y Órdenes
- [x] Ciclar, Normalizar y Estandarizar
- [x] Imputación
- [x] Búsqueda y Filtros
- [x] Pandas (DataFrame)
- [x] Carga de datos (CSV y Excel)
- [x] Matplotlib
- [x] Distribución de datos
- [x] Diagrama de Cajas
- [x] Gráficas Relacionales (Seaborn)
- [x] Centralidad
- [x] Cuartiles
- [x] Medida de dispersión
- [x] Correlación de Spearman
- [x] Análisis de Dispersión
- [x] Estadísticas Inferenciales
- [x] Matriz de Covarianza

¡Proyecto completo! 🎉
