from rest_framework import routers
from attendances.views import AttendanceViewSet

router = routers.DefaultRouter()
router.register('attendance',AttendanceViewSet,'attendances')
urlpatterns = router.urls