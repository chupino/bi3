# sakila_analysis.py
import pandas as pd
from sqlalchemy import create_engine

# Configuración de la conexión
DATABASE_URL = 'mysql+pymysql://sakila:password@mysql/sakila'
engine = create_engine(DATABASE_URL)

def load_table(table_name):
    """Carga una tabla de la base de datos a un DataFrame de pandas."""
    return pd.read_sql_table(table_name, con=engine)

def print_customer_statistics():
    """Imprime estadísticas de la tabla Cliente (Customer)."""
    df_customer = load_table('customer')
    print("Estadísticas de la tabla Customer:")
    print(df_customer.describe(include='all'))

def print_payment_central_tendencies():
    """Imprime las tres operaciones de tendencia central de la tabla Pagos (Payment)."""
    df_payment = load_table('payment')
    print("\nTendencia central de la tabla Payment:")
    print("Media (mean):", df_payment['amount'].mean())
    print("Mediana (median):", df_payment['amount'].median())
    print("Moda (mode):", df_payment['amount'].mode()[0])

def print_film_central_tendencies():
    """Imprime las tres operaciones de tendencia central de la tabla Película (Film) para el campo Replacement_cost."""
    df_film = load_table('film')
    print("\nTendencia central de la tabla Film (Replacement_cost):")
    print("Media (mean):", df_film['replacement_cost'].mean())
    print("Mediana (median):", df_film['replacement_cost'].median())
    print("Moda (mode):", df_film['replacement_cost'].mode()[0])

def print_payment_central_tendencies_peru():
    """Imprime las tres operaciones de tendencia central de la tabla Pagos (Payment) para clientes de Perú."""
    df_payment = load_table('payment')
    df_customer = load_table('customer')
    df_address = load_table('address')
    df_city = load_table('city')

    # Unir las tablas para obtener la información de dirección y ciudad
    df_address = df_address.merge(df_city[['city_id', 'country_id']], on='city_id')
    df_customer = df_customer.merge(df_address[['address_id', 'city_id']], on='address_id')
    df_customer = df_customer.merge(df_payment[['customer_id', 'amount']], on='customer_id')
    df_peru_customers = df_customer[df_customer['country_id'] == 1]  # Asumiendo que el country_id para Perú es 1

    print("\nTendencia central de la tabla Payment para clientes de Perú (Cantidad):")
    print("Media (mean):", df_peru_customers['amount'].mean())
    print("Mediana (median):", df_peru_customers['amount'].median())
    print("Moda (mode):", df_peru_customers['amount'].mode()[0])

if __name__ == "__main__":
    print_customer_statistics()
    print_payment_central_tendencies()
    print_film_central_tendencies()
    print_payment_central_tendencies_peru()