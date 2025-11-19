"""
Módulo para visualizaciones con Matplotlib y Seaborn
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


def grafica_distribucion(df, columna, bins=30, archivo_salida=None):
    """
    Crea un histograma para mostrar la distribución de datos
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columna (str): Columna a graficar
        bins (int): Número de intervalos
        archivo_salida (str): Ruta para guardar la imagen (opcional)
    """
    if columna not in df.columns:
        print(f"✗ Columna '{columna}' no encontrada")
        return
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Histograma
    axes[0].hist(df[columna].dropna(), bins=bins, edgecolor='black', alpha=0.7, color='steelblue')
    axes[0].set_xlabel(columna, fontweight='bold')
    axes[0].set_ylabel('Frecuencia', fontweight='bold')
    axes[0].set_title(f'Distribución de {columna}', fontsize=14, fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    
    # KDE (Kernel Density Estimation)
    df[columna].dropna().plot(kind='density', ax=axes[1], color='darkblue', linewidth=2)
    axes[1].set_xlabel(columna, fontweight='bold')
    axes[1].set_ylabel('Densidad', fontweight='bold')
    axes[1].set_title(f'Densidad de {columna}', fontsize=14, fontweight='bold')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if archivo_salida:
        plt.savefig(archivo_salida, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfica guardada en: {archivo_salida}")
    
    plt.show()


def diagrama_cajas(df, columnas=None, archivo_salida=None):
    """
    Crea diagramas de cajas (boxplot) para detectar outliers
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columnas (list): Lista de columnas a graficar
        archivo_salida (str): Ruta para guardar la imagen (opcional)
    """
    if columnas is None:
        columnas = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Filtrar columnas que existen
    columnas_validas = [col for col in columnas if col in df.columns]
    
    if not columnas_validas:
        print("✗ No hay columnas válidas para graficar")
        return
    
    n_cols = len(columnas_validas)
    n_rows = (n_cols + 2) // 3
    
    fig, axes = plt.subplots(n_rows, min(3, n_cols), figsize=(15, 5 * n_rows))
    
    if n_cols == 1:
        axes = [axes]
    else:
        axes = axes.flatten() if n_cols > 1 else [axes]
    
    for idx, col in enumerate(columnas_validas):
        sns.boxplot(data=df, y=col, ax=axes[idx], color='lightblue')
        axes[idx].set_title(f'Boxplot: {col}', fontweight='bold')
        axes[idx].set_ylabel(col, fontweight='bold')
        axes[idx].grid(True, alpha=0.3, axis='y')
    
    # Ocultar ejes extras
    for idx in range(len(columnas_validas), len(axes)):
        axes[idx].set_visible(False)
    
    plt.tight_layout()
    
    if archivo_salida:
        plt.savefig(archivo_salida, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfica guardada en: {archivo_salida}")
    
    plt.show()


def grafica_dispersion(df, columna_x, columna_y, hue=None, archivo_salida=None):
    """
    Crea gráfica de dispersión entre dos variables
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columna_x (str): Variable en eje X
        columna_y (str): Variable en eje Y
        hue (str): Columna para colorear puntos (opcional)
        archivo_salida (str): Ruta para guardar la imagen (opcional)
    """
    if columna_x not in df.columns or columna_y not in df.columns:
        print(f"✗ Una o ambas columnas no encontradas")
        return
    
    plt.figure(figsize=(10, 6))
    
    if hue and hue in df.columns:
        sns.scatterplot(data=df, x=columna_x, y=columna_y, hue=hue, 
                       palette='viridis', s=100, alpha=0.7)
    else:
        sns.scatterplot(data=df, x=columna_x, y=columna_y, 
                       color='steelblue', s=100, alpha=0.7)
    
    plt.xlabel(columna_x, fontweight='bold', fontsize=12)
    plt.ylabel(columna_y, fontweight='bold', fontsize=12)
    plt.title(f'Análisis de Dispersión: {columna_x} vs {columna_y}', 
             fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if archivo_salida:
        plt.savefig(archivo_salida, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfica guardada en: {archivo_salida}")
    
    plt.show()


def grafica_relacional_seaborn(df, columna_x, columna_y, hue=None, estilo='scatter', archivo_salida=None):
    """
    Crea gráficas relacionales avanzadas con Seaborn
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columna_x (str): Variable en eje X
        columna_y (str): Variable en eje Y
        hue (str): Columna para colorear (opcional)
        estilo (str): 'scatter' o 'line'
        archivo_salida (str): Ruta para guardar la imagen (opcional)
    """
    if columna_x not in df.columns or columna_y not in df.columns:
        print(f"✗ Una o ambas columnas no encontradas")
        return
    
    plt.figure(figsize=(12, 6))
    
    if estilo == 'scatter':
        sns.relplot(data=df, x=columna_x, y=columna_y, hue=hue, 
                   palette='deep', height=6, aspect=1.5, alpha=0.7)
    elif estilo == 'line':
        sns.relplot(data=df, x=columna_x, y=columna_y, hue=hue, 
                   kind='line', palette='deep', height=6, aspect=1.5)
    
    plt.xlabel(columna_x, fontweight='bold', fontsize=12)
    plt.ylabel(columna_y, fontweight='bold', fontsize=12)
    plt.title(f'Gráfica Relacional: {columna_x} vs {columna_y}', 
             fontsize=14, fontweight='bold')
    
    if archivo_salida:
        plt.savefig(archivo_salida, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfica guardada en: {archivo_salida}")
    
    plt.show()


def grafica_barras_categorias(df, columna_categoria, columna_valor=None, 
                               agregacion='count', archivo_salida=None):
    """
    Crea gráfica de barras para datos categóricos
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columna_categoria (str): Columna categórica
        columna_valor (str): Columna de valores a agregar (opcional)
        agregacion (str): 'count', 'sum', 'mean', 'median'
        archivo_salida (str): Ruta para guardar la imagen (opcional)
    """
    if columna_categoria not in df.columns:
        print(f"✗ Columna '{columna_categoria}' no encontrada")
        return
    
    plt.figure(figsize=(12, 6))
    
    if agregacion == 'count':
        datos = df[columna_categoria].value_counts().sort_values(ascending=False)
        sns.barplot(x=datos.index, y=datos.values, palette='viridis')
        plt.ylabel('Cantidad', fontweight='bold', fontsize=12)
    elif columna_valor and columna_valor in df.columns:
        if agregacion == 'sum':
            datos = df.groupby(columna_categoria)[columna_valor].sum().sort_values(ascending=False)
        elif agregacion == 'mean':
            datos = df.groupby(columna_categoria)[columna_valor].mean().sort_values(ascending=False)
        elif agregacion == 'median':
            datos = df.groupby(columna_categoria)[columna_valor].median().sort_values(ascending=False)
        
        sns.barplot(x=datos.index, y=datos.values, palette='mako')
        plt.ylabel(f'{agregacion.capitalize()} de {columna_valor}', fontweight='bold', fontsize=12)
    else:
        print(f"✗ Columna de valores '{columna_valor}' no encontrada")
        return
    
    plt.xlabel(columna_categoria, fontweight='bold', fontsize=12)
    plt.title(f'Análisis por {columna_categoria}', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    
    if archivo_salida:
        plt.savefig(archivo_salida, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfica guardada en: {archivo_salida}")
    
    plt.show()


def pairplot_seaborn(df, columnas=None, hue=None, archivo_salida=None):
    """
    Crea matriz de gráficas de relaciones entre múltiples variables
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columnas (list): Lista de columnas a incluir
        hue (str): Columna para colorear (opcional)
        archivo_salida (str): Ruta para guardar la imagen (opcional)
    """
    if columnas:
        df_subset = df[columnas + ([hue] if hue and hue not in columnas else [])]
    else:
        df_subset = df.select_dtypes(include=[np.number])
    
    g = sns.pairplot(df_subset, hue=hue, palette='husl', 
                     plot_kws={'alpha': 0.6}, diag_kind='kde', height=2.5)
    g.fig.suptitle('Matriz de Relaciones entre Variables', 
                   fontsize=16, fontweight='bold', y=1.01)
    
    if archivo_salida:
        plt.savefig(archivo_salida, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfica guardada en: {archivo_salida}")
    
    plt.show()


def dashboard_completo(df, archivo_salida=None):
    """
    Crea un dashboard completo con múltiples visualizaciones
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        archivo_salida (str): Ruta para guardar la imagen (opcional)
    """
    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # 1. Distribución de montos
    ax1 = fig.add_subplot(gs[0, :2])
    if 'montO_TOTAL' in df.columns:
        df['montO_TOTAL'].hist(bins=30, ax=ax1, color='steelblue', edgecolor='black', alpha=0.7)
        ax1.set_title('Distribución de Montos Totales', fontweight='bold', fontsize=12)
        ax1.set_xlabel('Monto Total', fontweight='bold')
        ax1.set_ylabel('Frecuencia', fontweight='bold')
        ax1.grid(True, alpha=0.3)
    
    # 2. Boxplot edades
    ax2 = fig.add_subplot(gs[0, 2])
    if 'edaD_PACIENTE' in df.columns:
        sns.boxplot(data=df, y='edaD_PACIENTE', ax=ax2, color='lightcoral')
        ax2.set_title('Distribución Edades', fontweight='bold', fontsize=12)
        ax2.grid(True, alpha=0.3, axis='y')
    
    # 3. Top aseguradoras
    ax3 = fig.add_subplot(gs[1, :])
    if 'aseguradora' in df.columns:
        top_aseg = df['aseguradora'].value_counts().head(10)
        sns.barplot(x=top_aseg.values, y=top_aseg.index, ax=ax3, palette='viridis')
        ax3.set_title('Top 10 Aseguradoras', fontweight='bold', fontsize=12)
        ax3.set_xlabel('Número de Episodios', fontweight='bold')
        ax3.grid(True, alpha=0.3, axis='x')
    
    # 4. Dispersión edad vs monto
    ax4 = fig.add_subplot(gs[2, 0])
    if 'edaD_PACIENTE' in df.columns and 'montO_TOTAL' in df.columns:
        ax4.scatter(df['edaD_PACIENTE'], df['montO_TOTAL'], alpha=0.5, color='purple')
        ax4.set_title('Edad vs Monto Total', fontweight='bold', fontsize=12)
        ax4.set_xlabel('Edad Paciente', fontweight='bold')
        ax4.set_ylabel('Monto Total', fontweight='bold')
        ax4.grid(True, alpha=0.3)
    
    # 5. Duración por clase de episodio
    ax5 = fig.add_subplot(gs[2, 1])
    if 'clasE_EPISODIO' in df.columns and 'duracioN_MINUTOS' in df.columns:
        df.groupby('clasE_EPISODIO')['duracioN_MINUTOS'].mean().plot(kind='bar', ax=ax5, color='orange')
        ax5.set_title('Duración Promedio por Clase', fontweight='bold', fontsize=12)
        ax5.set_xlabel('Clase Episodio', fontweight='bold')
        ax5.set_ylabel('Minutos', fontweight='bold')
        ax5.grid(True, alpha=0.3, axis='y')
        ax5.tick_params(axis='x', rotation=0)
    
    # 6. Estado factura
    ax6 = fig.add_subplot(gs[2, 2])
    if 'staT_FACTURA' in df.columns:
        df['staT_FACTURA'].value_counts().plot(kind='pie', ax=ax6, autopct='%1.1f%%', 
                                               colors=['lightgreen', 'lightcoral'])
        ax6.set_title('Estado de Facturas', fontweight='bold', fontsize=12)
        ax6.set_ylabel('')
    
    fig.suptitle('Dashboard de Análisis de Facturación Médica', 
                fontsize=18, fontweight='bold', y=0.995)
    
    if archivo_salida:
        plt.savefig(archivo_salida, dpi=300, bbox_inches='tight')
        print(f"✓ Dashboard guardado en: {archivo_salida}")
    
    plt.show()


if __name__ == "__main__":
    from carga_datos import cargar_json
    
    # Cargar datos
    df = cargar_json('../data/facturacion_medica.json')
    
    if df is not None:
        print("\n--- GENERANDO VISUALIZACIONES ---\n")
        
        # Crear dashboard completo
        dashboard_completo(df)
        
        # Distribución de montos
        if 'montO_TOTAL' in df.columns:
            grafica_distribucion(df, 'montO_TOTAL')
        
        # Diagrama de cajas
        columnas_numericas = ['montO_TOTAL', 'edaD_PACIENTE', 'duracioN_MINUTOS']
        diagrama_cajas(df, columnas_numericas)
