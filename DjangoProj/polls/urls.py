from django.urls import include, path

from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.index, name='index'),
    
    path('question/list/', views.QuestionList.as_view(), name='question-list'),
    path('question/create/', views.QuestionCreate.as_view(), name='question-create'),
    path('question/detail/<int:pk>/', views.QuestionDetail.as_view(), name='question-detail'),
    path('question/update/<int:pk>/', views.QuestionUpdate.as_view(), name='question-update'),
    path('question/delete/<int:pk>/', views.QuestionDelete.as_view(), name='question-delete'),
]
