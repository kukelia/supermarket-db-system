import os
from sqlalchemy import create_engine, text
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

table_names = ["clientes", "productos", "ventas", 'empleados']
pks = ["dni", "id_producto", "id_compra", 'dni']
 
    
def ver():
    entity = int(input("""
            elija que desea ver:
            1- clientes
            2- productos
            3- ventas
            4- empleados
    """)) -1
    id = int(input("seleccione el id del elemento a visualizar: "))
    #what if none?
    res =conn.execute(text(f"SELECT * FROM {table_names[entity]} WHERE {pks[entity]} = {id};"))
    if res.rowcount == 0:
        print(f"ningun resultado con {pks[entity]} igual a {id}")
        return
    else:
        print(res.fetchone())
        return


def agregar_producto():
    id = input("ingrese id: ")
    res = conn.execute(text(f"SELECT * FROM productos WHERE id_producto = {id};"))
    if res.rowcount == 0:
        nombre = input("ingrese nombre producto: ")
        precio = input("ingrese precio: ")
        cat = input("ingrese categoria: ")
        conn.execute(text(f"INSERT INTO productos VALUES ({id}, '{nombre}', {precio}, '{cat}');"))
        conn.commit()
    else:
        print("el producto ya existe")



def realizar_venta():
    global carrito

    if len(carrito) ==0:
        print("carrito vacio")
        return 0
    
    dni = input("ingrese dni cliente: ")
    res = conn.execute(text(f"SELECT * FROM clientes WHERE dni = {dni};"))
    if res.rowcount == 0:
        print("el cliente no existe, debera ser agregado")
        agregar_cliente(dni)
    
    conn.execute(text("BEGIN;"))
    res = conn.execute(text(f"""INSERT INTO ventas (dni_cliente, dni_empleado)
                    VALUES ({dni}, {dni_empleado}) RETURNING *"""))
    id_venta = res.fetchone()[0]
    for id_producto in carrito: #update for quantity
        res = conn.execute(text(f"""
                            INSERT INTO venta_detalle (id_venta, id_producto,cantidad)
                            VALUES ({id_venta}, {id_producto},1);"""))

        # Change? first get price, then make venta_detalle
        conn.execute(text(f"""       
                            WITH precio_actual AS (
                                SELECT precio FROM productos WHERE id_producto={id_producto}
                            )
                            UPDATE venta_detalle
                            SET precio_detalle = (SELECT precio FROM precio_actual)
                            WHERE id_venta = {id_venta} AND id_producto = {id_producto};
                            """)) 

    res = conn.execute(text(f"""
                            SELECT sum FROM(
                                SELECT venta_detalle.id_venta, SUM(productos.precio)
                                FROM venta_detalle
                                INNER JOIN productos ON venta_detalle.id_producto = productos.id_producto
                                GROUP BY venta_detalle.id_venta
                            ) AS result_table
                            where result_table.id_venta={id_venta}
                            """))
    
    precio_total = res.fetchone()[0]
    conn.execute(text(f"UPDATE ventas SET precio_total={precio_total} WHERE id_venta={id_venta}"))

    conn.execute(text("COMMIT;"))
    carrito= []
    conn.commit()
    


def agregar_carrito():
    id = input("ingrese id: ")
    res = conn.execute(text(f"SELECT * FROM productos WHERE id_producto = {id};"))
    if res.rowcount == 0:
        print("no existe ese producto")
        return
    else:
        print(f'se agrego el producto: {res.fetchone()}')
        carrito.append(id)


def eliminar_producto():
    id = input("ingrese id del producto a eliminar: ")
    res = conn.execute(text(f"DELETE FROM productos WHERE id_producto={id}"))
    if res.rowcount == 0:
        print("ningun producto posee ese id")
    else:
        conn.commit()
        print("el producto fue eliminado exitosamente")


def agregar_cliente(dni):
    nombre = input("ingrese nombre del cliente: ")
    ape = input("ingrese apellido del cliente: ")
    edad = input("ingrese edad: ")
    conn.execute(text(f"""INSERT INTO clientes (dni,nombre,apellido,edad)
                       VALUES ({dni}, '{nombre}', '{ape}', {edad});"""))
    conn.commit()


def agregar_empleado(dni):
    nombre = input("ingrese nombre del empleado: ")
    ape = input("ingrese apellido del empleado: ")
    edad = input("ingrese edad: ")
    conn.execute(text(f"""INSERT INTO empleados (dni,nombre,apellido,edad)
                        VALUES ({dni}, '{nombre}', '{ape}', {edad});"""))
    conn.commit()

def ver_carrito():
    print(carrito)



carrito = []
dni_empleado = 0

#----MENU-----
if __name__ == '__main__':
    sleep(2) # wait for docker attach command
    conn = engine.connect()
    print("engine conenected")
    
    # LOG IN empleado
    if dni_empleado != 0:
        input("presione enter para continuar")
    else:
        dni_empleado = input("ingrese su dni empleado: ")
        res =conn.execute(text(f"SELECT * FROM empleados WHERE dni = {dni_empleado};"))
        if res.rowcount == 0:
            print("no existe ese empleado, se creara su perfil...")
            agregar_empleado(dni_empleado)
            print("empleado agregado con exito..")
        else:
            print("Bienvenido al sistema!")

    # MENU
    while True:
        input("presione cualquier tecla para continuar")
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