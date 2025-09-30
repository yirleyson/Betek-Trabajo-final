import mysql.connector
from faker import Faker
import random

# Conexión a MySQL
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="banco"
)
cursor = conexion.cursor()
faker = Faker("es_CO")  # Datos realistas en español de Colombia

# ==========================
# 1. Insertar sucursales
# ==========================
def insertar_sucursales():
    sucursales_fijas = [
        ("Sucursal Medellín", "Calle 10 #20-30", "Medellín", "6041234567"),
        ("Sucursal Bogotá", "Cra 15 #45-67", "Bogotá", "6017654321"),
        ("Sucursal Cali", "Av. Roosevelt #25-50", "Cali", "6021112233"),
        ("Sucursal Barranquilla", "Calle 72 #53-45", "Barranquilla", "6053334444"),
        ("Sucursal Cartagena", "Cra 2 #31-45", "Cartagena", "6057778888")
    ]

    sql = """INSERT INTO sucursal (nombre_sucursal, direccion, ciudad, telefono, fecha_apertura)
             VALUES (%s, %s, %s, %s, %s)"""

    for suc in sucursales_fijas:
        cursor.execute(sql, (suc[0], suc[1], suc[2], suc[3], faker.date_between(start_date="-20y", end_date="today")))
    
    conexion.commit()
    print("✅ Sucursales insertadas")

# ==========================
# 2. Insertar empleados
# ==========================
def insertar_empleados(n):
    sql = """INSERT INTO empleados
             (cedula_empleado, nombre, apellido, fecha_nacimiento, correo,
              direccion, celular, fecha_contratacion, cargo, salario, id_sucursal)
             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

    cargos = ["vendedor", "gerente", "asesor"]

    for _ in range(n):
        cedula = faker.unique.random_number(digits=10)
        nombre = faker.first_name()
        apellido = faker.last_name()
        fecha_nac = faker.date_of_birth(minimum_age=25, maximum_age=60)
        correo = faker.unique.email()
        direccion = faker.address()
        celular = faker.msisdn()[:10]
        fecha_contratacion = faker.date_between(start_date="-10y", end_date="today")
        cargo = random.choice(cargos)
        salario = round(random.uniform(1500000, 8000000), 2)
        id_sucursal = random.randint(1, 5)  # asegura que siempre apunte a sucursal existente

        valores = (cedula, nombre, apellido, fecha_nac, correo,
                   direccion, celular, fecha_contratacion, cargo,
                   salario, id_sucursal)

        cursor.execute(sql, valores)

    conexion.commit()
    print(f"✅ {n} empleados insertados")

# ==========================
# 3. Insertar clientes
# ==========================
def insertar_clientes(n):
    sql = """INSERT INTO clientes
             (cedula_cliente, nombre, apellido, fecha_nacimiento, correo,
              direccion, celular, fecha_registro, genero)
             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

    generos = ["Masculino", "Femenino"]

    for _ in range(n):
        cedula = faker.unique.random_number(digits=10)
        nombre = faker.first_name()
        apellido = faker.last_name()
        fecha_nac = faker.date_of_birth(minimum_age=18, maximum_age=80)
        correo = faker.unique.email()
        direccion = faker.address()
        celular = faker.msisdn()[:10]
        fecha_registro = faker.date_between(start_date="-5y", end_date="today")
        genero = random.choice(generos)

        valores = (cedula, nombre, apellido, fecha_nac, correo,
                   direccion, celular, fecha_registro, genero)

        cursor.execute(sql, valores)

    conexion.commit()
    print(f"✅ {n} clientes insertados")


# ==========================
# Ejecutar
# ==========================
insertar_sucursales()    # 5 sucursales
insertar_empleados(50)   # 50 empleados
insertar_clientes(1000)  # 1000 clientes

cursor.close()
conexion.close()
