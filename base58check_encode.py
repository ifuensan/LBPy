import base58
import hashlib

def hex_to_bytes(hex_string):
    """
    Convierte una cadena hexadecimal a bytes.

    Args:
        hex_string (str): La cadena hexadecimal que se desea convertir a bytes.

    Returns:
        bytes: Los bytes resultantes de la conversión.

    Example:
        >>> hex_to_bytes('48656c6c6f20576f726c64')
        b'Hello World'
    """
    # Convierte una cadena hexadecimal a bytes
    return bytes.fromhex(hex_string)

def base58check_encode(data):
    """
    Codifica datos en formato Base58.

    Args:
        data (bytes): Los datos que se desean codificar en Base58.

    Returns:
        str: La representación Base58 de los datos.

    Raises:
        ValueError: Si los datos no son bytes.

    Example:
        >>> base58check_encode(b'Hello World')
        '1DUJooNvwrPvt42PfVB6f6y5brru'
    """
    # Codificar en Base58
    base58_encoded = base58.b58encode(data)

    # Decodificar en hexadecimal
    hex_encoded = base58_encoded.decode("utf-8")
    hex_result = int.from_bytes(base58.b58decode(hex_encoded), byteorder='big').to_bytes(25, byteorder='big').hex()

    return hex_result.upper()

# Ejemplo de uso
hex_data_to_encode = '00CB226B9CC60C613DDDCB188E984F631764CEF143CE281C01'
bytes_data_to_encode = hex_to_bytes(hex_data_to_encode)
encoded_result = base58check_encode(bytes_data_to_encode)
print("Base58Check Encoded:", encoded_result)

version=0x00
# Paso 1: Agregar el byte de versión al principio de los datos
data_with_version = bytes([version]) + bytes_data_to_encode
# Paso 2: Calcular el doble SHA256 del resultado del paso 1
checksum = hashlib.sha256(hashlib.sha256(data_with_version).digest()).digest()[:4]
print("Checksum en Hexadecimal:", checksum.hex())


