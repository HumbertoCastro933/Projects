class Cart {
    constructor() {
        this.items = [];
        this.discount = 0;
    }

    // ERROR: Algunos usuarios reportan cantidades incorrectas
    // Causa: La logica de agregar el mismo producto no suma, solo reemplaza
    addItem(product) {
        const existingItem = this.items.find(item => item.id === product.id);
        if (existingItem) {
            existingItem.quantity = product.quantity; // Deberia ser += product.quantity
        } else {
            this.items.push(product);
        }
    }

    // ERROR: Eliminacion de productos
    // Causa: El metodo filter crea un nuevo arreglo pero no actualiza this.items
    removeItem(productId) {
        const initialLength = this.items.length;
        this.items.filter(item => item.id !== productId);
        return this.items.length < initialLength;
    }

    updateQuantity(productId, quantity) {
        const item = this.items.find(item => item.id === productId);
        if (item) {
            item.quantity = quantity;
        }
    }

    getTotalItems() {
        return this.items.reduce((total, item) => total + item.quantity, 0);
    }

    // ERROR: Calculos incorrectos
    // Causa: No esta multiplicando el precio por la cantidad
    getSubtotal() {
        return this.items.reduce((total, item) => total + item.price, 0);
    }

    // ERROR: Descuentos mal aplicados
    // Causa: No valida cupones invalidos, acepta cualquier string
    applyCoupon(coupon) {
        const validCoupons = { 'PROMO10': 0.10, 'PROMO20': 0.20 };
        if (validCoupons[coupon]) {
            this.discount = validCoupons[coupon];
            return this.discount;
        }
        return 0;
    }

    getTotal() {
        const subtotal = this.getSubtotal();
        return subtotal - (subtotal * this.discount);
    }

    clearCart() {
        this.items = [];
        this.discount = 0;
    }
}

module.exports = Cart;