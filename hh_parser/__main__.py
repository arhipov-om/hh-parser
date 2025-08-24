import asyncio
import argparse
import logging

from hh_parser.api import HHApiClient
from hh_parser.parser import HHParser

logging.basicConfig(level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)


async def main(parse_query: str):
    parser = HHParser(HHApiClient())
    await parser.parse(parse_query)

def run():
    arg_parser = argparse.ArgumentParser(description="HH парсер")
    arg_parser.add_argument(
        "--query",
        type=str,
        help="Строка запроса для поиска вакансий",
        required=False,
        default='Python'
    )
    args = arg_parser.parse_args()
    asyncio.run(main(args.query))

if __name__ == '__main__':
    run()
