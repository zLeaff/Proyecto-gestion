from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API de Mi Proyecto",
        default_version='v1',
        description="Descripción de mi API",
        terms_of_service="https://www.myapp.com/terms/",
        contact=openapi.Contact(email="contact@myapp.com"),
        license=openapi.License(name="Licencia"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/', include('inventario.urls'))
]