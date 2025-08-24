import json
import logging
from asyncio import TaskGroup, Task, sleep
from pathlib import Path

from hh_parser.api import HHApiClient

logger = logging.getLogger(__name__)


class HHParser:
    def __init__(self, api_client: HHApiClient):
        self.api_client = api_client

    async def parse(self, text: str, per_page: int = 100, result_file: Path = Path("vacancies.json")) -> None:
        response: dict = await self.api_client.vacancies(text=text, per_page=per_page)
        if response:
            total_pages = response.get('pages')
        else:
            logger.warning('Не смог получить первую страницу')
            return

        tasks: list[Task] = []
        async with TaskGroup() as tg:
            for i in range(1, total_pages + 1):
                task = tg.create_task(self.api_client.vacancies(text=text, page=i, per_page=per_page))
                tasks.append(task)
                await sleep(0.1)

        total_result_pages = 0
        vacancies_data = []
        for t in tasks:
            if t.result():
                total_result_pages += 1
                vacancies_data.extend(t.result().get('items', []))

        result_file.write_text(json.dumps(vacancies_data, ensure_ascii=False, indent=4), encoding="utf-8")
        logger.info("В итоговый файл записаны данные с %s страниц, всего %s вакансий",
                    total_result_pages,
                    len(vacancies_data))