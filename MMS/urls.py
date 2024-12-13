from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # App URLs
    path('users/', include(('users.urls', 'users'), namespace='users')),

    # Swagger/OpenAPI URLs
    path('schema/', SpectacularAPIView.as_view(), name='schema'),  # Generates the schema
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # Swagger UI
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),  # Redoc UI
]