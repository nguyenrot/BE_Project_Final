from rest_framework.routers import DefaultRouter

# from api_users.views import UserView, RoleView

router = DefaultRouter()

# router.register(r"role", RoleView, basename="role")
# router.register(r"", UserView, basename="user")

urlpatterns = router.urls
