from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from rest_framework import routers
from .views import UserViewSet, MatchViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'matches', MatchViewSet)

urlpatterns = [
    path("login/", views.login, name="login"),
    path("register/", views.reg, name="reg"),
    path("logout/", views.logout, name="logout"),
    path("", views.index, name="home"),
    path("create/", views.create, name="create"),
    path("match/", views.matches, name="matches"),
    path("match/<int:match_id>/", views.match, name="match"),
    path("api/", include(router.urls)),

]
