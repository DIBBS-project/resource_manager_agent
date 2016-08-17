from django.conf.urls import include, url
from django.contrib import admin
from rmaapp import views
from rest_framework.routers import DefaultRouter
import rest_framework.authtoken.views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^new_account/$', views.create_account),

]


# Allows to get a token by sending credentials
urlpatterns += [
    url(r'^api-token-auth/', rest_framework.authtoken.views.obtain_auth_token)
]
