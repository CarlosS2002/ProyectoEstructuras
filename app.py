from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src import carga_datos, estadisticas, correlaciones, visualizaciones, procesamiento, filtros, inferencia
import pandas as pd
import numpy as np
import json

app = Flask(__name__, 
            template_folder='web_app/templates',
            static_folder='web_app/static')
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analizar', methods=['POST'])
def analizar():
    try:
        data = request.get_json()
        
        facturas_data = data.get('facturas')
        admisiones_data = data.get('admisiones')
        
        resultados = {
            'success': True,
            'overview': {},
            'facturas': {},
            'admisiones': {},
            'prestaciones': {},
            'estadisticas': {}
        }
        
        # Procesar facturas
        if facturas_data:
            facturas_df = procesar_facturas(facturas_data)
            resultados['facturas'] = analizar_facturas(facturas_df)
        
        # Procesar admisiones
        if admisiones_data:
            admisiones_df = procesar_admisiones(admisiones_data)
            resultados['admisiones'] = analizar_admisiones(admisiones_df)
        
        # Overview combinado
        resultados['overview'] = {
            'totalEpisodios': len(admisiones_df) if admisiones_data else 0,
            'totalFacturas': len(facturas_df) if facturas_data else 0,
            'totalPrestaciones': resultados['facturas'].get('totalPrestaciones', 0),
            'montoTotal': float(resultados['facturas'].get('montoTotal', 0))
        }
        
        return jsonify(resultados)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def procesar_facturas(facturas_data):
    """Expandir prestaciones de facturas"""
    datos = facturas_data.get('datos', [])
    prestaciones_list = []
    
    for factura in datos:
        if 'prestaciones' in factura and isinstance(factura['prestaciones'], list):
            for prest in factura['prestaciones']:
                prest_expandida = {
                    'episodio': factura.get('episodio'),
                    'nro_factura': factura.get('nrO_FACTURA'),
                    'fecha_factura': factura.get('fechA_FACTURA'),
                    'centro_sanitario': factura.get('centrO_SANITARIO'),
                    **prest
                }
                prestaciones_list.append(prest_expandida)
    
    df = pd.DataFrame(prestaciones_list)
    
    # Convertir valores numéricos
    if 'valoR_NETO' in df.columns:
        df['valor_neto_num'] = pd.to_numeric(df['valoR_NETO'], errors='coerce')
    
    return df

def procesar_admisiones(admisiones_data):
    """Procesar datos de admisiones"""
    datos = admisiones_data.get('datos', [])
    df = pd.DataFrame(datos)
    return df

def analizar_facturas(df):
    """Análisis estadístico de facturas con numpy/pandas"""
    if df.empty or 'valor_neto_num' not in df.columns:
        return {'exists': False}
    
    montos = df['valor_neto_num'].dropna()
    
    # Estadísticas con numpy
    stats = {
        'mean': float(np.mean(montos)),
        'median': float(np.median(montos)),
        'std': float(np.std(montos, ddof=1)),
        'min': float(np.min(montos)),
        'max': float(np.max(montos)),
        'q1': float(np.percentile(montos, 25)),
        'q3': float(np.percentile(montos, 75)),
        'cv': float((np.std(montos, ddof=1) / np.mean(montos)) * 100)
    }
    
    # Agrupar por tipo
    prestaciones_por_tipo = {}
    if 'tipO_PRESTACION' in df.columns:
        prestaciones_por_tipo = df['tipO_PRESTACION'].value_counts().to_dict()
    
    # Top 10 más costosas
    top_prestaciones = df.nlargest(10, 'valor_neto_num')[
        ['noM_PRESTACION', 'tipO_PRESTACION', 'valoR_NETO']
    ].to_dict('records')
    
    return {
        'exists': True,
        'total': len(df),
        'totalPrestaciones': len(df),
        'montoTotal': float(montos.sum()),
        'montoPromedio': float(montos.mean()),
        'estadisticas': stats,
        'prestacionesPorTipo': prestaciones_por_tipo,
        'topPrestaciones': top_prestaciones,
        'montos': montos.tolist()
    }

def analizar_admisiones(df):
    """Análisis de admisiones"""
    if df.empty:
        return {'exists': False}
    
    # Agrupar por aseguradora
    por_aseguradora = df['aseguradora'].value_counts().to_dict() if 'aseguradora' in df.columns else {}
    
    # Agrupar por clase
    por_clase = df['clasE_EPISODIO'].value_counts().to_dict() if 'clasE_EPISODIO' in df.columns else {}
    
    # Agrupar por estado
    por_estado = df['staT_FACTURA'].value_counts().to_dict() if 'staT_FACTURA' in df.columns else {}
    
    return {
        'exists': True,
        'total': len(df),
        'porAseguradora': por_aseguradora,
        'porClase': por_clase,
        'porEstado': por_estado
    }

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
