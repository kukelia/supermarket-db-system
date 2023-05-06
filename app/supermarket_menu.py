import os
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from time import sleep

POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

#using db service's name as dns hostname
engine = create_engine(f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}',
                        connect_args={'options': '-csearch_path=supermarketdb'},
                        poolclass=StaticPool) #static because there'll be only 1 connection at a time


#USE COMMITS

table_names = [0,"clientes", "productos", "ventas", 'empleados','venta_detalle']
pks = [0,"dni", "id_producto", "id_compra"]
 
    
def ver():
    entity = int(input("""elija que desea ver:
    1- clientes
    2- productos
    3- ventas
    """))
    id = int(input("seleccione el id del elemento a visualizar: "))
    #what if none?
    conn.execute(f"SELECT * FROM {table_names[entity]} WHERE {pks[entity]} = {id};") 
    if conn.rowcount == 0:
        print(f"ningun resultado con {pks[entity]} igual a {id}")
        return
    else:
        print(conn.fetchone())
        return


def agregar_producto():
    id = input("ingrese id: ")
    conn.execute(f"SELECT * FROM productos WHERE id_producto = {id};")
    if conn.rowcount == 0:
        nombre = input("ingrese nombre producto: ")
        precio = input("ingrese precio: ")
        cat = input("ingrese categoria: ")
        conn.execute( f"INSERT INTO productos VALUES ({id}, '{nombre}', {precio}, '{cat}');")
    else:
        print("el producto ya existe")


def realizar_venta():

    global carrito
    dni = input("ingrese dni cliente: ")
    conn.execute(f"SELECT * FROM clientes WHERE dni = {dni};")
    if conn.rowcount == 0:
        print("el cliente no existe, debera ser agregado")
        agregar_cliente(dni)
    
    conn.execute("BEGIN;")
    conn.execute(f"""INSERT INTO ventas (dni_cliente, dni_empleado)
                    VALUES ({dni}, {dni_empleado}) RETURNING *""")
    id_venta = conn.fetchone()[0]
    for id_producto in carrito:
        conn.execute(f"""
                            INSERT INTO venta_detalle (id_venta, id_producto)
                            VALUES ({id_venta}, {id_producto}) RETURNING producto_vendido ;""")
        id_producto_vendido = conn.fetchone()[0] 
    
        conn.execute(f"""       
                            with precio_actual as
                            (SELECT precio FROM productos WHERE id_producto={id_producto})
                            UPDATE venta_detalle
                            SET precio_compra = precio_actual.precio FROM precio_actual
                            WHERE producto_vendido = {id_producto_vendido}
                            """)

    conn.execute(f"""
                SELECT sum FROM(
                    SELECT venta_detalle.id_compra, SUM(productos.precio)
                    FROM venta_detalle
                    INNER JOIN productos ON venta_detalle.id_producto = productos.id_producto
                    GROUP BY venta_detalle.id_compra
        ) as result_table
    where result_table.id_compra={id_compra}
    """)
    precio_total = conn.fetchone()[0]
    conn.execute(f"UPDATE compras SET precio_total={precio_total} WHERE id_compra={id_compra}")

    conn.execute("COMMIT;")
    carrito= []
    


def agregar_carrito():
    id = input("ingrese id: ")
    conn.execute(f"SELECT * FROM productos WHERE id_producto = {id};")
    if conn.rowcount == 0:
        print("no existe ese producto")
        return
    else:
        carrito.append(id)



def eliminar_producto():
    id = input("ingrese id del producto a eliminar: ")
    conn.execute(f"DELETE FROM productos WHERE id_producto={id}")
    if conn.rowcount == 0:
        print("ningun producto posee ese id")
    else:
        print("el producto fue eliminado exitosamente")


def agregar_cliente(dni):
    nombre = input("ingrese nombre del cliente: ")
    ape = input("ingrese apellido del cliente: ")
    edad = input("ingrese edad: ")
    conn.execute( f"INSERT INTO clientes VALUES ({dni}, '{nombre}', '{ape}', {edad});")


def agregar_empleado(dni):
    nombre = input("ingrese nombre del empleado: ")
    ape = input("ingrese apellido del empleado: ")
    edad = input("ingrese edad: ")
    conn.execute( f"""INSERT INTO empleados (dni,nombre,apellido,edad)
                        VALUES ({dni}, '{nombre}', '{ape}', {edad});""")

def ver_carrito():
    print(carrito)



carrito = []
dni_empleado = 0

#----MENU-----
if __name__ == '__main__':

    conn = engine.connect()
    
    while True:
        # LOG IN empleado
        if dni_empleado != 0:
            input("presione enter para continuar")
        else:
            dni_empleado = input("ingrese su dni empleado: ")
            conn.execute(f"SELECT * FROM empleados WHERE dni = {dni_empleado};")
            if conn.rowcount == 0:
                print("no existe ese empleado, se creara su perfil...")
                agregar_empleado(dni_empleado)
            else:
                print("Bienvenido al sistema!")
        sleep(2)

        # MENU
        os.system("clear")
        print("--------------------------------------------")
        print("bienvenido al supermercado! que desea hacer?")
        operation = int(input(""" 
        0- agregar producto al carrito
        1- realizar venta
        2- agregar producto
        3- eliminar producto
        4- ver datos
        5- ver carrito
        6- salir
        
        -> """))

        match operation:
            case 0:
                agregar_carrito()
            case 1:
                realizar_venta()
            case 2:
                agregar_producto()
            case 3:
                eliminar_producto()
            case 4:
                ver()
            case 5:
                ver_carrito()
            case 6:
                conn.close()
                print("conexion cerrada")
                break
            case _:
                print("opcion no valida")