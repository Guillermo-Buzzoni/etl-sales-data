import time
import pandas as pd
import psycopg2

# Constantes Globales
MAX_RETRIES = 5
RETRY_DELAY = 5

def extract_products(df):
    """Extraer productos únicos y agregar un identificador."""
    df_products = df[['Product', 'Price Each', 'Cost price']].drop_duplicates()
    df_products['Product_id'] = range(1, len(df_products) + 1)
    return df_products[['Product_id', 'Product', 'Price Each', 'Cost price']]

def extract_addresses(df):
    """Extraer direcciones únicas y agregar un identificador."""
    df_addresses = df[['Purchase Address']].drop_duplicates()
    df_addresses['Google_Maps'] = 'https://www.google.com/maps/place/' + df_addresses['Purchase Address'].str.replace(' ', '+')
    df_addresses['Address_id'] = range(1, len(df_addresses) + 1)
    return df_addresses[['Address_id', 'Purchase Address', 'Google_Maps']]

def transform_sales_data(df, df_products, df_direcciones):
    """Combinar los datos de ventas con los identificadores de productos y direcciones."""
    df = df.merge(df_products, on='Product', how='left')
    df = df.merge(df_direcciones, left_on='Purchase Address', right_on='Purchase Address', how='left')
    df['Sale_id'] = range(1, len(df) + 1)
    return df[['Sale_id', 'Order Date', 'Order ID', 'Product_id', 'Address_id', 'Quantity Ordered', 'turnover']]

def insert_into_db(df, table_name, columns, connection):
    """Insertar datos desde un dataframe en una tabla de la base de datos."""
    cursor = connection.cursor()
    tuples = [row for row in df.itertuples(index=False, name=None)]
    values = ','.join(['%s'] * len(tuples[0]))
    query = f'INSERT INTO {table_name} ({",".join(columns)}) VALUES ({values})'
    cursor.executemany(query, tuples)
    connection.commit()
    cursor.close()

def connect_to_db():
    """Establecer conexión con la base de datos, con reintento en caso de fallo."""
    retries = 0
    while retries < MAX_RETRIES:
        try:
            conn = psycopg2.connect(
                host='db',
                port=5432,
                database='sales',
                user='root',
                password='root'
            )
            return conn
        except psycopg2.OperationalError:
            retries += 1
            print(f"Error al conectarse a la base de datos. Intento {retries}/{MAX_RETRIES}. Esperando {RETRY_DELAY} segundos antes de volver a intentar.")
            time.sleep(RETRY_DELAY)
    raise Exception("No se pudo establecer conexión con la base de datos después de varios intentos.")

if __name__ == '__main__':
    df = pd.read_csv('sales_data.csv')
    df_products = extract_products(df)
    df_addresses = extract_addresses(df)
    df_sales = transform_sales_data(df, df_products, df_addresses)

    conn = connect_to_db()
    
    insert_into_db(df_products, 'producto', ['id_producto', 'producto', 'precio', 'costo'], conn)
    insert_into_db(df_addresses, 'direccion_compra', ['id_direccion', 'direccion', 'enlace_maps'], conn)
    insert_into_db(df_sales, 'ventas', ['id_venta', 'fecha_orden', 'id_orden','id_producto', 'id_direccion', 'cantidad_ordenada', 'ingresos'], conn)

    conn.close()