from django.urls import path

from base import views

urlpatterns = [
    path('', views.dashboard, name='admin-dashboard-url'),
]
urlpatterns += [
    path('sign-in/', views.sign_in, name='sign-in-url'),
    path('sign-out/', views.sign_out, name='sign-out-url'),
]
# Department Admin sign up=======================================================
urlpatterns += [
    path('Admin/Signup', views.admin_signup, name='admin-signup-url'),
    path('Admin/status/<pk>', views.admin_status, name='admin-status-url'),
    path('Admin/list/', views.admin_list, name='admin-list-url'),
    path('Admin/list/active/', views.admin_list_active_only, name='admin-list-active-url'),
    path('Admin/list/inactive/', views.admin_list_inactive_only, name='admin-list-inactive-url'),
    path('user/details/', views.user_details, name='user-details-url'),
    path('user/details/<pk>', views.other_user_details, name='other-user-details-url'),
    path('user/edit/', views.edit_user, name='edit-user-url'),
    path('user/edit/<pk>', views.edit_other_user, name='edit-other-user-url'),
]
