from django.urls import path
from . import views

urlpatterns = [
  path('<int:id>',views.home,name = 'home'),
  path('menu/',views.menu,name = 'menu'),
  path('add/',views.add,name='add'),
  path('cart/',views.cart,name='cart'),
]
