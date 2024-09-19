import requests,datetime
from django.shortcuts import render
from django.http import HttpResponse

def get_weather_data(city):
    weather_api_key = 'enter your weather api key'
    google_api_key = 'enter your google api key'
    search_engine_id = 'enter your google search engine ID'
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
    google_url = f"https://www.googleapis.com/customsearch/v1?q={city}+background&key={google_api_key}&cx={search_engine_id}&searchType=image"
    day = datetime.date.today()
    try:
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        image_response = requests.get(google_url)
        image_response.raise_for_status()
        image_data = image_response.json()
        image_url = image_data['items'][0]['link']

        return {
            'city': city,
            'day':day,
            'temperature': weather_data['main']['temp'],
            'description': weather_data['weather'][0]['description'],
            'icon': weather_data['weather'][0]['icon'],
            'background_image': image_url
        }
    except requests.RequestException:
        return None

def home(request):
    city = request.GET.get('city')
    if city:
        data = get_weather_data(city)
        if data:
            return render(request, 'weatherapp/index.html', data)
        else:
            return HttpResponse("<h1 style='text-align:center;'>***Error fetching data, go back and 'ENTER VALID CITY' name***<h1>")
    return render(request, 'weatherapp/index.html')
