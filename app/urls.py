from django.urls import path

from app import views

urlpatterns = [
    path('', views.dashboard, name='clock-dashboard-url'),
]
urlpatterns += [
    path('trainer/signup/', views.trainer_signup, name='trainer-signup-url'),
    path('trainer/edit/<pk>', views.trainer_edit, name='trainer-edit-url'),
    path('trainer/unit/assign/', views.assign_trainer_to_unit, name='assign-trainer-to-unit-url'),
    path('trainer/unit/assign/<pk>', views.assign_trainer_to_unit_from_trainer_list, name='assign-trainer-to-unit'
                                                                                          '-from-list-url'),
    path('trainer/unit/assign/rm/<pk>', views.remove_assigned_unit, name='remove-assigned-unit-url'),
    path('trainers/status/<pk>', views.trainer_status, name='trainer-status-url'),
    path('trainers/list/', views.trainer_list, name='trainer-list-url'),
    path('trainers/list/active/', views.trainer_list_active_only, name='trainer-list-active-url'),
    path('trainers/list/inactive/', views.trainer_list_inactive_only, name='trainer-list-inactive-url'),
]

# Students information urls ==================================================================
urlpatterns += [
    path('student/signup/', views.student_signup, name='student-signup-url'),
    path('student/edit/<pk>', views.student_edit, name='student-edit-url'),
    path('student/status/<pk>', views.student_status, name='student-status-url'),
    path('student/list/', views.student_list, name='student-list-url'),
    path('student/list/active/', views.student_list_active_only, name='student-list-active-url'),
    path('student/list/inactive/', views.student_list_inactive_only, name='student-list-inactive-url'),
    path('generate/excel/all/student/', views.generate_excel_for_student_all, name='generate-excel-all-student-url'),
]

# Unit urls ==================================================================
urlpatterns += [
    path('unit/signup/', views.unit_signup, name='unit-signup-url'),
    path('unit/edit/<pk>', views.unit_edit, name='unit-edit-url'),
    path('unit/all/', views.units_list, name='units-url'),
]
# Teaching clock in/out admin dashboard=========================================================
urlpatterns += [
    path('teaching/clock/', views.clock, name='clock-url'),
    path('teaching/clockin/<pk>', views.clock_in, name='clock-in-url'),
    path('teaching/clockout/<pk>', views.clock_out, name='clock-out-url'),
    path('teaching/clock-history/', views.clock_history, name='clock-history-url'),
    path('teaching/clock/list/', views.clock_list, name='clock-list-url'),
    path('teaching/active-classes/', views.active_classes, name='active-classes-url'),
]

# Teaching clock in/out after face recognition=========================================================
urlpatterns += [
    path('teaching/clock_in/unit_data/', views.get_unit_data, name='get-unit-data-url'),
    path('teaching/clock/before-face/', views.clock_face_recognition, name='clock-face-url'),
    path('teaching/clock/after-face/<pk>', views.clock_after_face_recognition, name='clock-after-face-url'),
    path('teaching/clock/face-recognizer/', views.face_recognition_view, name='face-recognition-url'),
    path('teaching/clockin/face/<pk>', views.clock_in_after_face_recognition, name='clock-in-face-url'),
    path('teaching/clockout/face/<pk>', views.clock_out_after_face_recognition, name='clock-out-face-url'),
]

# Generate excel ==================================================================
urlpatterns += [
    path('generate/excel/<pk>', views.generate_excel_for_clock_history, name='generate-excel-url'),
    path('generate/excel/all/', views.generate_excel_for_clock_all, name='generate-excel-all-url'),
]
# Generate PDF ==================================================================
urlpatterns += [
    path('generate/PDF/', views.generate_pdf, name='generate-pdf-url'),
]
