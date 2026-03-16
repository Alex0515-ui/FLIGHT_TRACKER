from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # Логин будущий
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Обновление токена
    path('api/', include('users.urls')), # Пока только пользователя зарегал
    path('api/', include('subscriptions.urls')),
    path("api/", include('flights.urls'))
]
