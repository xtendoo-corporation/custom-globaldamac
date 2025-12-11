# Globaldamac Product Units Per Box

## Descripcion

Este modulo para Odoo 17 permite gestionar productos que se venden en cajas, calculando automaticamente el numero de cajas a partir de las unidades. El flujo completo esta cubierto: ventas, inventario y facturacion.

**LOGICA DEL MODULO:**
- La **unidad base de Odoo** representa **unidades individuales** del producto
- El campo **"Unidades por Caja"** indica cuantas unidades contiene cada caja
- El sistema **calcula automaticamente** el numero de cajas: `Cajas = Unidades ÷ Unidades por Caja`

**Ejemplo:**
- Producto: `units_per_box = 80` (cada caja contiene 80 unidades)
- Venta: `Cantidad = 80` unidades
- Resultado: `Cajas = 1` (80 ÷ 80 = 1 caja)

## Caracteristicas

### Configuracion de Variantes de Productos

- **Unidades por Caja**: Campo en cada variante (product.product) que indica cuantas unidades contiene una caja.
- Cada variante puede tener una configuracion diferente de unidades por caja.

### Lineas de Venta (Sale Order)

- **Cantidad**: Numero de unidades individuales (campo estandar de Odoo)
- **Unidades por Caja**: Cuantas unidades hay en cada caja (del producto)
- **Cajas**: Campo calculado automaticamente (Cantidad ÷ Unidades por Caja)

### Inventario (Stock)

- **Stock Moves**: Campos de unidades por caja y cajas calculadas
- **Stock Move Lines**: Campos de unidades por caja y cajas calculadas
- **Pickings**: Visualizacion de unidades por caja y cajas en albaranes

### Facturacion (Account)

- **Lineas de Factura**: Campos de unidades por caja y cajas calculadas
- **Facturas de Cliente**: Visualizacion en facturas de venta
- **Facturas de Proveedor**: Visualizacion en facturas de compra

## Instalacion

1. Copiar el modulo en el directorio de addons personalizado.
2. Actualizar la lista de aplicaciones.
3. Buscar e instalar "Globaldamac Product Units Per Box".

## Uso

### Configurar una Variante de Producto

1. Ir a Ventas > Productos > Productos.
2. Abrir o crear una variante de producto.
3. Establecer el campo "Unidades por Caja" (por ejemplo: 80).

### Ejemplo con Variantes Diferentes

Si tienes un producto con multiples variantes, cada una puede tener diferentes unidades por caja:

**Producto: Refresco Cola**
- Variante "Lata 330ml": Unidades por Caja = 24
  - Si vendes 48 unidades → 2 cajas
- Variante "Botella 500ml": Unidades por Caja = 12
  - Si vendes 36 unidades → 3 cajas
- Variante "Botella 2L": Unidades por Caja = 6
  - Si vendes 18 unidades → 3 cajas

### Flujo Completo

1. **Venta**: Al crear un pedido, introduces las unidades. El sistema calcula automaticamente las cajas.
2. **Albaran**: Los movimientos de stock muestran unidades y cajas.
3. **Factura**: Las lineas de factura muestran unidades y cajas.

## Dependencias

- `sale`
- `product`
- `stock`
- `account`

## Autor

- Xtendoo (https://xtendoo.es)

## Licencia

AGPL-3.0 o posterior (http://www.gnu.org/licenses/agpl.html)

