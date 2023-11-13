
# Conocimientos técnicos de las direcciones Bitcoin de la versión 1
Traducción de https://en.bitcoin.it/wiki/Technical_background_of_version_1_Bitcoin_addresses

Este artículo puede resultar demasiado técnico para algunos usuarios. El [artículo más básico sobre direcciones de Bitcoin](https://en.bitcoin.it/wiki/Address) puede ser más apropiado.

Una dirección de Bitcoin es un hash de 160 bits de la parte pública de un par de claves [ECDSA](http://en.wikipedia.org/wiki/Elliptic_Curve_DSA) público/privado. Utilizando la criptografía de [clave pública](http://en.wikipedia.org/wiki/Public-key_cryptography), puedes "firmar" datos con tu clave privada y cualquiera que conozca tu clave pública puede verificar que la firma es válida.

Se genera un nuevo par de claves para cada dirección de recepción (con monederos [HD más recientes](https://en.bitcoin.it/wiki/Deterministic_wallet), esto se hace de manera determinista). La clave pública y sus claves privadas asociadas (o la semilla necesaria para generarlas) se almacenan en el [archivo de datos del monedero](https://en.bitcoin.it/wiki/Wallet). Este es el único archivo que los usuarios deberían necesitar [respaldar](https://en.bitcoin.it/wiki/Backup). Una transacción de "envío" a una dirección de Bitcoin específica requiere que el monedero correspondiente conozca la clave privada que la implementa. Esto implica que si creas una dirección y recibes monedas en esa dirección, luego restauras el monedero desde una [copia de seguridad anterior](enlace a copia de seguridad), antes de que se generara la dirección, entonces las monedas recibidas con esa dirección se pierden; esto no es un problema para monederos HD donde todas las direcciones se generan a partir de una única semilla. Las direcciones se añaden a un [grupo de claves de direcciones o `key pool`](https://en.bitcoin.it/wiki/Key_pool) antes de ser utilizadas para recibir monedas. Si pierdes tu monedero por completo, todas tus monedas se pierden y no pueden recuperarse.

Bitcoin te permite crear tantas direcciones como desees y usar una nueva para cada transacción. No hay una "dirección maestra": el área de "Tu dirección de Bitcoin" en algunas interfaces de monedero no tiene ninguna importancia especial. Solo está allí para tu conveniencia y debería cambiar automáticamente cuando se utiliza.

Las direcciones de Bitcoin contienen un código de verificación incorporado, por lo que generalmente no es posible enviar bitcoins a una dirección mal escrita. Sin embargo, si la dirección está bien formada pero nadie la posee (o el propietario perdió su `wallet.dat`), cualquier moneda enviada a esa dirección se perderá para siempre.

Los valores hash y los datos de comprobación se convierten a una representación alfanumérica mediante un esquema personalizado: el [esquema de codificación Base58Check](https://en.bitcoin.it/wiki/Base58Check_encoding). Bajo Base58Check, las direcciones pueden contener todos los caracteres alfanuméricos excepto 0, O, I y l. Las direcciones [P2PKH](https://en.bitcoin.it/wiki/P2PKH) de la red principal o `Mainnet` comienzan con 1, mientras que las direcciones [P2SH](https://en.bitcoin.it/wiki/P2SH) comienzan con 3 (las direcciones [Bech32](https://en.bitcoin.it/wiki/Bech32) comienzan con bc1 y no utilizan la codificación Base58Check). Las direcciones de testnet suelen comenzar con m o n. Las direcciones de la red principal pueden tener una longitud de 25-34 caracteres, y las direcciones de testnet pueden tener una longitud de 26-34 caracteres. La mayoría de las direcciones tienen 33 o 34 caracteres de longitud.

## Colisiones (o la falta de ellas)
Dado que las direcciones de Bitcoin son esencialmente números aleatorios, es posible, aunque extremadamente improbable, que dos personas generen independientemente la misma dirección. Esto se llama una [colisión](http://en.wikipedia.org/wiki/Collision_(computer_science)). Si esto sucede, tanto el propietario original de la dirección como el propietario colisionado podrían gastar el dinero enviado a esa dirección. No sería posible para la persona colisionada gastar la billetera completa del propietario original (o viceversa).

Pero debido a que el espacio de direcciones posibles es tan astronómicamente grande, es más probable que la Tierra sea destruida en los próximos 5 segundos que ocurra una colisión en el próximo milenio.


## Cómo crear una dirección de Bitcoin
La forma correcta de crear una dirección de Bitcoin es utilizar un software de monedero bien probado, de código abierto y revisado por pares. Manipular claves manualmente ha resultado en pérdida de fondos una y otra vez. A diferencia de otros sistemas centralizados, las pérdidas en Bitcoin suelen ser irreversibles.

Aquí hay un resumen breve de cómo funciona la generación de direcciones, con fines informativos:

0 - Tener una clave privada ECDSA
   ``` 
   18e14a7b6a307f426a94f8114701e7c8e774e7f9a47e2c2035db29a206321725
   ```

1 - Tomar la clave pública correspondiente generada con ella (33 bytes, 1 byte 0x02 (la coordenada y es par) y 32 bytes correspondientes a la coordenada X)
   ``` 
   0250863ad64a87ae8a2fe83c1af1a8403cb53f53e486d8511dad8a04887e5b2352
   ```
2 - Realizar un hash SHA-256 en la clave pública
   ```
   0b7c28c9b7290c98d7438e70b3d3f7c848fbd7d1dc194ff83f4f7cc9b1378e98
   ```
3 - Realizar un hash RIPEMD-160 en el resultado de SHA-256
   ``` 
   f54a5851e9372b87810a8e60cdd2e7cfd80b6e31
   ```
4 - Agregar un byte de versión delante del hash RIPEMD-160 (0x00 para la Red Principal)
   ```
   00f54a5851e9372b87810a8e60cdd2e7cfd80b6e31
   ```
(nota que los siguientes pasos son la codificación Base58Check, que tiene múltiples opciones de bibliotecas que la implementan)
5 - Realizar un hash SHA-256 en el resultado extendido de RIPEMD-160
   ```
   ad3c854da227c7e99c4abfad4ea41d71311160df2e415e713318c70d67c6b41c
   ```
6 - Realizar un hash SHA-256 en el resultado del anterior hash SHA-256
   ```
   c7f18fe8fcbed6396741e58ad259b5cb16b7fd7f041904147ba1dcffabf747fd
   ```
7 - Tomar los primeros 4 bytes del segundo hash SHA-256. Este es el checksum de la dirección
   ```
   c7f18fe8
   ```
8 - Agregar los 4 bytes de checksum del paso 7 al final del hash extendido de RIPEMD-160 del paso 4. Este es el Bitcoin Address binario de 25 bytes.
   ```
   00f54a5851e9372b87810a8e60cdd2e7cfd80b6e31c7f18fe8
   ```
9 - Convertir el resultado de una cadena de bytes a una cadena base58 utilizando la codificación Base58Check. Este es el formato más comúnmente utilizado para una dirección de Bitcoin.
   ``` 
   1PMycacnJaSqwwJqjawXBErnLsZ7RkXUAs
   ```
## Conversión de la clave pública de ECDSA a la dirección de Bitcoin (Explicación gráfica)
![Conversión de la clave pública de ECDSA a la dirección de Bitcoin](https://en.bitcoin.it/w/images/en/9/9b/PubKeyToAddr.png)