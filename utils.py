import datetime
import pymysql
import pandas as pd

def write_df_to_mysql(df, table_name, user, password, host, database, trunc = False):
    """
    Writes a pandas DataFrame to a MySQL table.

    Args:
        df (pd.DataFrame): The DataFrame to write to the MySQL table.
        table_name (str): The name of the table in MySQL.
        user (str): MySQL username.
        password (str): MySQL password.
        host (str): MySQL host.
        database (str): MySQL database name.
    """
    try:

        # Create a connection to MySQL
        connection = pymysql.connect(
            user=user,
            password=password,
            host=host,
            database=database
        )

        # Create a cursor object
        cursor = connection.cursor()

        # Create the table if it does not exist
        columns = ', '.join([f"{col} VARCHAR(255)" for col in df.columns])
        if table_name == "faulted_jobs":
            print(df.columns)
            print(df.head)
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {columns}
        )
        """
        cursor.execute(create_table_query)

        if trunc:
            cursor.execute(f"TRUNCATE TABLE {table_name}")

        # Prepare the INSERT statement
        placeholders = ', '.join(['%s'] * len(df.columns))
        insert_query = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({placeholders})"

        # Insert DataFrame rows into the table
        for row in df.itertuples(index=False, name=None):
            cursor.execute(insert_query, row)

        # Commit the transaction
        connection.commit()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        print(f" DataFrame written to {table_name} table in MySQL.")
    except Exception as e:
        print("Error during db operation : "+str(e))


def now():
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

