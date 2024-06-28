from django.urls import path
from account.views import Userprofile,UserLogin,Userviews,StudentAllData,TeachersAllData,StudentIDData,TeacherIDData,MeViews

urlpatterns = [
    path('register/', Userprofile.as_view(), name='user-profile'),  
    path('login/', UserLogin.as_view(), name='user-login'),
    path('student/',StudentAllData.as_view(), name="student-detail"),
    path('teacher/',TeachersAllData.as_view(),name='teachers-details'),
    path('student/<int:pk>/', StudentIDData.as_view(), name='user-detail'),
    path('teacher/<int:pk>/', TeacherIDData.as_view(), name='user-detail'),
    path('user/',Userviews.as_view(),name="user-detail"),
    path('me/',MeViews.as_view(),name="my-details")
]