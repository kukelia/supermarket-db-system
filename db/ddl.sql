drop schema if exists supermarketdb;
create schema supermarketdb;


-- TABLES
drop table if exists supermarketdb.ventas;
create table supermarketdb.ventas (
    id_venta integer PRIMARY KEY SERIAL,
    dni_cliente integer,
    dni_empleado integer,
    precio_total integer,
    fecha timestamp without time zone
);

drop table if exists supermarketdb.empleados;
create table supermarketdb.empleados (
    dni integer PRIMARY KEY,
    nombre varchar(20),
    apellido varchar(20),
    edad integer
);

drop table if exists supermarketdb.clientes;
create table supermarketdb.clientes (
    dni integer PRIMARY KEY,
    nombre varchar(20),
    apellido varchar(20),
    edad integer
);

drop table if exists supermarketdb.venta_detalle;
create table supermarketdb.venta_detalle (
    id_venta integer,
    id_producto integer,
    cantidad integer,
    precio_detalle integer,
    PRIMARY KEY(id_venta,id_producto)
);

drop table if exists supermarketdb.productos;
create table supermarketdb.productos(
    id_producto integer PRIMARY KEY,
    nombre_producto varchar(20),
    precio integer,
    categoria varchar(20)
);
