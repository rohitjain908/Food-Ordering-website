from django.shortcuts import render,redirect
from accounts.models import *
from restaurant.models import *
from .models import *
# Create your views here.
 
def home(request,id):
	customer = Customer.objects.get(id=id)
	# print(customer.id)
	request.session["cust_id"] = id
	# if customer.is_login:

	restaurant = Resturant.objects.all()
	return render(request,'home.html',{'restaurant' : restaurant,'customer' : customer})

def menu(request):
	if request.method == 'POST':
		rest_id = request.POST.get('try')
		cust_id = request.session["cust_id"]
		print(cust_id)
		restaurant = Resturant.objects.get(id =rest_id)
		dish = Dish.objects.filter(owner = restaurant.owner)
		if Customer.objects.filter(id = cust_id).exists():
			customer = Customer.objects.get(id = cust_id)
			if Order.objects.filter(customer = customer,restaurant_id = restaurant.id, complete = False).exists():
				order = Order.objects.get(customer = customer,restaurant_id = restaurant.id, complete = False)

			else:
				order = Order.objects.create(customer = customer,restaurant_id = restaurant.id, complete = False)
				order.save()
				print(order)

			return render(request,'menu.html',{'dish' : dish,'customer' : customer, 'rest_id' : rest_id, 'order' : order})
		else:
			customer = None
			return render(request,'menu.html',{'dish' : dish,'customer' : customer, 'rest_id' : rest_id})
	

def add(request):
	if request.method == 'POST':	
		dish_id = request.POST.get('try')
		dish = Dish.objects.get(id = dish_id)
		cust_id = request.session["cust_id"]
		customer = Customer.objects.get(id = cust_id)
		owner = dish.owner
		restaurant = Resturant.objects.get(owner = owner)

		if Order.objects.filter(customer = customer,restaurant_id = restaurant.id, complete = False).exists():
			order = Order.objects.get(customer = customer,restaurant_id = restaurant.id, complete = False)

		else:
			order = Order.objects.create(customer = customer,restaurant_id = restaurant.id, complete = False)
			order.save()
			print(order)

		if Orderdish.objects.filter(order = order,dish = dish).exists():
			orderdish = Orderdish.objects.get(order = order,dish = dish)
			orderdish.quantity = (orderdish.quantity + 1)
			orderdish.save()

		else:
			orderdish = Orderdish.objects.create(order = order,dish = dish,quantity = 1)
			orderdish.save()
		alldish = Dish.objects.filter(owner = owner)
		return render(request,'menu.html',{'dish' : alldish,'customer' : customer, 'order' : order, 'rest_id' : restaurant.id})
	else:
		return redirect('customer_login')


def cart(request):
	cust_id = request.session["cust_id"]
	customer = Customer.objects.get(id = cust_id)
	rest_id = request.POST.get('restid')
	restaurant = Resturant.objects.get(id = rest_id)

	if Order.objects.filter(customer = customer,restaurant_id = restaurant.id, complete = False).exists():
			order = Order.objects.get(customer = customer,restaurant_id = restaurant.id, complete = False)

	else:
		order = Order.objects.create(customer = customer,restaurant_id = restaurant.id, complete = False)
		order.save()
		print(order)

	items = Orderdish.objects.filter(order = order).all()
	context = {'items':items,'order':order}
	return render(request,'cart.html',context)