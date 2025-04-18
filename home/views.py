from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from . models import *
from django.contrib.auth.decorators import login_required
from django.contrib.messages import success, error
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def index(request): #fetches all cars and displays in the home page
    cars = Car.objects.all()
    return render(request,"index.html",{'cars':cars})

# def index2(request):
#     cars = Car.objects.all()
#     return render(request,"index2.html",{'cars':cars})

# def index3(request):
#     cars = Car.objects.all()
#     return render(request,"index3.html",{'cars':cars})

def customer_signup(request):
    if request.user.is_authenticated:
        return redirect("/home/")
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        phone = request.POST.get('phone')
        city = request.POST.get('city')

        if password1 != password2:
            return redirect("/customer_signup")

        user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password1)
        user.save()
        try:
            location = Location.objects.get(city=city.lower())
        except:
            location = None
        if location is not None:
            customer = Customer(user=user, phone=phone, location=location, type="Customer")
        else:
            location = Location(city=city.lower())
            location.save()
            location = Location.objects.get(city=city.lower())
            customer = Customer(user=user, phone=phone, location=location, type="Customer")
        customer.save()
        alert = True
        return render(request, "customer_signup.html", {'alert':alert})
    return render(request, "customer_signup.html")

def customer_login(request):
    if request.user.is_authenticated:
        return redirect("/home/")
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                user1 = Customer.objects.get(user=user)
                if user1.type == "Customer":
                    login(request, user)
                    return redirect("/customer_homepage")
            else:
                alert = True
                return render(request, "customer_login.html", {'alert':alert})
    return render(request, "customer_login.html")

def car_dealer_signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name','')
        email = request.POST.get('email')
        city = request.POST.get('city')
        phone = request.POST.get('phone')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            return redirect('/car_dealer_signup')

        user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password1)
        user.save()
        try:
            location = Location.objects.get(city = city.lower())
        except:
            location = None
        if location is not None:
            car_dealer = CarDealer(car_dealer=user, phone=phone, location=location, type="Car Dealer")
        else:
            location = Location(city = city.lower())
            location.save()
            location = Location.objects.get(city = city.lower())
            car_dealer = CarDealer(car_dealer = user, phone=phone, location=location, type="Car Dealer")
        car_dealer.save()
        #return render(request, "car_dealer_login.html")
        return redirect("car_dealer_login")
    return render(request, "car_dealer_signup.html")
""" 
def car_dealer_login(request):
    if request.user.is_authenticated:
        return redirect("/all_Cars")
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                user1 = CarDealer.objects.get(car_dealer=user)
                if user1.type == "Car Dealer":
                    login(request, user)
                    return redirect("/all_cars")
                else:
                    alert = True
                    return render(request, "car_dealer_login.html", {"alert":alert})
    return render(request, "car_dealer_login.html")

"""

def car_dealer_login(request):
    if request.user.is_authenticated:
        return redirect("/all_cars")
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                try:
                    user1 = CarDealer.objects.get(car_dealer=user)
                    if user1.type == "Car Dealer":
                        login(request, user)
                        return redirect("/all_cars")
                except CarDealer.DoesNotExist:
                    alert = True
                    return render(request, "car_dealer_login.html", {"alert": alert})
            else:
                alert = True
                return render(request, "car_dealer_login.html", {"alert": alert})
    return render(request, "car_dealer_login.html")

def signout(request): #logsout the user and redirects to home page
    logout(request)
    return redirect('/')

@login_required(login_url='/car_dealer_login')
def add_car(request):
    if request.method == "POST":
        car_name = request.POST.get('car_name')
        city = request.POST.get('city')
        image = request.FILES.get('image')
        capacity = request.POST.get('capacity')
        rent = request.POST.get('rent')
        car_dealer = CarDealer.objects.get(car_dealer=request.user)
        try:
            location = Location.objects.get(city=city)
        except:
            location = None
        if location is not None:
            car = Car(name=car_name, car_dealer=car_dealer, location=location, capacity=capacity, image=image, rent=rent)
            car.save()
        else:
            location = Location(city = city)
            location.save()
            car = Car(name=car_name, car_dealer=car_dealer, location=location, capacity=capacity, image=image, rent=rent)
            car.save()
        alertt = True
        return render(request, "add_car.html", {'alertt':alertt})
    return render(request, "add_car.html") 


@login_required(login_url='/car_dealer_login')
def all_cars(request):
    dealer = CarDealer.objects.filter(car_dealer=request.user).first()
    cars = Car.objects.filter(car_dealer=dealer)
    if request.method == "POST":
        car_id = request.POST.get('car_id')
        car = get_object_or_404(Car, id=car_id)
        return render(request, "edit_car.html", {'car': car})
    return render(request, "all_cars.html", {'cars':cars})


