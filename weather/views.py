from django.shortcuts import render
from .forms import CityForm
from .models import City
import requests

def index(request):
	url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=332954e273e15150dd810502b150803d"
	cities = City.objects.all()
	if request.method == 'POST':
		form = CityForm(data=request.POST)
		form.save()
	weather_data = []
	for city in cities:
		city_weather = requests.get(url.format(city)).json() #Request API data/ convert to python
		weather = {
			'city': city,
			'temperature': city_weather['main']['temp'],
			'description': city_weather['weather'][0]['description'],
			'icon': city_weather['weather'][0]['icon']}

		weather_data.append(weather)

	form = CityForm()
	context = {'weather_data':weather_data, 'form':form}
	return render(request, 'weather/index.html', context)
