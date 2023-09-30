CREATE TABLE producto (
    id_producto SERIAL PRIMARY KEY,
    producto VARCHAR(45) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    costo DECIMAL(10,2) NOT NULL
);

CREATE TABLE direccion_compra (
    id_direccion SERIAL PRIMARY KEY,
    direccion VARCHAR(60) NOT NULL,
    enlace_maps VARCHAR (95) NOT NULL
);

CREATE TABLE ventas (
    id_venta SERIAL PRIMARY KEY,
    fecha_orden DATE NOT NULL,
    id_orden INT NOT NULL,
    id_producto INT NOT NULL,
    id_direccion INT NOT NULL,
    cantidad_ordenada INT NOT NULL,
    ingresos DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto),
    FOREIGN KEY (id_direccion) REFERENCES direccion_compra(id_direccion)
);