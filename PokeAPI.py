import requests

name = "pikachu"
url = f"https://pokeapi.co/api/v2/pokemon/{name}"

response = requests.get(url)

data = response.json()
    
print("Name:", data["name"])
print("Number:", data["id"])
print("Weight:", data["weight"] / 10, "kg")
print("Height:", data["height"] / 10, "m")
    
print("\nTypes:")
for t in data["types"]:
    print("-", t["type"]["name"])
    
print("\nAbilities:")
for a in data["abilities"]:
    print("-", a["ability"]["name"])
