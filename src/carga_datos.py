"""
Módulo para carga de datos desde diferentes formatos (JSON, CSV, Excel)
"""
import pandas as pd
import json


def cargar_json(ruta_archivo):
    """
    Carga datos desde archivo JSON
    
    Args:
        ruta_archivo (str): Ruta al archivo JSON
        
    Returns:
        pd.DataFrame: DataFrame con los datos cargados
    """
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as file:
            datos = json.load(file)
        df = pd.DataFrame(datos)
        print(f"✓ Datos cargados exitosamente desde JSON: {len(df)} registros")
        return df
    except Exception as e:
        print(f"✗ Error al cargar JSON: {e}")
        return None


def cargar_csv(ruta_archivo):
    """
    Carga datos desde archivo CSV
    
    Args:
        ruta_archivo (str): Ruta al archivo CSV
        
    Returns:
        pd.DataFrame: DataFrame con los datos cargados
    """
    try:
        df = pd.read_csv(ruta_archivo, encoding='utf-8')
        print(f"✓ Datos cargados exitosamente desde CSV: {len(df)} registros")
        return df
    except Exception as e:
        print(f"✗ Error al cargar CSV: {e}")
        return None


def cargar_excel(ruta_archivo, hoja=0):
    """
    Carga datos desde archivo Excel
    
    Args:
        ruta_archivo (str): Ruta al archivo Excel
        hoja (int/str): Nombre o índice de la hoja a cargar
        
    Returns:
        pd.DataFrame: DataFrame con los datos cargados
    """
    try:
        df = pd.read_excel(ruta_archivo, sheet_name=hoja)
        print(f"✓ Datos cargados exitosamente desde Excel: {len(df)} registros")
        return df
    except Exception as e:
        print(f"✗ Error al cargar Excel: {e}")
        return None


def exportar_a_csv(df, ruta_archivo):
    """
    Exporta DataFrame a CSV
    
    Args:
        df (pd.DataFrame): DataFrame a exportar
        ruta_archivo (str): Ruta del archivo de destino
    """
    try:
        df.to_csv(ruta_archivo, index=False, encoding='utf-8')
        print(f"✓ Datos exportados exitosamente a CSV: {ruta_archivo}")
    except Exception as e:
        print(f"✗ Error al exportar CSV: {e}")


def exportar_a_excel(df, ruta_archivo, nombre_hoja='Datos'):
    """
    Exporta DataFrame a Excel
    
    Args:
        df (pd.DataFrame): DataFrame a exportar
        ruta_archivo (str): Ruta del archivo de destino
        nombre_hoja (str): Nombre de la hoja
    """
    try:
        df.to_excel(ruta_archivo, sheet_name=nombre_hoja, index=False)
        print(f"✓ Datos exportados exitosamente a Excel: {ruta_archivo}")
    except Exception as e:
        print(f"✗ Error al exportar Excel: {e}")


def info_dataframe(df):
    """
    Muestra información general del DataFrame
    
    Args:
        df (pd.DataFrame): DataFrame a analizar
    """
    print("\n" + "="*60)
    print("INFORMACIÓN DEL DATAFRAME")
    print("="*60)
    print(f"Dimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
    print(f"\nColumnas: {list(df.columns)}")
    print(f"\nTipos de datos:")
    print(df.dtypes)
    print(f"\nValores nulos:")
    print(df.isnull().sum())
    print(f"\nPrimeras 5 filas:")
    print(df.head())
    print("="*60 + "\n")


if __name__ == "__main__":
    # Ejemplo de uso
    df = cargar_json('../data/facturacion_medica.json')
    if df is not None:
        info_dataframe(df)
        exportar_a_csv(df, '../data/facturacion_medica.csv')
        exportar_a_excel(df, '../data/facturacion_medica.xlsx')
