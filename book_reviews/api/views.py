from rest_framework.viewsets import ModelViewSet
from book_reviews.models import Categoria, Autor
from book_reviews.api.serializers import CategoriaSerializer, AutorSerializer

class CategoriaApiViewSet(ModelViewSet):
    serializer_class = CategoriaSerializer
    queryset = Categoria.objects.all()

class AutorApiViewSet(ModelViewSet):
    serializer_class = AutorSerializer
    queryset = Autor.objects.all()
