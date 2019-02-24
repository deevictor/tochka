from django.db import connection

def truncate_tables(tables):
    cursor = connection.cursor()
    for table in tables:
        cursor.execute(f"TRUNCATE TABLE `{table}`")
