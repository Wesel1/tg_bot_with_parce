import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup as bs



async def take_data(volume: int, chapter: int, number: int = 7413, name: str = "release-that-witch-novel") -> str:
    url = f"https://ranobelib.me/ru/{number}--{name}/read/v{volume}/c{chapter}"
    # https://ranobelib.me/ru/262500--megami-isekai-tensei-nani-ni-naritai-desu-ka-ore-yusha-no-rokkotsu-de/read/v1/c0
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


async def main_data_proc_par(volume: int, chapter: int) -> str:
    html = await take_data(volume, chapter)
    print(data_processing(html))
    return data_processing(html)


if __name__ == '__main__':
    asyncio.run(main_data_proc_par(1, 1000))




# https://ranobelib.me/ru/20818--lord-of-the-mysteries/read/v2/c311?bid=18695
# https://ranobelib.me/ru/book/20818--lord-of-the-mysteries?section=chapters