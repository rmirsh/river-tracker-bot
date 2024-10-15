import logging
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any

import httpx
from fake_useragent import UserAgent

from config import settings


@dataclass(slots=True, frozen=True)
class RiverData:
    current_river_level: float
    prevention_level: float
    danger_level: float
    date: date
    time: str


class RiverDataParser:

    def __init__(self):
        self.logger = self._setup_logger()
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

    async def fetch_river_data(self, town: str) -> RiverData:
        if town not in self.town_mapper:
            raise ValueError(f"Город {town} не найден.")
        data = await self._fetch_data()
        town_data = self._format_town_data(data, town)
        parsed_data = self._parse_town_data(town_data)
        return parsed_data

    def _setup_logger(self) -> logging.Logger:
        """Настраивает и возвращает логгер для текущего объекта."""
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)

        # Добавление обработчика в логгер
        if not logger.hasHandlers():
            logger.addHandler(console_handler)

        return logger

    @staticmethod
    def _parse_town_data(town_data: dict[str, Any]) -> RiverData:
        river_level = town_data["data"]["river_level"]
        return RiverData(
            current_river_level=round(river_level["level"]["bs"], 3),
            prevention_level=river_level["prevention"]["bs"],
            danger_level=river_level["danger"]["bs"],
            date=datetime.strptime(river_level["time"], "%d.%m.%Y").date(),
            time=datetime.strptime(river_level["time"], "%H:%M").strftime("%H:%M"),
        )

    def _format_town_data(self, data: dict, town: str) -> dict[str, Any]:
        features = data["features"]
        for feature in features:
            if feature["properties"]["name"] == self.town_mapper[town]:
                town_data = feature["properties"]

                return town_data
        raise ValueError(f"Данные для города {town} не найдены.")

    async def _fetch_data(self) -> dict[str, Any]:
        timeout = httpx.Timeout(timeout=settings.parser.timeout)
        async with httpx.AsyncClient(timeout=timeout) as client:
            self.logger.debug("Начало запроса к серверу")
            try:
                response = await client.get(self.url, headers=self.headers)
                self.logger.debug("Запрос выполнен, проверка статуса ответа")
                response.raise_for_status()
                self.logger.debug("Ответ успешно получен")
                return response.json()
            except (httpx.HTTPStatusError, httpx.RequestError) as e:
                self.logger.error(f"Ошибка HTTP-запроса: {e}")
                raise RuntimeError(f"Ошибка при получении данных: {e}")
            except Exception as e:
                self.logger.error(f"Непредвиденная ошибка: {e}")
                raise RuntimeError(f"Непредвиденная ошибка: {e}")


river_parser = RiverDataParser()
