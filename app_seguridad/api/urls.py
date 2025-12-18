from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    UsuarioViewSet, 
    IncidenciaViewSet, 
    AlertaViewSet,
    NotificacionViewSet,
    register,
    login_view,
    health_check
)

# Router para los ViewSets
router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'incidencias', IncidenciaViewSet, basename='incidencia')
router.register(r'alertas', AlertaViewSet, basename='alerta')
router.register(r'notificaciones', NotificacionViewSet, basename='notificacion')

urlpatterns = [
    # Health check
    path('health/', health_check, name='health_check'),
    
    # Autenticación endpoints
    path('auth/login/', login_view, name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', register, name='register'),
    path('auth/user/', UsuarioViewSet.as_view({'get': 'me'}), name='current_user'),
    
    # Endpoints de los ViewSets
    path('', include(router.urls)),
]
