from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include('auto_water_system_app.urls')),
    # from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView, TokenVerifyView,
]
    # path("polls/", include("polls.urls")),