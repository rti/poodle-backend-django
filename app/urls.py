from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views as authtoken_views
from . import views as app_views

router = routers.DefaultRouter()
router.register('items', app_views.ItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth-token/', authtoken_views.obtain_auth_token),
]
