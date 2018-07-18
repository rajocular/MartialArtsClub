from django.urls import path
from django.conf.urls import url
from karate import views
from django.contrib.auth.views import password_reset, password_reset_complete, password_reset_done, password_reset_confirm

app_name = 'karate'

urlpatterns = [
    path(r'', views.admin_login, name='admin_login'),
    path(r'admin_home', views.admin_home, name='admin_home'),
    path(r'admin_logout', views.admin_logout, name='admin_logout'),

    path(r'guest_home', views.guest_home, name='guest_home'),
    path(r'session_expired', views.session_expired, name='session_expired'),

    path(r'student_details', views.student_details, name='student_details'),
    path(r'parent_details', views.parent_details, name='parent_details'),
    path(r'class_details', views.class_details, name='class_details'),
    path(r'attendance_details', views.attendance_details, name='attendance_details'),
    path(r'progress_details', views.progress_details, name='progress_details'),
    path(r'payment_details', views.payment_details, name='payment_details'),

    path(r'student_register', views.student_register, name='student_register'),
    path(r'parent_register', views.parent_register, name='parent_register'),
    path(r'class_register', views.class_register, name='class_register'),
    path(r'attendance_register', views.attendance_register, name='attendance_register'),
    path(r'progress_register', views.progress_register, name='progress_register'),
    path(r'payment_register', views.payment_register, name='payment_register'),

    path(r'parent_check/<int:parent_id>', views.parent_check, name='parent_check'),

    path(r'student_edit/<int:student_id>', views.student_edit, name='student_edit'),
    path(r'parent_edit/<int:parent_id>', views.parent_edit, name='parent_edit'),
    path(r'class_edit/<int:class_id>', views.class_edit, name='class_edit'),
    path(r'attendance_edit/<int:attendance_id>', views.attendance_edit, name='attendance_edit'),
    path(r'progress_edit/<int:progress_id>', views.progress_edit, name='progress_edit'),
    path(r'payment_edit/<int:payment_id>', views.payment_edit, name='payment_edit'),

    path(r'change_password/', views.change_password, name='change_password'),

    path(r'reset-password/', password_reset, {'post_reset_redirect': 'karate:password_reset_done', 'email_template_name': 'karate/reset_email.html'}, name='reset_password'),
    path(r'reset-password/done', password_reset_done, {'template_name': 'karate/reset_done.html'}, name='password_reset_done'),
    url(r'^reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)$', password_reset_confirm, name='BigBoss_reset_confirm'),
    path(r'reset/complete', password_reset_complete, name='BigBoss_reset_complete'),

    path(r'student_delete/<int:student_id>', views.student_delete, name='student_delete'),
    path(r'parent_delete/<int:parent_id>', views.parent_delete, name='parent_delete'),
    path(r'class_delete/<int:class_id>', views.class_delete, name='class_delete'),
    path(r'attendance_delete/<int:attendance_id>', views.attendance_delete, name='attendance_delete'),
    path(r'progress_delete/<int:progress_id>', views.progress_delete, name='progress_delete'),
    path(r'payment_delete/<int:payment_id>', views.payment_delete, name='payment_delete'),

]
