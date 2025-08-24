import asyncio
import logging
from functools import wraps

from httpx import AsyncClient

logger = logging.getLogger(__name__)


def retry(attempts: int):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            count = 0
            while count < attempts:
                count += 1
                result = await func(*args, **kwargs)
                if result:
                    return result
                await asyncio.sleep(0.3)
            return None

        return wrapper

    return decorator


class HHApiClient:
    def __init__(self, base_url: str | None = None) -> None:
        if base_url is None:
            base_url = "https://api.hh.ru"
        self._client = AsyncClient(base_url=base_url)

    @retry(5)
    async def _request(self, **kwargs):
        response = await self._client.request(**kwargs)
        if response.is_error:
            logger.warning("Произошла ошибка: kwargs=%s response=%s", kwargs, response.json())
            return None
        return response

    async def vacancies(self, text: str, page: int = 1, per_page: int = 100) -> dict | None:
        params = {"text": text, "page": page, "per_page": per_page}
        response = await self._request(method='GET', url='/vacancies', params=params)
        if response:
            response = response.json()
            logger.info("Успешно получены вакансии page=%s", page)
        return response
