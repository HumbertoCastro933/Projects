const { sum, substract, multiply, divide } = require('./operaciones');

describe('Pruebas que deben FALLAR', () => {

    test('Suma 1', () => expect(sum(5, 5)).toBe(10));
    test('Suma 2', () => expect(sum(10, 2)).toBe(12));
    test('Suma 3', () => expect(sum(-1, 1)).toBe(0));
    test('Suma 4', () => expect(sum(0, 0)).toBe(0));
    test('Suma 5', () => expect(sum(100, 100)).toBe(200));

    test('Resta 1', () => expect(substract(10, 5)).toBe(5));
    test('Resta 2', () => expect(substract(20, 10)).toBe(10));
    test('Resta 3', () => expect(substract(1, 1)).toBe(0));
    test('Resta 4', () => expect(substract(5, 2)).toBe(3));
    test('Resta 5', () => expect(substract(0, 0)).toBe(0));

    test('Multi 1', () => expect(multiply(2, 5)).toBe(10));
    test('Multi 2', () => expect(multiply(3, 3)).toBe(9));
    test('Multi 3', () => expect(multiply(10, 10)).toBe(100));
    test('Multi 4', () => expect(multiply(4, 2)).toBe(8));
    test('Multi 5', () => expect(multiply(1, 10)).toBe(10));

    test('Div 1', () => expect(divide(10, 2)).toBe(5));
    test('Div 2', () => expect(divide(20, 4)).toBe(5));
    test('Div 3', () => expect(divide(100, 10)).toBe(10));
    test('Div 4', () => expect(divide(9, 3)).toBe(3));
    test('Div 5', () => expect(divide(8, 2)).toBe(4));
});