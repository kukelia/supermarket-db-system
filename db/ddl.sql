drop table if exists supermarketdb.productos;
drop table if exists supermarketdb.empleados;
drop table if exists supermarketdb.clientes;
drop table if exists supermarketdb.venta_detalle;
drop table if exists supermarketdb.ventas;

drop schema if exists supermarketdb;
create schema supermarketdb;


-- TABLES
create table supermarketdb.empleados (
    dni integer PRIMARY KEY,
    nombre varchar(20),
    apellido varchar(20),
    edad integer
);

create table supermarketdb.clientes (
    dni integer PRIMARY KEY,
    nombre varchar(20),
    apellido varchar(20),
    edad integer
);

create table supermarketdb.ventas (
    id_venta SERIAL PRIMARY KEY,
    dni_cliente integer,
    dni_empleado integer,
    precio_total integer,
    fecha timestamp without time zone,
    CONSTRAINT fk_dni_cliente FOREIGN KEY(dni_cliente) REFERENCES supermarketdb.clientes(dni),

    CONSTRAINT fk_dni_empleado FOREIGN KEY(dni_empleado) REFERENCES supermarketdb.empleados(dni)
);

create table supermarketdb.productos(
    id_producto integer PRIMARY KEY,
    nombre_producto varchar(20),
    precio integer,
    categoria varchar(20)
);

create table supermarketdb.venta_detalle (
    id_venta integer,
    id_producto integer,
    cantidad integer,
    precio_detalle integer,
    PRIMARY KEY(id_venta,id_producto),
    CONSTRAINT fk_id_producto FOREIGN KEY(id_producto) 
        REFERENCES supermarketdb.productos(id_producto),
    CONSTRAINT fk_id_venta FOREIGN KEY(id_venta) 
        REFERENCES supermarketdb.ventas(id_venta) ON DELETE CASCADE

);