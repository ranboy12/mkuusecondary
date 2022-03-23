from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import DistrictAutocomplete

app_name = 'SRS'

urlpatterns = [
    path('', views.index, name="login"),
    path('student-entry/', views.student_entry, name="entry"),
    path('staff-entry-template/', views.staff_entry_template, name="staff_entry_template"),
    path('staff-entry-update/<object_pk>', views.update_staff_detail, name="update_staff_detail"),
    path('student-entry-update/<object_pk>', views.update_student_detail, name="update_student_detail"),
    path('update-teaching-workload/<object_pk>', views.update_teaching_workload, name="update_teaching_workload"),
    path('staff-entry/', views.staff_entry, name="staff_entry"),
    path('staff/', views.home, name="home"),
    path('upload-staff/', views.import_staff, name="import_staff"),
    path('subject-list/', views.subject_list, name="subject"),
    path('student-academic-year/', views.student_academic_year, name="student_academic_year"),
    path('Combination-Subjects-list/', views.combination_subject_list, name="combination_subject_list"),

    path('classes-combination-coordinator_results/<rank>', views.coordinator_classes_combination_results,
         name="coordinator_classes_combination_results"),

    path('academic-event/', views.academic_events, name="academic_event"),
    path('academic-year_result/<rank>/<combination>', views.event_result, name="event_result"),

    path('send-academic-year_result/<rank>/<combination>', views.send_event_result, name="send_event_result"),
    path('send-Form3-4-academic-year_result/<rank>/<combination>', views.send_event_result_f3_f4,
         name="send_event_result_f3_f4"),
    path('download-template/<subject>/<rank>/', views.download_csv_data, name="download_csv_data"),

    path('coordinator-classes_results/', views.coordinator_classes_results, name="coordinator_classes_results"),

    path('class-results-pdf/<rank>/<combination>', views.download_result, name="download_result"),
    path('parent-download-results-pdf/<rank>/<combination>', views.parent_download_result,
         name="parent_download_result"),

    # URL FOR REGISTRATION PROCESS
    path('fee-payment-structure/', views.payment_structure_list, name="payment_structure_list"),
    path('school-payment-items/', views.payment_items_list, name="payment_items_list"),
    path('financial-year-income/', views.financial_year_income, name="financial_year_income"),
    path('financial-year-incomplete-payment/', views.financial_year_debt, name="financial_year_debt"),

    path('teacher-Subject-list/', views.subject_teacher, name="subject_teacher"),
    path('class-coordinator-list/', views.class_coordinator_list, name="class_coordinator_list"),
    path('subject-result-lists/<rank>/<subject_name>', views.subject_results_list, name="subject_results_list"),
    path('student-character-assessment/<rank>/<combination>', views.student_character, name="student_character"),

    path('available-Schools-list/', views.available_school, name="available_school"),
    path('teaching-Workload-list/', views.workload_setting, name="workload_setting"),

    path('download-selected-student-list/', views.download_admitted_student, name="download_admitted_student"),
    path('registration-home-page/', views.start_registration, name="registration_home"),
    path('registration-phase-one/<entry>', views.register_phase_one, name="start_registration"),
    path('registration-phase-one-save-payments/', views.save_student_payments, name="save_student_payments"),
    path('registration-phase-two/<student>', views.complete_student_registration, name="complete_registration"),

    path('rank-event-results/', views.rank_event_results, name="rank_event_results"),
    path('student-registration-Template/', views.download_csv_template, name="download_csv_template"),
    path('combination-subject-assessment/<rank>/<combination>', views.combination_subjects,
         name="combination_subjects"),
    path('Academic-event-subject-upload/<get__subject>/<rank>', views.subject_result_upload,
         name="subject_result_upload"),

    path('upload-student-character-assessment/<rank>/<combination>', views.student_assessment_result_upload,
         name="student_assessment_result_upload"),

    path('event-subject-result/<rank>/<subject>/<combination>', views.subject_result, name="subject_results"),

    path('download-subject-result-data/<subject>/<rank>/', views.download_subject_result_data,
         name="download_subject_result_data"),

    path('download-student-assessment-template/<rank>/<combination>/', views.download_assessment_template,
         name="download_assessment_template"),
    path('delete-subject-result-data/<subject>/<rank>/', views.delete_subject_result_data,
         name="delete_subject_result_data"),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # autocomplete views
    path('district-auto-complete/', DistrictAutocomplete.as_view(), name='district_autocomplete'),

]

'''
    Password view For reseting password
------------------------------------------
1 - PasswordResetView submit email from user
2 - PasswordResetDoneView email sent successfull
3 - link to password Rest form in email
4 - Password successfully changed
'''
