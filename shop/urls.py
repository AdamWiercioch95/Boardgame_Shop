from django.urls import path
from shop import views


urlpatterns = [
    path('boardgames_list/', views.BoardgameListView.as_view(), name='boardgames_list'),
    path('boardgame_details/<int:pk>', views.BoardgameDetailView.as_view(), name='boardgame_details'),
    path('boardgame_add/', views.BoardgameAddView.as_view(), name='boardgame_add'),
    path('boardgame_update/<int:pk>', views.BoardgameUpdateView.as_view(), name='boardgame_update'),
    path('boardgame_delete/<int:pk>', views.BoardgameDeleteView.as_view(), name='boardgame_delete'),
]
