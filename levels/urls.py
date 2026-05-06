from rest_framework import routers

from levels.views import LevelViewSet

router = routers.DefaultRouter()
router.register('levels', LevelViewSet, basename='levels')

urlpatterns = router.urls