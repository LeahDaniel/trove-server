"""trove URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from troveapi.views import (AuthorView, BookRecommendationView, BookView,
                            GameView, PlatformView, StreamingServiceView,
                            TagView, UserView, login_user, register_user)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'games', GameView, 'game')
router.register(r'platforms', PlatformView, 'platform')
router.register(r'tags', TagView, 'tag')
router.register(r'books', BookView, 'book')
router.register(r'users', UserView, 'user')
router.register(r'authors', AuthorView, 'author')
router.register(r'book_recommendations', BookRecommendationView, 'bookRecommendation')
router.register(r'streaming_services', StreamingServiceView, 'streaming service')


urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
