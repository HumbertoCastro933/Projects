const Cart = require('./cart');

describe('Pruebas unitarias del Carrito de Compras', () => {
    let cart;

    beforeEach(() => {
        cart = new Cart();
    });

    test('1. Crear un carrito vacío', () => {
        expect(cart).toBeDefined();
        expect(cart.items).toHaveLength(0);
    });

    test('2. Agregar un producto al carrito', () => {
        cart.addItem({ id: 1, name: 'Laptop', price: 1000, quantity: 1 });
        expect(cart.items.length).toBeGreaterThan(0);
        expect(cart.items[0].name).toBe('Laptop');
    });

    test('3. Agregar el mismo producto dos veces (Aumentar cantidad)', () => {
        cart.addItem({ id: 1, name: 'Mouse', price: 20, quantity: 1 });
        cart.addItem({ id: 1, name: 'Mouse', price: 20, quantity: 1 });
        expect(cart.items[0].quantity).toBe(2);
    });

    test('4. Eliminar un producto existente', () => {
        cart.addItem({ id: 2, name: 'Teclado', price: 50, quantity: 1 });
        const removed = cart.removeItem(2);
        expect(removed).toBeTruthy();
        expect(cart.items).toHaveLength(0);
    });

    test('5. Intentar eliminar un producto que no existe', () => {
        const removed = cart.removeItem(99);
        expect(removed).toBeFalsy();
    });

    test('6. Actualizar la cantidad de un producto', () => {
        cart.addItem({ id: 3, name: 'Monitor', price: 200, quantity: 1 });
        cart.updateQuantity(3, 5);
        expect(cart.items[0].quantity).toBe(5);
    });

    test('7. Contar el total de productos', () => {
        cart.addItem({ id: 1, name: 'A', price: 10, quantity: 2 });
        cart.addItem({ id: 2, name: 'B', price: 10, quantity: 3 });
        expect(cart.getTotalItems()).toBe(5);
    });

    test('8. Calcular el subtotal del carrito', () => {
        cart.addItem({ id: 1, name: 'A', price: 100, quantity: 2 });
        expect(cart.getSubtotal()).toBe(200);
    });

    test('9. Aplicar un cupón válido', () => {
        const discountValue = cart.applyCoupon('PROMO10');
        expect(discountValue).toBe(0.10);
        expect(cart.discount).toBe(0.10);
    });

    test('10. Aplicar un cupón inválido (Debe generar error)', () => {
        expect(() => {
            cart.applyCoupon('CUPON_FALSO');
        }).toThrow();
    });

    test('11. Calcular el total con descuento', () => {
        cart.addItem({ id: 1, name: 'A', price: 100, quantity: 1 });
        cart.applyCoupon('PROMO10'); // 10% de 100 = 10
        expect(cart.getTotal()).toBe(90);
    });

    test('12. Vaciar el carrito', () => {
        cart.addItem({ id: 1, name: 'A', price: 10, quantity: 1 });
        cart.applyCoupon('PROMO10');
        cart.clearCart();
        expect(cart.items).toHaveLength(0);
        expect(cart.discount).toBe(0);
    });
});