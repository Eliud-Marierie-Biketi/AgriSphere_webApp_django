# mainapp/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    HomePageView,
    LoginView,
    SignupView,
    PasswordResetView,
    CreatePostView,
    ViewPostView,
    ViewMyPostsView,
    ReplyPostView,
    AccountSettingsView,
    DeletePostView,
    LogoutView
)

app_name = 'Mainapp'

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('create_post/', CreatePostView.as_view(), name='create_post'),
    path('view_post/<int:pk>/', ViewPostView.as_view(), name='view_post'),
    path('reply_post/<int:pk>/', ReplyPostView.as_view(), name='reply_post'),
    path('view_my_posts/', ViewMyPostsView.as_view(), name='view_my_posts'),
    path('delete_post/<int:pk>/', DeletePostView.as_view(), name='delete_post'),
    path('account_settings/', AccountSettingsView.as_view(), name='account_settings'),
     path('logout/', LogoutView.as_view(), name='logout'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
