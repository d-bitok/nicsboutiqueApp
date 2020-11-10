from django.contrib.auth.models import User
from django.http import request
from django.shortcuts import render, get_object_or_404
from .models import *
import json
import datetime
from .utils import cookieCart, cartData, guestOrder
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

def home(request):
    context = {
        'posts': Post.objects.all(),
        'title': 'Forum'
    }
    return render(request, 'boutiqueApp/home.html', context)

@login_required
def store(request):
    if request == 'GET':
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print('CART:', cart)
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]["quantity"]

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["quantity"]

            item = {
                'product':{
                    #'id':product.id,
                    'productName':product.productName,
                    'price':product.price,
                    'designer':product.designer,
                    'price':product.price,
                    'digital':product.digital,
                    #'date_added':product.date_added,
                    'imageURL':product.imageURL,
                    'description':product.description,
                    'designer':product.designer
                    },
                'quantity':cart[i]["quantity"],
                'get_total':total,
                }
            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass

    products = Product.objects.all().order_by('-date_added')
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 6)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {'products':products, 'paginator':paginator, 'cartItems':cartItems}
    return render(request, 'boutiqueApp/store.html', context)

def boutique(request):
    if request == 'GET':
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print('CART:', cart)
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]["quantity"]

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["quantity"]

            item = {
                'product':{
                    #'id':product.id,
                    'productName':product.productName,
                    'price':product.price,
                    'designer':product.designer,
                    'price':product.price,
                    'digital':product.digital,
                    #'date_added':product.date_added,
                    'imageURL':product.imageURL,
                    'description':product.description,
                    'designer':product.designer
                    },
                'quantity':cart[i]["quantity"],
                'get_total':total,
                }
            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass

    products = Product.objects.all().order_by('-date_added')
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 6)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {'products':products, 'paginator':paginator, 'cartItems':cartItems}
    return render(request, 'boutiqueApp/boutique.html', context)

class StoreListView(ListView):
    model = Product
    template_name = 'boutiqueApp/boutique.html'
    context_object_name = 'products'
    ordering = ['-date_added']
    paginate_by = 6

def productDetail(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'boutiqueApp/product_detail.html', context)

class ProductDetailView(DetailView):
    model = Product

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['designer', 'productName', 'price', 'digital', 'image', 'description']

    #def form_valid(form):
        #form.instance.user = self.request.user
        #return super().form_valid(form)
    
class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['designer', 'productName', 'price', 'digital', 'image', 'description']

    #def form_valid(form):
        #form.instance.user = self.request.user
        #return super().form_valid(form)

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.designer:
            return True
        return False

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = '/'

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.designer:
            return True
        return False

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

class PostListView(ListView):
    model = Post
    template_name = 'boutiqueApp/home.html'     # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'boutiqueApp/user_posts.html'     # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request,'boutiqueApp/about.html', {'title':'About'})

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items' : items, 'order' : order, 'title':'Cart', 'cartItems': cartItems}
    return render(request, 'boutiqueApp/cart.html', context)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment Complete!', safe=False)

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        'items' : items,
        'order' : order,
        'title':'Checkout',
        'cartItems': cartItems
    }
    return render(request, 'boutiqueApp/checkout.html', context)
