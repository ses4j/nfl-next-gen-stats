from . import views
from django.urls import include, path

urlpatterns = [
    path('', views.home, name='home'),
    path('player-search/', views.SearchResultsView.as_view(), name='player-search'),
    path('player/<str:gsis_id>/', views.player_page, name='player-page'),
    path('player/<str:gsis_id>/<int:season>/', views.player_page, name='player-season')
]