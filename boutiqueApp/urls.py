from django.urls import path
from . import views
from .views import (
    PostListView, 
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    #StoreListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView
)

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
    path('boutique/', views.boutique, name='Boutique-Home'),

    #path('boutique/', StoreListView.as_view(), name='Boutique-Home'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='Product-Detail'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='Product-Update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='Product-Delete'),
    path('product/new/', ProductCreateView.as_view(), name='Product-Create'),
    path('update_item/', views.updateItem, name='Update-Item'),
    path('process_order/', views.processOrder, name='Process-Order'),
]