@login_required(login_url='/car_dealer_login')
def edit_car(request):
    if request.method == "POST":
        car_id = request.POST.get('car_id')
        car = get_object_or_404(Car, id=car_id)

        car.name = request.POST.get('car_name')
        car.capacity = request.POST.get('capacity')
        car.rent = request.POST.get('rent')

        city_name = request.POST.get('city')
        if city_name:
            location = Location.objects.filter(city__iexact=city_name).first()
            if location:
                car.location = location
            else:
                location = Location.objects.create(city=city_name)
                car.location = location

        image = request.FILES.get('image')
        if image:
            car.image = image

        car.save()

        return render(request, "edit_car.html", {'car': car, 'alert': True})

    return render(request, "edit_car.html")


@login_required(login_url='/car_dealer_login')
def delete_car(request, myid):
    if not request.user.is_authenticated:
        return redirect("/car_dealer_login")
    car = Car.objects.filter(id = myid)
    car.delete()
    return redirect("/all_cars") 

def customer_homepage(request):
    return render(request, "customer_homepage.html")


@login_required(login_url='/customer_login')
def search_results(request): #Gets city input from the customer, finds cars available in that city
    city = request.POST.get('city')
    if city is not None:
        city = city.lower()
    vehicles_list = []
    location = Location.objects.filter(city = city)
    for a in location:
        cars = Car.objects.filter(location=a)
        for car in cars:
            if car.is_available == True:
                vehicle_dictionary = {'name':car.name, 'id':car.id, 'image':car.image.url, 'city':car.location.city,'capacity':car.capacity}
                vehicles_list.append(vehicle_dictionary)
    request.session['vehicles_list'] = vehicles_list
    return render(request, "search_results.html")

def car_rent(request): #Fetches the selected car and shows its rental page with cost-per-day.
    id = request.POST.get('id')
    car = Car.objects.get(id=id)
    cost_per_day = int(car.rent)
    return render(request, 'car_rent.html', {'car':car, 'cost_per_day':cost_per_day})

@login_required(login_url='/customer_login') 
def order_details(request):
    car_id = request.POST.get('id')
    user = request.user
    days = request.POST.get('days')
    car = Car.objects.get(id=car_id)
    if car.is_available:
        car_dealer = car.car_dealer
        rent = (int(car.rent))*(int(days))
        car_dealer.earnings += rent
        car_dealer.save()
        try:
            order = Order(car=car, car_dealer=car_dealer, user=user, rent=rent, days=days)
            order.save()
        except:
            order = Order.objects.get(car=car, car_dealer=car_dealer, user=user, rent=rent, days=days)
        car.is_available = False
        car.save()
        return render(request, "order_details.html", {'order':order})
    return render(request, "order_details.html")


@login_required(login_url='/customer_login')
def past_orders(request):
    all_orders = []
    user = User.objects.get(username=request.user)
    try:
        orders = Order.objects.filter(user=user)
    except:
        orders = None
    if orders is not None:
        for order in orders:
            if order.is_complete == False:
                order_dictionary = {'id':order.id, 'rent':order.rent, 'car':order.car, 'days':order.days, 'car_dealer':order.car_dealer}
                all_orders.append(order_dictionary)
    return render(request, "past_orders.html", {'all_orders':all_orders})

@login_required(login_url='/customer_login')
def delete_order(request, myid):
    order = Order.objects.filter(id=myid)
    order.delete()
    return redirect("/past_orders")


@login_required(login_url='/car_dealer_login')
def all_orders(request):
    username = request.user
    user = User.objects.get(username = username)
    car_dealer = CarDealer.objects.get(car_dealer=user)
    orders = Order.objects.filter(car_dealer=car_dealer)
    all_orders = []
    for order in orders:
        if order.is_complete == False:
            all_orders.append(order)
    return render(request, "all_orders.html", {'all_orders':all_orders})


@login_required(login_url='/car_dealer_login')
def complete_order(request):
    order_id = request.POST.get('id')
    order = Order.objects.get(id=order_id)
    car = order.car
    order.is_complete = True
    order.save()
    car.is_available = True
    car.save()
    return HttpResponseRedirect('/all_orders/') 


@login_required(login_url='/car_dealer_login')
def earnings(request):
    username = request.user
    user = User.objects.get(username=username)
    car_dealer = CarDealer.objects.get(car_dealer=user)
    orders = Order.objects.filter(car_dealer=car_dealer)
    all_orders = []
    for order in orders:
        all_orders.append(order)
    return render(request, "earnings.html", {'amount':car_dealer.earnings, 'all_orders':all_orders}) 

# Create your views here.
