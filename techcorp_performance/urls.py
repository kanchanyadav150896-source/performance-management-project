from django.urls import path, include
from django.contrib import admin



schema_view = get_schema_view(
   openapi.Info(
      title="TechCorp Performance Management API",
      default_version='v1',
      description="API documentation for TechCorp PMS",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/', include('reviews.urls')),
    path('api/goals/', include('goals.urls')),
    path('api/', include('reviews.urls_outliers')),


    
    # Swagger URLs
    path('swagger(<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
