"""D_daignosis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    # path('admin_header/', views.admin_header),
    path('adminhome/', views.adminhome),
    path('logout/', views.logout),
    path('login_get/', views.login_get),
    path('login_post/', views.login_post),


    path('evaluate_model/', views.evaluate_model),
    path('change_password/', views.change_password),
    path('change_password_post/', views.change_password_post),

    path('view_complaint_send/', views.view_complaint_send_reply),
    path("view_comlaint_send_reply_post/", views.view_comlaint_send_reply_post),
    path('send_reply/<id>', views.send_reply),
    path("post_send_reply/", views.post_send_reply),



    path('view_doctor/', views.view_doctor),
    path("aprove_doctor/<id>", views.aprove_doctor),
    path('reject_doctors/<id>', views.reject_doctors),
    path('view_approved_doctor/', views.view_approved_doctor),
    path('view_rejected_doctor/', views.view_rejected_doctor),
    path('view_users/', views.view_users),


    path('view_rewiew_about_doctors/', views.view_review_about_doctors),
    path("view_review_about_post/", views.view_review_about_post),




    path("doctor_signup/", views.doctor_signup),
    path("doctor_signup_post/", views.doctor_signup_post),
    path('doctornhome/', views.doctornhome),
    path("doctor_profile/", views.doctor_profile),
    path('doctor_edit_profile/', views.doctor_edit_profile),
    path('doctor_edit_profile_post/', views.doctor_edit_profile_post),

    path("doctor_REVIEW/", views.doctor_REVIEW),
    path("doctor_REVIEW_post/", views.doctor_REVIEW_post),
    path("doctor_change_password/", views.doctor_change_password),
    path('doctor_change_password_post/', views.doctor_change_password_post),
    # path("doc_view_doctor/", views.doc_view_doctor),
    # path("doctor_add_schedule/", views.doctor_add_schedule),
    path("doctor_appoiment/", views.doctor_appoiment),
    path("doctor_schedule/", views.doctor_schedule),
    path("doctor_add_schedule/",views.doctor_add_schedule),
    path('doctor_add_schedule_post/', views.doctor_add_schedule_post),
    path('delete_schedule/<id>', views.delete_schedule),
    #
    path('User_sendchat/', views.User_sendchat),
    path('User_viewchat/', views.User_viewchat),
    #
    path('doctor_predict_result/', views.doctor_predict_result),
    path('doctor_predict_result_post/', views.doctor_predict_result_post),
    path('doctor_predict_result_voice/', views.doctor_predict_result_voice),
    path('doctor_predict_result_voice_post/', views.doctor_predict_result_voice_post),
    path('doc_upload/<id>', views.doc_upload),
    path('doc_upload_post/<id>', views.doc_upload_post),





    # #################Android
    path('and_login/', views.and_login),
    path('and_signup/', views.and_signup),
    path('and_view_doctor/', views.user_view_doctor),
    path('view_user_reviews/', views.view_user_reviews),
    path('view_user_schedule/', views.view_user_schedule),
    path('and_view_profile/', views.and_view_profile),
    path('and_changepassword/', views.and_changepassword),
    path('and_send_complaint/', views.and_send_complaint),
    path('and_view_complaint_reply/', views.and_view_complaint_reply),
    # path('and_edit_profile/', views.and_edit_profile),
    # path('view_user_schedule/', views.view_user_schedule),
    path('and_user_take_appointment/', views.and_user_take_appointment),
    path('and_user_view_appointment/', views.and_user_view_appointment),
    path('and_user_send_feedback/', views.and_user_send_feedback),
    # path('upload_image/', views.upload_image),
    # path('upload_audio/', views.upload_audio),

]
