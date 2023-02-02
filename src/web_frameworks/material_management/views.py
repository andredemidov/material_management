from django.shortcuts import render
from .models import ObjectType

# Create your views here.

def test_view():
    types = ObjectType.objects