from rest_framework.serializers import ModelSerializer
from book_reviews.models import Categoria, Autor

class CategoriaSerializer(ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']

class AutorSerializer(ModelSerializer):
    class Meta:
        model = Autor
        fields = ['id', 'nombre', 'foto', 'resumen', 'pais', 'fecha_nacimiento']