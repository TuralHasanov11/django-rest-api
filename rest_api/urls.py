from django.contrib import admin
from django.urls import path, include
from auth_user import views as authViews
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('blog/', include('blog.urls', 'blog')),
    path('register/', authViews.register, name='register'),
    path('logout/', authViews.signout, name='logout'),
    path('login/', authViews.signin, name='login'),
    path('must_authenticate/', authViews.mustAuth, name='must_auth'),
    path('profile/', authViews.profile, name='profile'),
    path('auth/password_change/', auth_views.PasswordChangeView.as_view(template_name='auth/password_change.html'), name='password_change'),
    path('auth/password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='auth/password_change_done.html'), name='password_change_done'),
    path('auth/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('auth/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('auth/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('auth/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name='password_reset_complete'),

    # API
    path('api/blog/', include('blog.api.urls', 'blog_api')),
    path('api/auth/', include('auth_user.api.urls', 'auth_api')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)