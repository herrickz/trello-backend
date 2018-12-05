from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from trelloApp.views import BoardApi, ListApi, CardApi

router = routers.DefaultRouter()
router.register('board', BoardApi)
router.register('list', ListApi)
router.register('card', CardApi)

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
