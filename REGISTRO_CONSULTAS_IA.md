# Registro de consultas a la IA (ES2 — Ferretería)

Se completa durante todo el desarrollo, según la pauta.

| # | Fecha | Consulta al asistente | Respuesta / uso aplicado |
|---|---|---|---|
| 1 | 2026-10-06 | Crear proyecto en `Evaluacion_2`: login cliente decente, carrito funcional que baje stock, admin que modifique nombre/precio/stock/categoría/descripción, cuentas genéricas, estructura limpia y CSS minimalista simple | Se generó app `productos` (modelos, vistas, carrito en sesión con descuento de stock en checkout, panel admin + Django admin, templates y 1 CSS). Verificado con tests: checkout baja stock, edición admin OK |
| 2 | 2026-10-06 | Cambiar todo a ferretería con 40 productos según imágenes de la pauta ES2 (Sección A: nombre, categoría, precio, stock, 40 productos; etapas con commits) | Se cambió seed a 40 productos de ferretería en 5 categorías, branding “El Martillo”, README con etapas, docs IA y commits `etapa-0-entorno` → `entrega-final`. Verificado: `Producto.objects.count() == 40` |

Notas:
- Las cuentas `admin/admin123` y `cliente/cliente123` se crean con `python manage.py seed`.
- El poblamiento de 40 productos fue generado con IA y cargado a la BD con el comando `seed`.
