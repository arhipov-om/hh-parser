# HH Parser

HH Parser — это простой асинхронный парсер вакансий с платформы [HeadHunter](https://hh.ru), написанный на Python. Проект позволяет получать вакансии по ключевым словам и сохранять результаты в JSON-файл.

## Архитектура и принципы

Проект построен с учётом принципов **SOLID**, насколько это целесообразно для небольшого PET-проекта:

* **SRP (Single Responsibility)** — каждый класс имеет в основном одну ответственность: `HHApiClient` — работа с API, `HHParser` — обработка и сбор данных, `__main__.py` — CLI и запуск.
* **OCP (Open/Closed)** — классы можно расширять при необходимости, но проект небольшой, поэтому прямого разделения интерфейсов нет.
* **LSP, ISP, DIP** — принципы учитывались по мере необходимости. Например, `HHParser` использует конкретный API-класс, чтобы не усложнять структуру.

Цель — соблюсти баланс между чистой архитектурой и простотой использования, без излишней «фанатичной» строгости.

## Особенности

* Асинхронное получение данных с API HeadHunter через `httpx`.
* Автоматические повторные попытки запроса при ошибках.
* Поддержка пагинации для загрузки всех страниц результатов.
* Сохранение данных в локальный JSON-файл.

## Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/arhipov-om/hh-parser.git
cd hh-parser
```

2. Установите зависимости через pip:

```bash
python -m pip install .
```

> Проект требует Python >= 3.11.

## Использование

### Через командную строку

Запуск парсера по ключевому слову (по умолчанию — `Python`):

```bash
python -m hh_parser --query "FastApi"
```

Результаты сохраняются в файл `vacancies.json` в текущей директории.

### Через Python код

```python
import asyncio
from pathlib import Path
from hh_parser.api import HHApiClient
from hh_parser.parser import HHParser


async def main():
    client = HHApiClient()
    parser = HHParser(client)
    await parser.parse("Python", result_file=Path("my_vacancies.json"))


asyncio.run(main())
```

* `api.py` — клиент для работы с API HeadHunter.
* `parser.py` — логика асинхронного парсинга и сохранения вакансий.
* `__main__.py` — точка входа для запуска из командной строки.

## Лицензия

MIT License.
