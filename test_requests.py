import requests

city = "Irkutsk"
API_KEY = "ba5c6ff4a3f74710ecb24b81cf5f915a"

params = {
    "q": city,
    "appid": API_KEY
}

response = requests.get(f"https://api.openweathermap.org/geo/1.0/direct", params=params)
lon = response.json()[0]["lon"]
lat = response.json()[0]["lat"]

params = {
    "lat": lat,
    "lon": lon,
    "appid": API_KEY,
    "lang": "RU"
}

response = requests.get(f"https://api.openweathermap.org/data/2.5/weather", params=params)

temp = response.json()["main"]["temp"] - 273.15
weather = response.json()["weather"][0]["description"]

print(temp)
print(weather)