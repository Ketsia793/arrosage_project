from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PlanteViewSet, LinkUserToPlanteAPIView, UpdatePlanteDataAPIView

# Création du routeur pour l'API
router = DefaultRouter()
router.register(r'users', UserViewSet)  
router.register(r'plantes', PlanteViewSet)  

# URLs de l'API
urlpatterns = [
    path('', include(router.urls)), 
    path('api-token-auth/', views.obtain_auth_token),  

    # Route pour lier un utilisateur à une plante
    path('link-user-to-plante/', LinkUserToPlanteAPIView.as_view(), name='link-user-to-plante'),
    path('api/update-plante/', UpdatePlanteDataAPIView.as_view(), name='update-plante-data'),
]
