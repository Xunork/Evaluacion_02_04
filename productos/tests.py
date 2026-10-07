from django.test import TestCase
from django.contrib.auth.models import User
from .models import Categoria, Producto


class TiendaTest(TestCase):
    def setUp(self):
        self.cat = Categoria.objects.create(nombre="Herramientas")
        self.prod = Producto.objects.create(
            nombre="Martillo", precio=1000, stock=10, categoria=self.cat)
        self.cliente = User.objects.create_user("cliente", password="cliente123")

    def test_producto_queda_en_bd(self):
        self.assertEqual(Producto.objects.count(), 1)

    def test_tienda_muestra_productos_de_la_bd(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Martillo")

    def test_compra_baja_stock(self):
        self.client.login(username="cliente", password="cliente123")
        self.client.get(f"/carrito/agregar/{self.prod.id}/")
        self.client.post("/checkout/")
        self.prod.refresh_from_db()
        self.assertEqual(self.prod.stock, 9)
