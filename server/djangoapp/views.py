from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({
                    "userName": username,
                    "status": "Authenticated"
                })
            else:
                return JsonResponse({
                    "error": "Invalid credentials"
                }, status=401)
        except json.JSONDecodeError:
            return JsonResponse({
                "error": "Invalid JSON"
            }, status=400)
    return JsonResponse({
        "error": "POST method required"
    }, status=405)


def logout_request(request):
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def registration(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data['userName']
            password = data['password']
            first_name = data['firstName']
            last_name = data['lastName']
            email = data['email']

            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    "userName": username,
                    "error": "Already Registered"
                })

            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
                email=email
            )
            login(request, user)
            return JsonResponse({
                "userName": username,
                "status": "Authenticated"
            })
        except json.JSONDecodeError:
            return JsonResponse({
                "error": "Invalid JSON"
            }, status=400)
    return JsonResponse({
        "error": "POST method required"
    }, status=405)


def get_cars(request):
    count = CarMake.objects.filter().count()
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = [
        {"CarModel": car_model.name, "CarMake": car_model.car_make.name}
        for car_model in car_models
    ]
    return JsonResponse({"CarModels": cars})


def get_dealerships(request, state="All"):
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({
        "status": 200,
        "dealers": dealerships
    })


def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({
            "status": 200,
            "reviews": reviews
        })
    return JsonResponse({
        "status": 400,
        "message": "Bad Request"
    })


def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({
            "status": 200,
            "dealer": dealership
        })
    return JsonResponse({
        "status": 400,
        "message": "Bad Request"
    })


def add_review(request):
    if not request.user.is_anonymous:
        data = json.loads(request.body)
        try:
            post_review(data)
            return JsonResponse({"status": 200})
        except Exception:
            return JsonResponse({
                "status": 401,
                "message": "Error in posting review"
            })
    return JsonResponse({
        "status": 403,
        "message": "Unauthorized"
    })
