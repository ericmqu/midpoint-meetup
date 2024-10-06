import  requests
import math
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('GOOGLE_API_KEY')

def get_latlng(address):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            print(f"Error: {data['status']}")
            return None
    else:
        print(f"Error: {response.status_code}")
        return None

def calc_midpoint(coords):
    x = y = z = 0.0
    for lat, lng in coords:
        lat_rad = math.radians(lat)
        lng_rad = math.radians(lng)
        x += math.cos(lat_rad) * math.cos(lng_rad)
        y += math.cos(lat_rad) * math.sin(lng_rad)
        z += math.sin(lat_rad)

    total = len(coords)
    x /= total
    y /= total
    z /= total

    lng_mid = math.atan2(y, x)
    hyp = math.sqrt(x*x + y*y)
    lat_mid = math.atan2(z, hyp)

    return math.degrees(lat_mid), math.degrees(lng_mid)

def find_nearby_places(lat, lng, place_type='restaurant'):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=1500&type={place_type}&key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            places = []
            for place in data['results']:
                places.append({
                    'name': place['name'],
                    'address': place.get('vicinity', 'Address not available')
                })
            return places
        else:
            print(f"Error: {data['status']}")
            return None
    else:
        print(f"Error: {response.status_code}")
        return None

def main():
    addresses = []

    n = int(input("Enter number of places to search: "))
    for i in range(n):
        address = input(f"Enter address {i+1}: ")
        addresses.append(address)

    coords = []
    for address in addresses:
        lat_lng = get_latlng(address)
        if lat_lng:
            coords.append(lat_lng)

    if coords:
        mid_lat, mid_lng = calc_midpoint(coords)
        print(f"Midpoint Latitude: {mid_lat}, Longitude: {mid_lng}")

        places = find_nearby_places(mid_lat, mid_lng)
        if places:
            print("Nearby places:")
            for place in places:
                print(f"{place['name']} - {place['address']}")
        else:
            print("No nearby places found.")
    else:
        print("Could not geocode the addresses.")

if __name__ == "__main__":
    main()