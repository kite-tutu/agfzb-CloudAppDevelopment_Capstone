from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import DealerReview,CarModel
from .restapis import get_dealers_from_cf,get_dealer_reviews_from_cf,get_dealer_by_state_from_cf,get_dealer_by_id_from_cf,post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    return render(request,"djangoapp/aboutus.html")

# Create a `contact` view to return a static contact page
def contact(request):
    return render(request,"djangoapp/contact.html")

# Create a `login_request` view to handle sign in request
def login_request(request):
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            #return render(request, 'djangoapp/index.html',{'user':user})
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return redirect('djangoapp:index')
    else:
        return render(request, 'djangoapp/index.html')

def logout_request(request):
    # Get the user object based on session id in request
    print("Logging out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
        # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
            # If it is a new user
            if not user_exist:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                password=password)
                # Login the user and redirect to course list page
                login(request, user)
                return redirect("djangoapp:index")
            else:
                return render(request, 'djangoapp/registration.html',context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context={}
        url = "https://kitetutu-3000.theiadocker-3-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        #dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        context["dealers"]=dealerships
        return render(request, 'djangoapp/index.html', context)
        #return HttpResponse(dealer_names)

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, id):
    if request.method == "GET":
        context ={}
        context["dealer_id"] = id
        url = "https://kitetutu-5000.theiadocker-3-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews?id="+str(id)+""
        # Get dealers from the URL
        dealer_reviews = get_dealer_reviews_from_cf(url, id)
        context['reviews']=(dealer_reviews)
        # Concat all dealer's reviews
        #dealer_reviews = ' '.join([dealer.review for dealer in dealerships])
        # Return a list of dealer short name
        #return HttpResponse(dealerships)
        return render(request, 'djangoapp/dealer_details.html', context)

def get_dealer_by_id(request, dealer_id):
    if request.method == "GET":
        url = "https://kitetutu-5000.theiadocker-3-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews?id="+str(dealer_id)+""
        # Get dealers from the URL
        dealerships = get_dealer_by_id_from_cf(url,dealer_id)
        #print(dealerships)
        # Concat all dealer's reviews
        dealer_reviews = ' '.join([dealer.review for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_reviews)

def get_dealers_by_state(request, stateval):
    if request.method == "GET":
        url = "https://kitetutu-3000.theiadocker-3-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get?state="+ stateval +""
        # Get dealers from the URL
        dealerships = get_dealer_by_state_from_cf(url,stateval=stateval)
        # Concat all dealer's reviews
        #dealer_reviews = ' '.join([dealer for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealerships)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.user.is_authenticated:
        if request.method == "GET":
            context = {}
            cars = list(CarModel.objects.filter(dealerid=dealer_id))
            #for car in cars:
               #car.year = car.year.strftime("%Y")
            context["cars"] = cars

            dealer_url = "https://kitetutu-3000.theiadocker-3-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
            dealer = get_dealer_by_id_from_cf(dealer_url, dealer_id)  

            context["dealer"] = dealer
            context["dealer_id"] = dealer_id

            return render(request, "djangoapp/add_review.html", context)

        if request.method == "POST":
            context={}
            user = request.user
            review = {}
            review["id"] = dealer_id
            review["name"] = f"{user.first_name} {user.last_name}"
            review["dealership"] = dealer_id
            review["review"] = request.POST['content']   
            review["purchase"] = False
            checkedVal = request.POST.get('purchasecheck', False)
            if checkedVal == "on":
                checkedVal = True
            review["purchase"] = checkedVal
            review["purchase_date"] = request.POST['purchasedate']
            car_make, car_model, car_year = request.POST['car_details'].split("-")
            review["car_make"] = car_make
            review["car_model"] = car_model
            review["car_year"] = car_year
            url = "https://kitetutu-5000.theiadocker-3-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review"
            json_payload = {}
            json_payload["review"] = review
           
            post_request(url, json_payload, dealerId=dealer_id)
            print("Review submitted.")

            return redirect("djangoapp:dealer_details", id=dealer_id)
            
    else: 
        print("User is not authenticated")
        return redirect("djangoapp:dealer_details", context)
