import hashlib
import base58


def little_endian_to_big_endian(input_str):
    # Verifica si la cadena de entrada tiene la longitud correcta
    if len(input_str) % 2 != 0:
        raise ValueError("La cadena debe tener una longitud par")

    # Divide la cadena en pares de caracteres
    pairs = [input_str[i:i+2] for i in range(0, len(input_str), 2)]

    # Intercambia cada par de caracteres
    reversed_pairs = pairs[::-1]

    # Une los pares invertidos
    output_str = ''.join(reversed_pairs)

    return output_str

def pubkey_to_bitcoin_address(pubkey_hex):
    pubkey_bytes = bytes.fromhex(pubkey_hex)

    # Calculate SHA-256 of the public key
    sha256_hash = hashlib.sha256(pubkey_bytes).digest()
    print('sha256_hash: '+ sha256_hash.hex())

    # Calculate RIPEMD-160 of the SHA-256 result
    ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()
    print('ripemd160_hash: '+ ripemd160_hash.hex())

    # Add the version byte at the beginning
    version_byte = b'\x00'
    hash_with_version = version_byte + ripemd160_hash
    print('hash_with_version: ' +hash_with_version.hex())

    # Calculate the double SHA-256 of the result
    double_sha256_hash = hashlib.sha256(hashlib.sha256(hash_with_version).digest()).digest()
    checksum = double_sha256_hash[:4]
    print("SHA256(SHA256(extended Pubkey)):", double_sha256_hash.hex())
    print("Checksum:", checksum.hex())

    # Concatenate the result and the checksum
    binary_address = hash_with_version + checksum
    print("binary_address:", binary_address.hex().upper())

    # Encode in Base58Check
    bitcoin_address = base58.b58encode(binary_address).decode("utf-8")

    return bitcoin_address

# Example of usage
#ex. rene
pubkey_hex = '03486669962008e0713660b6d69117a65fcecd221d06c1e5077b4d9cd477c0cf98'
#my example
#pubkey_hex = '0335c1d3651153e5745da6d2365b7a2f2806bc4887e484f95c4a278fec1de28b83'
bitcoin_address = pubkey_to_bitcoin_address(pubkey_hex)
print("Bitcoin Address:", bitcoin_address)
#assert bitcoin_address == "1KwjU4UknzbXh1rnP1jAKz9wwjcuYwe9AC", f"The generated address {bitcoin_address} does not match the expected one."


tx_out_hash_little_endian = "911d280701fbaa08cd97646f5c3483284b4f37afeff3bf71f2b580063399bed5"

tx_out_hash_big_endian = little_endian_to_big_endian(tx_out_hash_little_endian)

print("Little-endian:", tx_out_hash_little_endian)
print("Big-endian:", tx_out_hash_big_endian)
