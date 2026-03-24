"""Main API URL routing for Campus Guardian."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    UsuarioViewSet, 
    IncidenciaViewSet, 
    AlertaViewSet,
    NotificacionViewSet,
    ComentarioViewSet,
    register,
    login_view,
    health_check,
    listar_usuarios,
    crear_usuario_seguridad,
    eliminar_usuario,
    chatbot_view
)

# Register API viewsets in a single DRF router.
router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'incidencias', IncidenciaViewSet, basename='incidencia')
router.register(r'alertas', AlertaViewSet, basename='alerta')
router.register(r'notificaciones', NotificacionViewSet, basename='notificacion')
router.register(r'comentarios', ComentarioViewSet, basename='comentario')

urlpatterns = [
    # Health check
    path('health/', health_check, name='health_check'),
    
    # Authentication endpoints.
    path('auth/login/', login_view, name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', register, name='register'),
    path('auth/user/', UsuarioViewSet.as_view({'get': 'me'}), name='current_user'),
    
    # Admin-only user management endpoints.
    path('admin/usuarios/', listar_usuarios, name='admin_listar_usuarios'),
    path('admin/usuarios/seguridad/', crear_usuario_seguridad, name='admin_crear_seguridad'),
    path('admin/usuarios/<int:pk>/', eliminar_usuario, name='admin_eliminar_usuario'),
    
    # Chatbot endpoint
    path('chatbot/', chatbot_view, name='chatbot'),
    
    # Include all router-generated endpoints.
    path('', include(router.urls)),
]
