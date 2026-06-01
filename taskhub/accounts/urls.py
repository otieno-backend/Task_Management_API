from django.urls import path
from .views import RegisterView, LoginView, LogoutView,AdminDashboardView,UserDashboardView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("admin/dashboard/", AdminDashboardView.as_view(), name="admin-dashboard"),
    path("user/dashboard/", UserDashboardView.as_view(), name="user-dashboard"),
]
