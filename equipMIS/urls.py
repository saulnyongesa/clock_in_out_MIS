from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from base import views
from django.contrib.auth import views as auth_views
from base.forms import PWDChangeView
from equipMIS import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home-url'),
    path('clock/', include('app.urls')),
    path('base/', include('base.urls')),
    path('hospital/', include('hospital.urls')),
]

# Password and account related urls===========================================
urlpatterns += [
    path('password-change/', PWDChangeView.as_view(template_name='pwd/pwd-change.html'), name='change-pwd-url'),
    path('reset_pwd/', auth_views.PasswordResetView.as_view(template_name='pwd/pwd-reset.html'),
         name='reset_password'),
    path('reset_pwd_done/',
         auth_views.PasswordResetDoneView.as_view(template_name='pwd/done.html'),
         name='password_reset_done'),
    path('reset_pwd/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='pwd/confirm.html'),
         name='password_reset_confirm'),
    path('reset_pwd_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='pwd/complete.html'),
         name='password_reset_complete'),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
