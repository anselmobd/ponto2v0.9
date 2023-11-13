from django.contrib.auth import views as auth_views
from django.urls import include, path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from ponto2.admin import admin
from ponto2.views import index


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('bordado/', include('bordado.urls')),

    # Autenticação
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(template_name="layout/login.html"),
        name='login',
    ),
    path(
        'encerrar/',
        auth_views.LogoutView.as_view(next_page="/"),
        name='encerrar',
    ),


]
