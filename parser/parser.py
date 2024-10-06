from dataclasses import dataclass
from typing import Any

import aiohttp
from fake_useragent import UserAgent


@dataclass(slots=True, frozen=True)
class RiverData:
    current_river_level: float
    prevention_level: float
    danger_level: float
    time: str


class RiverDataParser:

    def __init__(self):
        self.random_agent = UserAgent().random
        self.url = "http://emercit.com/map/overall.php"
        self.headers = {
            "Accept": "*/*",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Referer": "http://emercit.com/map/",
            "User-Agent": self.random_agent,
            "X-Requested-With": "XMLHttpRequest",
        }
        self.town_mapper: dict[str, str] = {
            "Горячий Ключ": "АГК-0088",
            "Пятигорская": "ЭМЕРСИТ-0007Д",
        }

    async def get_river_data(self, town: str) -> RiverData:
        if town not in self.town_mapper:
            raise ValueError(f"Город {town} не найден.")
        data = await self._get_data()
        town_data = self._format_town_data(data, town)
        parsed_data = self._parse_town_data(town_data)
        return parsed_data

    @staticmethod
    def _parse_town_data(town_data: dict[str, Any]) -> RiverData:
        river_level = town_data["data"]["river_level"]
        return RiverData(
            current_river_level=round(river_level["level"]["bs"], 3),
            prevention_level=river_level["prevention"]["bs"],
            danger_level=river_level["danger"]["bs"],
            time=river_level["time"],
        )

    def _format_town_data(self, data: dict, town: str) -> dict[str, Any]:
        features = data["features"]
        for feature in features:
            if feature["properties"]["name"] == self.town_mapper[town]:
                town_data = feature["properties"]

                return town_data
        raise ValueError(f"Данные для города {town} не найдены.")

    async def _get_data(self) -> dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            try:
                response = await session.get(self.url, headers=self.headers)
                response.raise_for_status()
                return await response.json()
            except (
                aiohttp.ClientResponseError,
                aiohttp.ClientConnectionError,
                aiohttp.InvalidURL,
            ) as e:
                raise RuntimeError(f"Ошибка при получении данных: {e}")


river_parser = RiverDataParser()
