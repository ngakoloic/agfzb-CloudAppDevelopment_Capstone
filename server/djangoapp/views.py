from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_by_id, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.contrib.auth.decorators import login_required

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def static_page(request):
    context = {}
    if request.method == "GET":
        return render(request, 'static/index.html', context)

# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
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
            return redirect('djangoapp:index')
        else:
            # If not, stay to index page
            return render(request, 'djangoapp:index', context)
    else:
        return render(request, 'djangoapp:index', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # stay to index page
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
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
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp:index', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        #launch get-dealership.js server to get this url
        url = "https://bngako-3000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context['dealership_list'] = dealerships
        # dealerships = get_dealer_by_id(url, dealerId=1)
        # Concat all dealer's short name
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        #launch reviews.py server to get this url
        url = "https://bngako-5000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/review?dealerId="+str(dealer_id)
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(url)
        context['review_list'] = reviews
        context['dealer_id'] = dealer_id
        # Concat all review's
        # dealer_reviews = ' </br> '.join([review.review+' : '+review.sentiment for review in reviews])
        # Return a list of dealer short name
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
@login_required
def add_review(request, dealer_id):
    if request.method == "GET":
        context = {}
        url_1 = "https://bngako-5000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/review?dealerId=all"
        cars = get_dealer_reviews_from_cf(url_1)
        url_2 = "https://bngako-3000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/dealership?id="+str(dealer_id)
        dealership = get_dealers_from_cf(url_2)
        context['dealership'] = dealership[0]
        context['dealer_id'] = dealer_id
        context['cars'] = cars
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == "POST":
        car = request.POST['car'].split('-')
        purchase = request.POST['purchasecheck']
        if purchase == 'on':
            purchase = True
        elif purchase == 'off':
            purchase = False
        review = dict()
        review["id"] = request.POST['id']
        review["name"] = request.POST['name']
        review["dealership"] = dealer_id
        review["review"] = request.POST['content']
        review["purchase"] = purchase
        review["purchase_date"] = request.POST['purchasedate']
        review["car_make"] = car[0]
        review["car_model"] = car[1]
        review["car_year"] = car[2]

        json_payload = dict()
        json_payload["review"] = review

        url = 'https://bngako-5000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/review'

        result = post_request(url, json_payload, dealerId=dealer_id)
        # Return the post review
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
