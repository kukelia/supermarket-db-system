import psycopg2
import os


conn = psycopg2.connect(database="supermarket",
                        host="127.0.0.1",
                        user="postgres",
                        password="password",
                        port="5432")
conn.autocommit = True
cursor = conn.cursor()
table_names = [0,"clientes", "productos", "compras"]
pks = [0,"dni", "id_producto", "id_compra"]
 
    
def ver():
    entity = int(input("""elija que desea ver:
    1- cliente
    2- producto
    3- compra
    """))
    id = int(input("seleccione el id del elemento a visualizar: "))
    #what if none?
    cursor.execute(f"SELECT * FROM {table_names[entity]} WHERE {pks[entity]} = {id};") 
    if cursor.rowcount == 0:
        print(f"ningun resultado con {pks[entity]} igual a {id}")
        return
    else:
        print(cursor.fetchone())
        return


def agregar_producto():
    id = input("ingrese id: ")
    cursor.execute(f"SELECT * FROM productos WHERE id_producto = {id};")
    if cursor.rowcount == 0:
        nombre = input("ingrese nombre producto: ")
        precio = input("ingrese precio: ")
        cat = input("ingrese categoria: ")
        cursor.execute( f"INSERT INTO productos VALUES ({id}, '{nombre}', {precio}, '{cat}');")
    else:
        print("el producto ya existe")


def realizar_compra():
    # try:
        global carrito
        dni = input("ingrese dni cliente: ")
        cursor.execute(f"SELECT * FROM clientes WHERE dni = {dni};")
        if cursor.rowcount == 0:
            print("el cliente no existe, debera ser agregado")
            agregar_cliente(dni)
        
        cursor.execute("BEGIN;")
        cursor.execute(f"""INSERT INTO compras (dni_cliente, dni_empleado)
                        VALUES ({dni}, {dni_empleado}) RETURNING *""")
        id_compra = cursor.fetchone()[0]
        for id_producto in carrito:
            cursor.execute(f"""
                                INSERT INTO productos_comprados (id_compra, id_producto)
                                VALUES ({id_compra}, {id_producto}) RETURNING producto_vendido ;""")
            id_producto_vendido = cursor.fetchone()[0] 
            print(f"id del producto vendido es {id_producto_vendido}")      
            cursor.execute(f"""       
                                with precio_actual as
                                (SELECT precio FROM productos WHERE id_producto={id_producto})
                                UPDATE productos_comprados
                                SET precio_compra = precio_actual.precio FROM precio_actual
                                WHERE producto_vendido = {id_producto_vendido}
                                """)

            # os.system(f"""echo "LOG
            #     INSERT INTO productos_comprados (id_compra, id_producto)
            #     VALUES ({id_compra}, {id_producto}) RETURNING producto_vendido ;

            #     with precio_actual as
            #     (SELECT precio FROM productos WHERE id_producto={id_producto})
            #     UPDATE productos_comprados
            #     SET precio_compra = precio_actual.precio FROM precio_actual
            #     WHERE producto_vendido = {id_producto_vendido}" >> logs/log.txt
            #     """)  

        cursor.execute(f"""
                    SELECT sum FROM(
                        SELECT productos_comprados.id_compra, SUM(productos.precio)
                        FROM productos_comprados
                        INNER JOIN productos ON productos_comprados.id_producto = productos.id_producto
                        GROUP BY productos_comprados.id_compra
            ) as result_table
        where result_table.id_compra={id_compra}
        """)
        precio_total = cursor.fetchone()[0]
        cursor.execute(f"UPDATE compras SET precio_total={precio_total} WHERE id_compra={id_compra}")

        cursor.execute("COMMIT;")
        carrito= []
    # except:
    #     print("ha ocurrido un error")
    #     cursor.execute("ROLLBACK;")
    


def agregar_carrito():
    id = input("ingrese id: ")
    cursor.execute(f"SELECT * FROM productos WHERE id_producto = {id};")
    if cursor.rowcount == 0:
        print("no existe ese producto")
        return
    else:
        carrito.append(id)



def eliminar_producto():
    id = input("ingrese id del producto a eliminar: ")
    cursor.execute(f"DELETE FROM productos WHERE id_producto={id}")
    if cursor.rowcount == 0:
        print("ningun producto posee ese id")
    else:
        print("el producto fue eliminado exitosamente")


def agregar_cliente(dni):
    nombre = input("ingrese nombre del cliente: ")
    ape = input("ingrese apellido del cliente: ")
    edad = input("ingrese edad: ")
    cursor.execute( f"INSERT INTO clientes VALUES ({dni}, '{nombre}', '{ape}', {edad});")


def agregar_empleado(dni):
    nombre = input("ingrese nombre del empleado: ")
    ape = input("ingrese apellido del empleado: ")
    edad = input("ingrese edad: ")
    cursor.execute( f"""INSERT INTO empleados (dni,nombre,apellido,edad)
                        VALUES ({dni}, '{nombre}', '{ape}', {edad});""")

def ver_carrito():
    print(carrito)



carrito = []
x = 0
dni_empleado=0

#----MENU-----

while True:
    if dni_empleado != 0:
        input("presione enter para continuar")
    else:
        dni_empleado = input("ingrese su dni empleado: ")
        cursor.execute(f"SELECT * FROM empleados WHERE dni = {dni_empleado};")
        if cursor.rowcount == 0:
            print("no existe ese empleado, se creara su perfil...")
            agregar_empleado(dni_empleado)
        else:
            print("Bienvenido al sistema!")

    os.system("clear")
    print("--------------------------------------------")
    print("bienvenido al supermercado! que desea hacer?")
    operation = int(input(""" 
    0- agregar producto al carrito
    1- realizar compra
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
            realizar_compra()
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