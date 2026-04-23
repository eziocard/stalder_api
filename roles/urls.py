from rest_framework import routers

from roles.views import RoleViewSet

router = routers.DefaultRouter()

router.register('roles', RoleViewSet, 'roles')

urlpatterns = router.urls