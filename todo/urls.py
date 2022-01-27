from django.urls import path
from .views import TodoCreateRetrieve, TodoDetails

urlpatterns = [
    path('todos/', TodoCreateRetrieve.as_view()),
    path('todos/<int:id>/', TodoDetails.as_view())
]