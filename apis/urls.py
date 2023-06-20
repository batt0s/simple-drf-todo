from django.urls import path
from apis import views

app_name = "apis"

urlpatterns = [
    path('', views.TodoList.as_view(), name="todos"),
    path('<int:pk>/', views.TodoDetail.as_view(), name="todo"),
]
