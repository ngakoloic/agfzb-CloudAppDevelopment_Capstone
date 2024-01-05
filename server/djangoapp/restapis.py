import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


# Create a `get_request` to make HTTP GET requests
def get_request(url, **kwargs):
    # print(kwargs)
    # print("GET from {} ".format(url))
    try:
        api_key = kwargs["api_key"]
    except:
        api_key = '' 
    if api_key:
        # Basic authentication GET
        params = dict()
        params["text"] = kwargs["text"]
        params["version"] = kwargs["version"]
        params["features"] = kwargs["features"]
        params["return_analyzed_text"] = kwargs["return_analyzed_text"]
        try:
            authenticator = IAMAuthenticator(api_key)
            natural_language_understanding = NaturalLanguageUnderstandingV1(
                version='2022-04-07',
                authenticator=authenticator
            )

            natural_language_understanding.set_service_url(url)
            response = natural_language_understanding.analyze(
                text=params["text"],
                features=params["features"]).get_result()

            result = response['sentiment']['document']['label']
            # print(response)
            return result
        except:
            # If any error occurs
            # print("Network exception occurred - 1")
            return ''
    else:
        # no authentication GET
        try:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
            status_code = response.status_code
            print("With status {} ".format(status_code))
            json_data = json.loads(response.text)
            return json_data
        except:
            # If any error occurs
            print("Network exception occurred")

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    pass

# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_by_id(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result
        # For each dealer object
        for review in reviews:
            review_doc = review
            try:
                purchase_date = review_doc["purchase_date"]
            except:
                purchase_date = '' 
            try:
                car_make = review_doc["car_make"]
            except:
                car_make = ''
            try:
                car_model = review_doc["car_model"]
            except:
                car_model = ''
            try:
                car_year = review_doc["car_year"]
            except:
                car_year = ''

            # Get its content in `doc` object
            review_doc = review
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(dealership=review_doc["dealership"], name=review_doc["name"], purchase=review_doc["purchase"],
                                   review=review_doc["review"], purchase_date=purchase_date, car_make=car_make,
                                   car_model=car_model,
                                   car_year=car_year, sentiment="", id=review_doc["id"])
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    url = 'https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/b4d65755-f3ab-4ee6-a008-a8808e30f2ce'
    api_key = 'aeWW9f628BqAEOhveui76WYseHDiL3TEo9rxjvX8Wynz'
    features=Features(sentiment=SentimentOptions())
    sentiment_result = get_request(url, api_key=api_key, text=text, version='2022-08-10', features=features, return_analyzed_text=True)
    return sentiment_result
