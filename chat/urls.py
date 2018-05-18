from django.urls import path
from . import views

urlpatterns = [
    path('send/input', views.SendInputView.as_view(), name='send-input'),
    path('send/response', views.SendResponseView.as_view(), name='send-response'),
    path('create/user', views.CreateUserView.as_view(), name='create-user'),
    path('get/response', views.GetResponse.as_view(), name="get-response"),
    path('submit/query', views.SubmitQuery.as_view(), name="submit-query")
]