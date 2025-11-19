# Proyecto de Análisis de Facturación Médica

## Descripción
Análisis completo de episodios de facturación médica en formato JSON, incluyendo procesamiento de datos, visualizaciones y estadísticas.

## Requisitos
- Python 3.8+
- pandas
- numpy
- matplotlib
- seaborn
- scipy
- openpyxl

## Instalación
```bash
pip install -r requirements.txt
```

## Estructura del Proyecto
```
ProyectoEstructuras/
│
├── data/
│   ├── facturacion_medica.json
│   ├── facturacion_medica.csv
│   └── facturacion_medica.xlsx
│
├── src/
│   ├── carga_datos.py          # Carga de datos JSON, CSV y Excel
│   ├── procesamiento.py        # Normalización, estandarización, imputación
│   ├── filtros.py              # Búsqueda y filtros
│   ├── estadisticas.py         # Centralidad, dispersión, cuartiles
│   ├── correlaciones.py        # Spearman, covarianza
│   ├── visualizaciones.py      # Matplotlib, Seaborn
│   └── inferencia.py           # Estadísticas inferenciales
│
├── notebooks/
│   └── analisis_completo.ipynb
│
├── main.py
├── requirements.txt
└── README.md
```

## Componentes Implementados
✓ Carga de datos (JSON, CSV, Excel)
✓ Normalización y Estandarización
✓ Imputación de datos faltantes
✓ Búsqueda y Filtros
✓ Pandas y DataFrames
✓ Matplotlib para visualizaciones
✓ Distribución de datos
✓ Diagrama de cajas (boxplot)
✓ Gráficas relacionales (Seaborn)
✓ Medidas de centralidad
✓ Cuartiles
✓ Medidas de dispersión
✓ Correlación de Spearman
✓ Análisis de dispersión
✓ Estadísticas inferenciales
✓ Matriz de covarianza

## Uso
```bash
python main.py
```
