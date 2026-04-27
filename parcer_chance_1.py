import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup as bs

from database.database import HelpBase


async def take_data(volume: int, chapter: int, number: int = 7413, name: str = "release-that-witch-novel") -> str:
    url = f"https://ranobelib.me/ru/{number}--{name}/read/v{volume}/c{chapter}"

    async with async_playwright() as p:
        browser = await p.chromium.launch()

        async with await browser.new_context() as context:
            page = await context.new_page()
            response = await page.goto(url)
            await page.wait_for_load_state("networkidle")
            html = await page.content()

        await browser.close()

    return html


def data_processing(html: str) -> str:
    soup = bs(html, "lxml")

    label = soup.find('h1').get_text()
    text = soup.find_all("p")

    result = label + '\n'

    for i in text:
        line = bs.get_text(i)
        result += line + '\n'

    return result


async def save_data(status: str, result: str) -> None:
    database = HelpBase('help.db')
    database.save(status, result)

async def main_data_proc_par(volume: int, chapter: int) -> None:
    html = await take_data(volume, chapter)

    result = data_processing(html)

    await save_data("parce_done", result)


if __name__ == '__main__':
    asyncio.run(main_data_proc_par(1, 10))
    database = HelpBase('help.db')
    print(database.find("parce_done"))




# https://ranobelib.me/ru/20818--lord-of-the-mysteries/read/v2/c311?bid=18695
# https://ranobelib.me/ru/book/20818--lord-of-the-mysteries?section=chapters