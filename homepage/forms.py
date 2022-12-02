from django.forms import ModelForm
from .models import Cliente
from django import forms
from django.utils.translation import gettext_lazy as _

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'


