from typing import Dict

import requests
import folium


def get_ip_address() -> str:
    flag = True
    ip_address = ""
    while flag:
        flag = False
        ip_address = input("Enter ip address: ")
        octets = ip_address.split(".")
        if len(octets) == 4:
            for number in octets:
                if not number.isdigit():
                    flag = True
                else:
                    if not (0 < int(number) < 256):
                        flag = True
        else:
            flag = True
        if flag:
            print("IP address is invalid.")
    return ip_address


def get_data(ip_address: str) -> Dict[str, str]:
    response = requests.get(f"https://ipinfo.io/{ip}/json")
    return response.json()


def extract_location(data: Dict[str, str]) -> (float, float):
    location = data["loc"].split(",")
    return float(location[0]), float(location[1])  # latitude and longitude


def create_map(lat: float, long: float):
    user_map = folium.Map(location=[lat, long], zoom_start=12)
    folium.Marker([lat, long], popup="User Location").add_to(user_map)
    return user_map


# MAIN STARTS HERE
ip = get_ip_address()
data = get_data(ip)

latitude, longitude = extract_location(data)

user_map = create_map(latitude, longitude)

user_map.save(f"user_location_{data["country"]}_{data["city"]}.html")
