from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return str(self.nombre)

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    
    def __str__(self):
        return str(self.nombre)

class Libro(models.Model):
    titulo = models.CharField(max_length=100)
    resumen = models.TextField()
    imagen = models.URLField()
    valoracion = models.DecimalField(max_digits=3, decimal_places=2, default=0.00) # Campo de valoración promedio
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    categorias = models.ManyToManyField(Categoria)

    def __str__(self):
        return str(self.titulo)

class Review(models.Model):
    comentario = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    valoracion = models.IntegerField() # Campo de valoración del usuario para el libro

    def __str__(self):
        return str(self.comentario)
