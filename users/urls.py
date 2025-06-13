from django.urls import path
# from .views import CreateUserView
from users.views import UsersView

urlpatterns = [
    # path('create-user', CreateUserView.as_view(), name='users-create'),
    path('', UsersView.as_view(), name='users-list'),
] 