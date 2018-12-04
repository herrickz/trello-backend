from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from trelloApp.views import BoardApi, BoardListApi, CardListApi

router = routers.DefaultRouter()
router.register('board', BoardApi)
router.register('list', BoardListApi)
router.register('card', CardListApi)

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
