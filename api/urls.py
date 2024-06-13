# usamos routers en lugar de path, ya que nos permiten hacer varias operaciones
# que gestiona Django como un CRUD (get, post, delete, etc..)
from rest_framework import routers
from .views import PropiedadesViewSet

app_name = "api_propiedades"

router = routers.DefaultRouter()  # Es clave porque lo gestiona Django (get, post, delete, etc..)
router.register("propiedades", PropiedadesViewSet, "propiedades_api")

urlpatterns = router.urls
