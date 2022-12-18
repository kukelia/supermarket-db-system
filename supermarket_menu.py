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
    result = cursor.fetchone()
    print(result)
    


def agregar_producto():
    id = input("ingrese id: ")
    nombre = input("ingrese nombre producto: ")
    precio = input("ingrese precio: ")
    cat = input("ingrese categoria: ")
    cursor.execute( f"INSERT INTO productos VALUES ({id}, '{nombre}', {precio}, '{cat}');")


def agregar_compra():
    dni = input("ingrese dni cliente: ")
    cursor.execute(f"SELECT * FROM clientes WHERE id == {dni};")
    if cursor.rowcount == 0:
        print("el cliente no existe, debera ser agregado")
        agregar_cliente(dni)
    # cursor.execute(f"INSERT INTO producto VALUES ({id}, {nombre}, {precio}, {cat});")



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

x = 0

while True:
    if x == 1:
        input("presione enter para continuar")
    else:
        x = 1
    os.system("clear")
    print("--------------------------------------------")
    print("bienvenido al supermercado! que desea hacer?")
    operation = int(input(""" 
    1- realizar compra
    2- agregar producto
    3- eliminar producto
    4- ver datos
    5-salir
    
    -> """))

    match operation:
        case 1:
            agregar_compra()
        case 2:
            agregar_producto()
        case 3:
            eliminar_producto()
        case 4:
            ver()
        case 5:
            conn.close()
            print("conexion cerrada")
            break
        case _:
            print("opcion no valida")
