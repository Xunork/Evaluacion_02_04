from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Producto, Categoria


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=False, label="Correo")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        labels = {"username": "Usuario"}


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "precio", "stock", "categoria", "descripcion"]
        labels = {
            "nombre": "Nombre",
            "precio": "Precio ($)",
            "stock": "Stock",
            "categoria": "Categoría",
            "descripcion": "Descripción",
        }
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
        }


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nombre", "descripcion"]
