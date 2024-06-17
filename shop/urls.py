from django.urls import path
from shop import views


urlpatterns = [
    path('boardgames_list/', views.BoardgameListView.as_view(), name='boardgames_list'),
    path('boardgame_details/<int:pk>', views.BoardgameDetailView.as_view(), name='boardgame_details'),
    path('boardgame_add/', views.BoardgameAddView.as_view(), name='boardgame_add'),
    path('boardgame_update/<int:pk>', views.BoardgameUpdateView.as_view(), name='boardgame_update'),
    path('boardgame_delete/<int:pk>', views.BoardgameDeleteView.as_view(), name='boardgame_delete'),
    path('cart_list/', views.CartListView.as_view(), name='cart_list'),
    path('add_boardgame_to_cart/<int:boardgame_pk>/', views.AddBoardgameToCartView.as_view(),
         name='add_boardgame_to_cart'),
    path('delete_boardgame_from_cart/<int:boardgame_pk>/', views.DeleteBoardgameFromCartView.as_view(),
         name='delete_boardgame_from_cart'),
    path('make_order/', views.MakeOrderView.as_view(), name='make_order'),
    path('orders_list/', views.OrdersListView.as_view(), name='orders_list'),
    path('order_detail/<int:pk>', views.OrderDetailView.as_view(), name='order_detail'),
    path('review_add/<int:boardgame_pk>/', views.ReviewAddView.as_view(), name='review_add'),
    path('review_detail/<int:pk>/', views.ReviewDitailView.as_view(), name='review_detail'),
    path('review_update/<int:pk>/', views.ReviewUpdateView.as_view(), name='review_update'),
    path('review_delete/<int:pk>/', views.ReviewDeleteView.as_view(), name='review_delete'),
    path('reviews_list/<int:boardgame_pk>/', views.ReviewsListView.as_view(), name='reviews_list'),
]
