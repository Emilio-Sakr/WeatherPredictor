import requests
from bs4 import BeautifulSoup
import json


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
    with open('./WeatherPredictorApi/data/cities.json', 'w') as f:
        dict = {'Cities': citiesData}
        json.dump(dict, f)
