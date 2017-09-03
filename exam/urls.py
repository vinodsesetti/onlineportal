from django.conf.urls import url
from . import views

urlpatterns=[
#url(r'^known/$',views.KnownFaces,name="KnownFaces"),
url(r'^$',views.Index,name="indexpage"),
url(r'^signup/$',views.Signup,name="Signup"),
url(r'^signin/$',views.Login,name="Login"),
url(r'^createexam/$',views.CreateExam,name="CreateExam"),
url(r'^exams/$',views.Exams,name="Exams"),
url(r'^signout/$',views.signout,name="signout"),
url(r'^changepassword/$',views.change_password,name="change_password"),
url(r'^forgetpassword/$',views.forget_password,name="forget_password"),
url(r'^profile/$',views.profile,name="profile"),
url(r'^list/$',views.exams_list,name="exams"),
url(r'^(?P<exam_id>[0-9]+)/$',views.exam_detail,name="exam_detail"),
url(r'^(?P<exam_id>[0-9]+)/submit/$', views.submits, name="submit1"),
]
