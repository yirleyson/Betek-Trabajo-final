import random
from datetime import datetime, timedelta
import mysql.connector

# Conexión a la BD
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="banco"
)
cursor = conn.cursor()

def insertar_mora(n=100):
    # Obtener créditos disponibles
    cursor.execute("SELECT id_credito FROM producto_credito")
    creditos = [row[0] for row in cursor.fetchall()]

    if len(creditos) < n:
        n = len(creditos)  # Evitar error si hay menos créditos que n

    # Escoger créditos al azar
    creditos_mora = random.sample(creditos, n)

    registros = []
    for id_credito in creditos_mora:
        # Fecha vencida entre 1 y 12 meses atrás
        dias_atraso = random.randint(30, 365)
        fecha_vencida = datetime.now() - timedelta(days=dias_atraso)

        # Saldo en mora aleatorio
        saldo_mora = round(random.uniform(100000, 5000000), 2)

        # Proceso de recuperación
        proceso_recuperacion = random.choice(['SI', 'NO'])

        registros.append((fecha_vencida.date(), saldo_mora, proceso_recuperacion, id_credito))

    sql = """
    INSERT INTO mora (fecha_vencida, saldo_mora, proceso_recuperacion, id_credito)
    VALUES (%s, %s, %s, %s)
    """
    cursor.executemany(sql, registros)
    conn.commit()
    print(f"✅ {cursor.rowcount} registros insertados en mora")

# Ejecutar
insertar_mora(100)

cursor.close()
conn.close()
