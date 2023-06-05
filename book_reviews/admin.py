from django.contrib import admin
from .models import Categoria
from .models import Autor
from .models import Libro
from .models import Review

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Autor)
admin.site.register(Libro)
admin.site.register(Review)


