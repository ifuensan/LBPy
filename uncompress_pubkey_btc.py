def pow_mod(x, y, z):
    """
    Calcula de manera eficiente el resultado de (x ** y) % z.

    Args:
        x (int): Base.
        y (int): Exponente.
        z (int): Módulo.

    Returns:
        int: El resultado de (x ** y) % z.

    Example:
        >>> pow_mod(3, 4, 5)
        1

    Note:
        Esta función utiliza el algoritmo de exponenciación modular para calcular de manera eficiente
        el resultado de la operación (x ** y) % z.
    """
    number = 1
    while y:
        if y & 1:
            number = number * x % z
        y >>= 1
        x = x * x % z
    return number

p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
compressed_key = '03486669962008e0713660b6d69117a65fcecd221d06c1e5077b4d9cd477c0cf98'
y_parity = int(compressed_key[:2]) - 2
x = int(compressed_key[2:], 16)
a = (pow_mod(x, 3, p) + 7) % p
y = pow_mod(a, (p+1)//4, p)
if y % 2 != y_parity:
    y = -y % p
uncompressed_key = '04{:x}{:x}'.format(x, y)
print(uncompressed_key)