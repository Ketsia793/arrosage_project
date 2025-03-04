from django.urls import path
from .import views 
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('users/count/', views.CountUser, name="Countusers"),
    path('users/create/', views.create_user, name="create_user"),
    path('users/profile/', views.get_user_profil, name="get_user_profile"),
    path('users/profile/put/', views.put_user_profil, name="put_user_profile"),
    path('users/delete/', views.delete_user, name="delete_user"),
    path('users/id/', views.get_userId, name="get_user_id"),
    # path('auth/signup/', views.create_user, name="signup"),
    path('auth/login/', TokenObtainPairView.as_view(), name="login"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
