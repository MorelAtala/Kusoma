from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from .models import *
from .forms import OrderForm
from .filters import OrderFilter

def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()

	
	total_customers = customers.count()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()
	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs 


	context = {'orders':orders, 'customers':customers,
	'total_orders':total_orders,'delivered':delivered,
	'pending':pending, 'myFilter':myFilter, 'total_customers':total_customers}
	
	return render(request, 'todo/dashboard.html', context)


def products(request):
	products = Product.objects.all()
	return render(request, 'todo/products.html', {'products':products})


def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)

	orders = customer.order_set.all()
	order_count = orders.count()

	context = {'customer':customer, 'orders':orders, 'order_count':order_count}
	return render(request, 'todo/customer.html',context)


def createOrder(request):
	form = OrderForm()
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'todo/order_form.html', context)

def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'todo/order_form.html', context)

def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'todo/delete.html', context)


