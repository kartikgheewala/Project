from django.urls import path
from . import views

# Create urls here.

urlpatterns = [
      path('', views.Index),
      path('Reg', views.Reg_View),
      path('Registration', views.Registration_View),
      path('OTP', views.Reg_OTP),
      path('Conform_OTP', views.Conform_OTP),
      path('Logout', views.Logout),
      path('Login', views.Login),
      path('Home', views.Home),
      path('Profile', views.Profile),
      path('Send_Message', views.Send_Message),
      path('<int:id>/Update_Profile', views.Update_Profile),
      path('<int:id>/Update_Image', views.Update_Image),

]
