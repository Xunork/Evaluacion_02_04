from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db import transaction
from django.db.models import Count
from .models import Producto, Categoria, Pedido, DetallePedido
from .forms import RegistroForm, ProductoForm, CategoriaForm


def es_admin(user):
    return user.is_authenticated and user.is_staff


def _get_cart(request):
    return request.session.get("carrito", {})


def _save_cart(request, cart):
    request.session["carrito"] = cart
    request.session.modified = True


def _cart_detalle(cart):
    """Devuelve (items, total, cantidad_total). items = lista dicts con producto, cantidad, subtotal."""
    items = []
    total = 0
    count = 0
    if not cart:
        return items, total, count
    productos = {str(p.id): p for p in Producto.objects.filter(id__in=[int(k) for k in cart.keys()])}
    for pid, cant in cart.items():
        p = productos.get(str(pid))
        if not p:
            continue
        cant = int(cant)
        sub = p.precio * cant
        items.append({"producto": p, "cantidad": cant, "subtotal": sub})
        total += sub
        count += cant
    return items, total, count


def landing(request):
    categorias = Categoria.objects.annotate(n=Count("productos")).all()
    destacados = Producto.objects.select_related("categoria").order_by("-stock")[:4]
    _, _, cart_count = _cart_detalle(_get_cart(request))
    return render(request, "landing.html", {
        "categorias": categorias,
        "destacados": destacados,
        "total_productos": Producto.objects.count(),
        "cart_count": cart_count,
    })


def tienda(request):
    q = request.GET.get("q", "").strip()
    cat_id = request.GET.get("categoria", "")
    cat_activa = int(cat_id) if cat_id.isdigit() else 0
    productos = Producto.objects.select_related("categoria").all()
    if cat_activa:
        productos = productos.filter(categoria_id=cat_activa)
    if q:
        productos = productos.filter(nombre__icontains=q)
    categorias = Categoria.objects.all()
    _, _, cart_count = _cart_detalle(_get_cart(request))
    return render(request, "tienda.html", {
        "productos": productos,
        "categorias": categorias,
        "cat_activa": cat_activa,
        "q": q,
        "cart_count": cart_count,
    })


def detalle(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    _, _, cart_count = _cart_detalle(_get_cart(request))
    return render(request, "detalle.html", {"producto": producto, "cart_count": cart_count})


def vista_registro(request):
    if request.user.is_authenticated:
        return redirect("tienda")
    form = RegistroForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f"Bienvenido/a, {user.username}.")
        return redirect("tienda")
    return render(request, "registro.html", {"form": form})


def vista_login(request):
    if request.user.is_authenticated:
        return redirect("panel_admin" if request.user.is_staff else "tienda")
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f"Hola, {user.username}.")
        nxt = request.GET.get("next") or request.POST.get("next") or ""
        if nxt:
            return redirect(nxt)
        return redirect("panel_admin" if user.is_staff else "tienda")
    return render(request, "login.html", {"form": form})


def vista_logout(request):
    logout(request)
    messages.info(request, "Sesión cerrada.")
    return redirect("tienda")


def carrito_ver(request):
    items, total, count = _cart_detalle(_get_cart(request))
    return render(request, "carrito.html", {"items": items, "total": total, "cart_count": count})


def carrito_agregar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    cart = _get_cart(request)
    actual = int(cart.get(str(pk), 0))
    if producto.stock <= 0:
        messages.error(request, f"{producto.nombre} está sin stock.")
    elif actual + 1 > producto.stock:
        messages.error(request, f"Solo quedan {producto.stock} de {producto.nombre}.")
    else:
        cart[str(pk)] = actual + 1
        _save_cart(request, cart)
        messages.success(request, f"{producto.nombre} agregado al carrito.")
    return redirect("carrito")


def carrito_quitar(request, pk):
    cart = _get_cart(request)
    cart.pop(str(pk), None)
    _save_cart(request, cart)
    return redirect("carrito")


def carrito_actualizar(request, pk):
    cart = _get_cart(request)
    try:
        cant = int(request.POST.get("cantidad", 1))
    except ValueError:
        cant = 1
    producto = get_object_or_404(Producto, pk=pk)
    if cant <= 0:
        cart.pop(str(pk), None)
    elif cant > producto.stock:
        messages.error(request, f"Stock máximo: {producto.stock}.")
        cart[str(pk)] = producto.stock
    else:
        cart[str(pk)] = cant
    _save_cart(request, cart)
    return redirect("carrito")


@login_required
@transaction.atomic
def checkout(request):
    if request.method != "POST":
        return redirect("carrito")
    cart = _get_cart(request)
    if not cart:
        messages.info(request, "Tu carrito está vacío.")
        return redirect("tienda")
    ids = [int(k) for k in cart.keys()]
    productos = {p.id: p for p in Producto.objects.filter(id__in=ids)}
    for pid_str, cant in cart.items():
        p = productos.get(int(pid_str))
        if not p or int(cant) > p.stock:
            nombre = p.nombre if p else f"#{pid_str}"
            messages.error(request, f"Sin stock suficiente de {nombre}. Ajusta tu carrito.")
            return redirect("carrito")
    total = sum(productos[int(pid)].precio * int(cant) for pid, cant in cart.items())
    pedido = Pedido.objects.create(usuario=request.user, total=total)
    for pid_str, cant in cart.items():
        p = productos[int(pid_str)]
        cant = int(cant)
        DetallePedido.objects.create(
            pedido=pedido, producto=p, nombre_producto=p.nombre,
            cantidad=cant, precio_unitario=p.precio,
        )
        p.stock -= cant
        p.save()
    _save_cart(request, {})
    messages.success(request, f"Compra exitosa. Pedido #{pedido.id} por ${total}. ¡Stock actualizado!")
    return redirect("mis_pedidos")


@login_required
def mis_pedidos(request):
    pedidos = request.user.pedidos.prefetch_related("detalles").all()
    _, _, cart_count = _cart_detalle(_get_cart(request))
    return render(request, "mis_pedidos.html", {"pedidos": pedidos, "cart_count": cart_count})


@login_required
@user_passes_test(es_admin)
def panel_admin(request):
    productos = Producto.objects.select_related("categoria").all()
    return render(request, "admin_panel.html", {"productos": productos})


@login_required
@user_passes_test(es_admin)
def producto_crear(request):
    form = ProductoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Producto creado.")
        return redirect("panel_admin")
    return render(request, "producto_form.html", {"form": form, "titulo": "Nuevo producto"})


@login_required
@user_passes_test(es_admin)
def producto_editar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    form = ProductoForm(request.POST or None, instance=producto)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Producto actualizado.")
        return redirect("panel_admin")
    return render(request, "producto_form.html", {"form": form, "titulo": f"Editar: {producto.nombre}"})


@login_required
@user_passes_test(es_admin)
def producto_eliminar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        producto.delete()
        messages.success(request, "Producto eliminado.")
        return redirect("panel_admin")
    return render(request, "producto_confirmar.html", {"producto": producto})


@login_required
@user_passes_test(es_admin)
def categorias_admin(request):
    form = CategoriaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Categoría creada.")
        return redirect("categorias_admin")
    categorias = Categoria.objects.all()
    return render(request, "categorias.html", {"categorias": categorias, "form": form})
