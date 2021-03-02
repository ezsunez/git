from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.welcome, name='welcom'),
    # path('<int:question_id>/<int:i>', views.detail, name='detail'),
    path('detail/<int:a_id>', views.detail,name='detail'),
    path('frame', views.frame),

]