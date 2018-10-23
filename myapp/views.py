from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'index.html')

def new_user(request):
    print("PRINTING POST DATA: ", request.POST)

    #<<--------VALIDATIONS-------->>
    errors = User.objects.basic_validator(request.POST)


    if len(errors):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)

        print(errors)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        hash_brown = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(username = request.POST['username'], name = request.POST['name'], dob=request.POST['dob'], password = hash_brown.decode('utf-8'))

        #store user id in session
        request.session['id'] = user.id
        request.session['username']=user.username

        return redirect('/user_dash')


def user_dash(request):

    if request.session._session:
        all_trips=Trip.objects.all()
        user_trips=Mytrip.objects.filter(user_id=request.session['id'])

        for i in user_trips:
            all_trips = all_trips.exclude(id=i.trip_id)

        context={
            'all_trips' : all_trips,
            'user_trips': user_trips,
        }
        return render(request, 'user_dash.html', context)
    else:
        return redirect("/")


def login(request):
    print("LOGIN REQUEST EXECUTED")
    print(request.POST)

    errors = User.objects.login_validator(request.POST)
    print(errors)


    if len(errors):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)

        print(errors)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        user = User.objects.get(username = request.POST['username'])
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            print("password match")
            request.session['id'] = user.id
            request.session['username'] = user.username
            return redirect('/user_dash')
        else:

            print("failed password")
            messages.error(request, "Wrong password")



            return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')


def create_trip(request):
    if request.session._session:
        return render(request, "create_trip.html")
    else:
        return redirect("/")

def make_trip(request):
    if request.session._session:
        print(request.POST)

        errors = Trip.objects.trip_validator(request.POST)
        print(errors)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)


            print (errors)
            return redirect ('/create_trip')

        else:
            Trip.objects.create(destination = request.POST['destination'], startdate = request.POST['startdate'], enddate = request.POST['enddate'], tripname = request.POST['tripname'], added_by_id = request.session['id'])
            return redirect('/user_dash')
    else:
        return redirect("/")

def mytrips (request, trip_id):
    Mytrip.objects.create(trip_id=movie_id, user_id=request.session['id'])
    
    return redirect('/user_dash')


def join(request, trip_id):
    if request.session._session:
        Mytrip.objects.create(trip_id = trip_id, user_id = request.session['id'])
        return redirect('/user_dash')
    else:
         return redirect ("/")

def show (request, trip_id):
    if request.session._session:
        trip = Trip.objects.get(id=trip_id)
        user_mytrips = Mytrip.objects.filter(trip_id = trip.id)
        context = {
            'trip': trip,
            'user_mytrips': user_mytrips
        }
        return render(request, 'show.html', context)
    else:
        return redirect ("/")


# Create your views here.
