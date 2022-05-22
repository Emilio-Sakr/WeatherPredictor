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
    allCitiesJson = json.load(open(f'{base_path}/cities.json'))
    if city not in allCitiesJson:
        raise Exception(detail="tried to get an unkown city location")
    try:
        response = requests.get(f'https://geocoding-api.open-meteo.com/v1/search?name={city}').json()
        la, lo = response["results"][0]["latitude"], response["results"][0]["longitude"]
        if la and lo != None:
            return la, lo
    except Exception as e:
        print(f'error in {e}')
        return (0, 0)

def citiesLocationsJson(citiesList):  #2 Errors
    locationsList = []
    for city in citiesList:
        data = scrapLocation(city)
        if data == None:
            citiesList.remove(city)
        else:
            locationsList.append(data)
    print(citiesList)
    print(locationsList)
    assert len(citiesList)==len(locationsList), 'locations do not match their givin cities, error occured'
    with open(f'{base_path}/cities.json', 'w') as f:
        dictionary = dict(zip(citiesList, locationsList))
        json.dump(dictionary, f)


citiesLocationsJson(scrapCities())