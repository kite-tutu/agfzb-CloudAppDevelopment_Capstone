import requests
import json
from .models import CarDealer,DealerReview
from requests.auth import HTTPBasicAuth

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs,auth=HTTPBasicAuth('apikey', "Cl0KYPEyjLVRHrKezpg6zLOg0cQ0Bjiaarw3XKxMPp-b"))
        #print(response.content)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        #print(json_result)
        # Get the row list in JSON as dealers
        dealers = json_result[0:]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            #dealer_doc = dealer["doc"]
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        print(json_result)
        # Get the row list in JSON as dealers
        dealer_reviews = json_result[0:]
        # For each dealer object
        for dealer_review in  dealer_reviews:
            # Get its content in `doc` object
            #dealer_doc = dealer["doc"]
            review_doc = dealer_review
            # Create a CarDealer object with values in `doc` object

            review_obj = DealerReview(dealership=review_doc["dealership"], name=review_doc["name"],purchase=review_doc["purchase"], review=review_doc["review"], purchase_date=review_doc["purchase_date"],car_make=review_doc["car_make"], car_model=review_doc["car_model"],car_year=review_doc["car_year"],id=review_doc["id"])
            results.append(review_obj)

            

    return results

def get_dealer_by_id_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,dealerId=dealerId)
    if json_result:
        print(json_result)
        # Get the row list in JSON as dealers
        reviews = json_result[0:]
        review_docs = reviews
        for doc in review_docs:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = DealerReview(car_make=doc["car_make"], car_model=doc["car_model"], car_year=doc["car_year"],
                                    dealership=doc["dealership"], id=doc["id"], name=doc["name"],
                                    purchase=doc["purchase"],
                                    purchase_date=doc["purchase_date"], review=doc["review"])
            results.append(dealer_obj)
            #json_data = json.loads(results)
        return results
    

def get_dealer_by_state_from_cf(url, stateval):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,stateval=stateval)
    if json_result:
        #print(json_result)
        # Get the row list in JSON as dealers
        dealers = json_result[0:]
        
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            #dealer_doc = dealer["doc"]
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return dealers

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
