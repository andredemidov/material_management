from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'objects', views.ObjectViewSet, basename='object')
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'groups', views.GroupViewSet, basename='group')
router.register(r'requirements', views.RequirementsViewSet, basename='requirement')


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', views.index_view),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]