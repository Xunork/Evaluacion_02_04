# ES2 — Catálogo Online Ferretería “El Martillo” (Sección A)

Plataforma web de negocio local. En esta evaluación el contenido **deja de estar estático:
vive en la base de datos y se administra desde Django Admin**. El template principal
muestra el listado **leyendo desde la BD**.

- Negocio: Ferretería (Sección A)
- Dato principal: nombre, categoría, precio, stock (+ descripción como extra)
- Volumen: **40 productos** en 5 categorías

## Cuentas genéricas
| Rol | Usuario | Clave | Acceso |
|---|---|---|---|
| Admin | `admin` | `admin123` | `/panel/` y `/admin/` (CRUD total) |
| Cliente | `cliente` | `cliente123` | tienda + carrito + `/mis-pedidos/` |

## Cómo correr
```bash
cd "Evaluacion_2"
source .venv/bin/activate
python manage.py migrate
python manage.py seed   # crea cuentas + 40 productos de ferretería
python manage.py runserver
```
Abrir http://127.0.0.1:8000/

## Estructura (limpia y simple)
```
Evaluacion_2/
  evaluacion_2/  (settings.py con BD sqlite, urls.py)
  productos/     (models.py, views.py, urls.py, forms.py, admin.py, management/commands/seed.py)
  templates/     (base.html, tienda.html, detalle.html, carrito.html, login/registro, panel admin)
  static/css/style.css   (un solo CSS minimalista)
  db.sqlite3     (BD con los 40 productos cargados)
```

## Etapas y commits (exigidos en la pauta)
| Etapa | Actividad | Commit |
|---|---|---|
| 0. Entorno | Repo, venv y proyecto operativo | `etapa-0-entorno` |
| 1. Modelo y BD | Modelo, conexión en settings.py y migraciones | `etapa-1-modelo` |
| 2. Admin | Superusuario + modelo en /admin con list_display, filtro/búsqueda | `etapa-2-admin` |
| 3. Poblamiento y listado | Seed IA con 40 productos; template lee desde BD | `etapa-3-bd` |
| 4. Entrega | Doc. uso IA, push final y verificación | `entrega-final` |

Verificar con: `git log --oneline` y `python manage.py shell -c "from productos.models import Producto; print(Producto.objects.count())"` → debe dar 40.

## Extras (pedidos del cliente, no exigidos en ES2)
Login/registro, carrito en sesión que **descuenta stock** en `/checkout/`,
panel simple `/panel/` donde el admin modifica nombre, precio, stock, categoría y descripción.

## Ver los datos en SQLite
La BD es `db.sqlite3` (tablas `productos_producto`, `productos_categoria`, `productos_pedido`...).
- **VS Code**: instala la extensión *SQLite* (o *SQLite Viewer*), clic derecho en `db.sqlite3` → *Open Database*, despliega la tabla `productos_producto` → *Show Table*.
- **Terminal**:
```bash
sqlite3 db.sqlite3 "SELECT id, nombre, precio, stock FROM productos_producto LIMIT 5;"
sqlite3 db.sqlite3 "SELECT COUNT(*) FROM productos_producto;"  -- debe dar 40
```
- **Django**: `python manage.py dbshell` o `python manage.py shell`.
