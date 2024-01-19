import requests
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class RiverData:
    current_river_level: float
    prevention_level: float
    danger_level: float 


def main():
    data = get_data("http://emercit.com/map/overall.php")
    town_data = get_town_data(data)
    parsed_data = parse_town_data(town_data) 
    return parsed_data


def parse_town_data(town_data) -> RiverData:
    river_level = town_data["data"]["river_level"]
    return RiverData(
            current_river_level=round(river_level["level"]["bs"], 3),
            prevention_level=river_level["prevention"]["bs"],
            danger_level=river_level["danger"]["bs"]
            )


def get_town_data(data: dict) -> dict[str, float] | None:
    features = data["features"]
    for feature in features:
        if feature["properties"]["name"] == "АГК-0088":
            town_data = feature["properties"]
    
            return town_data


def get_data(url: str) -> dict[str, float | None]:

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Referer': 'http://emercit.com/map/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        }

    params = {
        'time': '1705590664',
        }

    response = requests.get(url, params=params, headers=headers, verify=False).json()

    return response 
        
if __name__=="__main__":
    print(main())
