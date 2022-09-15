from django.urls import path
from . import views


urlpatterns = [
     path('publish_score/',views.PublishScoreView.as_view()),
     path('add_user/',views.AddUserView.as_view()),
     path('add_game/',views.AddGameView.as_view()),
     path('get_top_score/<int:count>/',views.GetTopScore.as_view()),
]