import random
import datetime
import mysql.connector

# Conexión a la BD
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="banco"
)
cursor = conexion.cursor()

# -------------------------------
# Insertar productos base
# -------------------------------
def insertar_productos():
    productos = [
        ("Cuenta de Ahorros", "debito"),
        ("Cuenta Corriente", "debito"),
        ("Tarjeta Débito Virtual", "virtual"),
        ("Tarjeta de Crédito Clásica", "credito"),
        ("Tarjeta de Crédito Oro", "credito"),
        ("Tarjeta de Crédito Platino", "credito"),
        ("Tarjeta Prepago Virtual", "virtual"),
        ("Cuenta Nómina", "debito"),
        ("Tarjeta Crédito Empresarial", "credito"),
        ("Cuenta Premium", "debito")
    ]
    sql = "INSERT INTO producto (nombre_producto, tipo_producto) VALUES (%s, %s)"
    cursor.executemany(sql, productos)
    conexion.commit()
    print(f"{cursor.rowcount} productos insertados.")

# -------------------------------
# Insertar contratos ajustados
# -------------------------------
def insertar_contratos():
    cursor.execute("SELECT id_producto, tipo_producto FROM producto")
    productos = cursor.fetchall()  # lista de (id_producto, tipo_producto)

    cursor.execute("SELECT cedula_cliente FROM clientes")
    clientes = [c[0] for c in cursor.fetchall()]

    cursor.execute("SELECT cedula_empleado FROM empleados")
    empleados = [e[0] for e in cursor.fetchall()]

    contratos = []

    for cliente in clientes:
        # cada cliente recibe al menos 1 producto
        num_productos = 1

        # algunos clientes reciben productos adicionales
        if random.random() < 0.4:   # 40% probabilidad
            num_productos += random.randint(1, 3)  # hasta 3 adicionales

        productos_asignados = random.sample(productos, min(num_productos, len(productos)))

        for prod in productos_asignados:
            contratos.append((
                datetime.date.today() - datetime.timedelta(days=random.randint(0, 365)),
                prod[0],              # id_producto
                cliente,              # cedula_cliente existente
                random.choice(empleados)  # empleado existente
            ))

    sql = """
        INSERT INTO contrato_producto (fecha_registro, id_producto, cedula_cliente, cedula_empleado)
        VALUES (%s, %s, %s, %s)
    """
    cursor.executemany(sql, contratos)
    conexion.commit()
    print(f"{cursor.rowcount} contratos insertados.")

# -------------------------------
# Insertar productos de crédito
# -------------------------------
def insertar_productos_credito():
    cursor.execute("""
        SELECT cp.id_contrato_producto 
        FROM contrato_producto cp
        JOIN producto p ON cp.id_producto = p.id_producto
        WHERE p.tipo_producto = 'credito'
    """)
    contratos_credito = [c[0] for c in cursor.fetchall()]

    productos_credito = []
    for contrato in contratos_credito:
        limite = random.choice([3000000, 5000000, 10000000, 20000000])
        saldo = random.randint(0, limite)
        cuota = random.randint(200000, 800000)
        productos_credito.append((
            random.choice(['activo','bloqueado','vencido','cancelado','mora']),
            limite,
            saldo,
            cuota,
            datetime.date.today() + datetime.timedelta(days=random.randint(30, 365)),
            random.randint(20000, 60000),
            round(random.uniform(1.5, 3.0), 2),
            contrato
        ))

    sql = """
        INSERT INTO producto_credito
        (estado, limite_credito, saldo_pendiente, valor_cuota, fecha_vencimiento,
         cuota_manejo, tasa_interes, id_contrato_producto)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """
    cursor.executemany(sql, productos_credito)
    conexion.commit()
    print(f"{cursor.rowcount} productos_credito insertados.")

# -------------------------------
# Insertar productos de inversión
# -------------------------------
def insertar_productos_inversion():
    cursor.execute("""
        SELECT cp.id_contrato_producto 
        FROM contrato_producto cp
        JOIN producto p ON cp.id_producto = p.id_producto
        WHERE p.tipo_producto = 'virtual'
    """)
    contratos_inv = [c[0] for c in cursor.fetchall()]

    productos_inv = []
    for contrato in contratos_inv:
        productos_inv.append((
            random.choice(['activo','bloqueado','vencido','cancelado']),
            random.randint(1000000, 20000000),
            random.choice(['3 meses','6 meses','12 meses','fecha vencida']),
            datetime.date.today() + datetime.timedelta(days=random.randint(90, 365)),
            round(random.uniform(2.0, 8.0), 2),
            random.choice(['bajo','medio','alto']),
            contrato
        ))

    sql = """
        INSERT INTO producto_inversion
        (estado, saldo_total, retiros, fecha_vencimiento, tasa_rendimiento, nivel_riesgo, id_contrato_producto)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """
    cursor.executemany(sql, productos_inv)
    conexion.commit()
    print(f"{cursor.rowcount} productos_inversion insertados.")

# -------------------------------
# Insertar productos de captación
# -------------------------------
def insertar_productos_captacion():
    cursor.execute("""
        SELECT cp.id_contrato_producto 
        FROM contrato_producto cp
        JOIN producto p ON cp.id_producto = p.id_producto
        WHERE p.tipo_producto = 'debito'
    """)
    contratos_cap = [c[0] for c in cursor.fetchall()]

    productos_cap = []
    for contrato in contratos_cap:
        productos_cap.append((
            random.choice(['activo','bloqueado','vencido','cancelado']),
            random.randint(500000, 10000000),
            round(random.uniform(1.0, 4.5), 2),
            contrato
        ))

    sql = """
        INSERT INTO producto_captacion
        (estado, saldo_total, tasa_rendimiento, id_contrato_producto)
        VALUES (%s,%s,%s,%s)
    """
    cursor.executemany(sql, productos_cap)
    conexion.commit()
    print(f"{cursor.rowcount} productos_captacion insertados.")

# -------------------------------
# Insertar transacciones
# -------------------------------
def insertar_transacciones(num_trans=150):
    cursor.execute("SELECT id_contrato_producto FROM contrato_producto")
    contratos = [c[0] for c in cursor.fetchall()]

    transacciones = []
    for _ in range(num_trans):
        transacciones.append((
            datetime.date.today() - datetime.timedelta(days=random.randint(0, 365)),
            random.randint(20000, 5000000),
            random.choice(['deposito','retiro','transferencia','pago factura','compra con tarjeta','giro internacional']),
            random.choice(['APP','WEB','SUCURSAL','ATM']),
            random.choice(contratos)  # SIEMPRE contrato existente
        ))

    sql = """
        INSERT INTO transaccion
        (fecha_transaccion, valor_transaccion, tipo_transaccion, canal, id_contrato_producto)
        VALUES (%s,%s,%s,%s,%s)
    """
    cursor.executemany(sql, transacciones)
    conexion.commit()
    print(f"{cursor.rowcount} transacciones insertadas.")

# -------------------------------
# Ejecución
# -------------------------------
insertar_productos()
insertar_contratos()
insertar_productos_credito()
insertar_productos_inversion()
insertar_productos_captacion()
insertar_transacciones()

cursor.close()
conexion.close()
