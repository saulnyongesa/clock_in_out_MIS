from django.urls import path

from hospital import views

urlpatterns = [
    path('', views.dashboard, name='hospital-dashboard-url')
]
urlpatterns += [
    path('appointments/active/', views.active_appointments, name='active-appointments-url'),
    path('appointments/all/', views.all_appointments, name='all-appointments-url'),
    path('appointments/view/<pk>', views.view_appointment, name='view-appointment-url'),
    path('appointments/reply/<pk>', views.reply_appointment, name='reply-appointment-url'),
    path('appointment/send/<pk>', views.send_appointment, name='send-appointment-url'),
    path('appointment/sender/type/', views.sender_type, name='sender-type-url'),

]
# Students and Staff information urls ==================================================================
urlpatterns += [
    path('student/self/signup/', views.student_signup, name='student-self-signup-url'),
    path('staff/self/signup/', views.staff_signup, name='staff-self-signup-url'),
]
urlpatterns += [
    path('sign-in/hospital/', views.sign_in, name='hospital-sign-in-url'),
    path('sign-out/hospital/', views.sign_out, name='hospital-sign-out-url'),
]
# Department Admin sign up=======================================================
urlpatterns += [
    path('user/details/', views.user_details, name='user-hospital-details-url'),
    path('user/edit/', views.edit_user, name='edit-user-hospital-url'),
]
# Medical Records
urlpatterns += [
    path('medical-records/bio/<pk>', views.bio_data, name='medical-record-bio-url'),
    path('medical-records/vital-signs/<pk>/', views.vital_signs, name='medical-record-vital-signs-url'),
    path('medical-records/complains/<pk>/', views.complains, name='medical-record-complains-url'),
    path('medical-records/hpi/<pk>/', views.hpi, name='medical-record-hpi-url'),
    path('medical-records/past-medical-history/<pk>/', views.past_medical_history, name='medical-record-pmh-url'),
    path('medical-records/family-medical-history/<pk>/', views.family_medical_history, name='medical-record-fmh-url'),
    path('medical-records/examination/<pk>/', views.examination, name='medical-record-examination-url'),
    path('medical-records/diagnosis/<pk>/', views.diagnosis, name='medical-record-diagnosis-url'),
    path('medical-records/findings/<pk>/', views.findings, name='medical-record-findings-url'),
    path('medical-records/treatment/<pk>/', views.treatment, name='medical-record-treatment-url'),

    path('medical-records/patient-search/', views.patient_search, name='patient-search-url'),
    path('medical-records/patient-type/', views.patient_type, name='patient-type-url'),

]
# Students and Staff information urls ==================================================================
urlpatterns += [
    path('student/medical/signup/', views.student_medical_signup, name='student-medical-signup-url'),
    path('staff/medical/signup/', views.staff_medical_signup, name='staff-medical-signup-url'),
]
