const procesarProducto = require('./Pruebas js/inventario');

test("Validación completa de un nuevo producto", () => {
    const producto = procesarProducto("Monitor Gamer", 4500, 10);

    // 1. toBe
    expect(producto.nombre).toBe("Monitor Gamer");

    // 2. toEqual
    expect(producto.categorias).toEqual(["hardware", "computación"]);

    // 3. toBeGreaterThan 
    expect(producto.precio).toBeGreaterThan(4000);

    // 4. toBeLessThanOrEqual 
    expect(producto.stock).toBeLessThanOrEqual(10);

    // 5. toBeTruthy 
    expect(producto.disponible).toBeTruthy();

    // 6. toContain 
    expect(producto.categorias).toContain("hardware");

    // 7. toMatch 
    expect(producto.nombre).toMatch(/Gamer/);

    // 8. toBeDefined 
    expect(producto.id).toBeDefined();

    // 9. toBeNull 
    expect(producto.detalles).toBeNull();

    // 10. toHaveLength 
    expect(producto.categorias).toHaveLength(2);
});


describe("Pruebas específicas de inventario", () => {

    test("Debe lanzar un error si el precio es negativo", () => {
        expect(() => {
            procesarProducto("Teclado", -10, 5);
        }).toThrow("El precio no puede ser negativo");
    });

    test("Verificar que la versión no sea nula ni indefinida", () => {
        const p = procesarProducto("Mouse", 200, 1);
        expect(p.precio === 0).toBeFalsy();
    });
});