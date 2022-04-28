from email.mime import base
import requests
from bs4 import BeautifulSoup
import json

base_path = './WeatherPredictorApi/data'

def scrapCities():
    cities = ''
    BASE_URL='https://open-meteo.com/en/docs#api-documentation'
    resp = requests.get(BASE_URL)
    soup = BeautifulSoup(resp.content, "html.parser")
    citiestags = soup.find_all("select",attrs={"id":"select_city"})
    
    for tag in citiestags:
        cities += tag.text.strip()

    citiesList= cities.split('\n')
    citiesData=list(filter(None, citiesList))
    return citiesData

def citiesToJson(citiesData):
    with open(f'{base_path}/cities.json', 'w') as f:
        dictionary = {'Cities': citiesData}
        json.dump(dictionary, f)

def scrapLocation(city):
    allCitiesJson = json.load(open(f'{base_path}/cities.json'))['Cities']
    if city not in allCitiesJson:
        raise Exception(detail="tried to get an unkown city location")
    try:
        response = requests.get(f'https://geocoding-api.open-meteo.com/v1/search?name={city}').json()
        return response["results"][0]["latitude"], response["results"][0]["longitude"]
    except Exception as e:
        print(f'error in {e}')

def citiesLocationsJson(citiesList):
    locationsList = []
    for city in citiesList:
        locationsList.append(scrapLocation(city))
    assert len(citiesList)==len(locationsList), 'locations do not match their givin cities, error occured'
    with open(f'{base_path}/cities.json', 'w') as f:
        dictionary = dict(zip(citiesList, locationsList))
        json.dump(dictionary, f)


citiesLocationsJson(scrapCities())