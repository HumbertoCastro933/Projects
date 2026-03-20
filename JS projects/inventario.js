function procesarProducto(nombre, precio, stock) {
    if (precio < 0) {
        throw new Error("El precio no puede ser negativo");
    }

    return {
        id: Math.floor(Math.random() * 100),
        nombre: nombre,
        precio: precio,
        stock: stock,
        categorias: ["hardware", "computación"],
        disponible: stock > 0,
        detalles: null,
        version: "1.0.0"
    };
}

module.exports = procesarProducto;