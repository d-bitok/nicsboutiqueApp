from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView

urlpatterns = [
    path('forum/', PostListView.as_view(), name='Boutique-Forum'),
    path('user/<str:username>/', UserPostListView.as_view(), name='User-Posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='Post-Detail'),
    path('post/new/', PostCreateView.as_view(), name='Post-Create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='Post-Update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='Post-Delete'),
    path('about/', views.about, name='Boutique-About'),
    path('', views.store, name='Boutique-Store'),
    path('cart/', views.cart, name='Boutique-Cart'),
    path('checkout/', views.checkout, name='Boutique-Checkout'),
]
