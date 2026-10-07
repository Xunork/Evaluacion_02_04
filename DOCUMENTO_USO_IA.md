# Documento de uso de IA (ES2 — Ferretería “El Martillo”, entrega-final)

## Qué se generó con IA
1. Modelos `Categoria`, `Producto` (nombre, categoría FK, precio, stock + descripción), `Pedido`/`DetallePedido`.
2. Registro en `/admin` con `list_display`, `list_editable` (precio, stock), `search_fields` y `list_filter`.
3. Comando `productos/management/commands/seed.py` con las 40 descripciones/precios/stocks de ferretería y las 2 cuentas genéricas.
4. Vistas y templates (listado desde BD, detalle, login/registro, carrito, panel admin) y el CSS minimalista.

## Qué verifiqué manualmente (sin IA)
- `python manage.py check` sin errores.
- `Producto.objects.count()` → 40 (10 Herramientas, 8 Fijaciones, 8 Pinturas, 7 Electricidad, 7 Plomería).
- Flujo cliente: login `cliente/cliente123`, agregar x2 al carrito, checkout descuenta stock (16→14 en prueba, luego restaurado a 16).
- Flujo admin: login `admin/admin123`, `/panel/` 200, editar guarda los 5 campos.
- Servidor real: `/` 200, `/login/` 200, `/carrito/` 200, `/panel/` sin login redirige (302).
- `git log --oneline` contiene los 5 mensajes de etapa exigidos.

## Declaración
La IA asistió en la redacción de código y datos de ejemplo; la ejecución, las pruebas
y la verificación del repositorio las realicé yo. El código es comprendido y puede ser
explicado en la defensa.
