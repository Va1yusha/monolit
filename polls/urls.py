from django.urls import path
from . import views


app_name = 'polls'
urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('register/', views.register, name='register'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),

    path('home/', views.IndexView.as_view(), name='index'),
    path('create/', views.create_question, name='create_question'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),

]