from rest_framework.routers import DefaultRouter
from book_reviews.api.views import CategoriaApiViewSet, AutorApiViewSet

router_categorias = DefaultRouter()
router_autor = DefaultRouter()

router_categorias.register(prefix='categoria', basename='categoria', viewset=CategoriaApiViewSet)
router_autor.register(prefix='autor', basename='autor', viewset=AutorApiViewSet)