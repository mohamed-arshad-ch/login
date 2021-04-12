from .views import RegisterAPI,GetDetails,LoginAPI,GetAllDetails
from django.urls import path
from knox import views as knox_views


urlpatterns = [
    path('api/v1/register/', RegisterAPI.as_view(), name='register'),
    path('api/v1/user/<slug:slug>',GetDetails.as_view()),
    path('api/v1/login/', LoginAPI.as_view(), name='login'),
    path('api/v1/all/', GetAllDetails.as_view(), name='login'),

    path('api/v1/logout/', knox_views.LogoutView.as_view(), name='logout'),
]