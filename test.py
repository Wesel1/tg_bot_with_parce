# a = 'https://ranobelib.me/ru/262500--megami-isekai-tensei-nani-ni-naritai-desu-ka-ore-yusha-no-rokkotsu-de/read/v1/c0'
# c = 'https://ranobelib.me/ru/262500--megami-isekai-tensei-nani-ni-naritai-desu-ka-ore-yusha-no-rokkotsu-de/read/v1/c100'
# b = a.split('/read/')[0]
# volume = 1
# chapter = 100
# s = f"v{volume}/c{chapter}"
#
# # print(''.join([b[0],'/read/', s]))
# print(b)
# import requests
#
# headers = {
#     'Content-Type': 'application/json',
#     'Accept': '*/*',
#     'Sec-Fetch-Site': 'cross-site',
#     'Accept-Language': 'ru',
#     'Sec-Fetch-Mode': 'cors',
#     # 'Accept-Encoding': 'gzip, deflate, br, zstd',
#     'Origin': 'https://ranobelib.me',
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.3.1 Safari/605.1.15',
#     'Referer': 'https://ranobelib.me/',
#     'Sec-Fetch-Dest': 'empty',
#     'Priority': 'u=3, i',
#     'Client-Time-Zone': 'Asia/Yekaterinburg',
#     'Site-Id': '3',
# }
#
# params = {
#     'number': '101',
#     'volume': '1',
# }
#
# response = requests.get(
#     'https://api.cdnlibs.org/api/manga/7413--release-that-witch-novel/chapter',
#     params=params,
#     headers=headers,
# )
#
# print(response.text)

from pydantic import BaseModel
from typing import Optional

from app.handlers import build_chapter


class Book(BaseModel):
    id: Optional[int] = None
    pipidastr: str
    hurl: Optional[str] = None
    Vanya: int
    hyi: int
    text: str = None

a = Book.model_validate({'pipidastr': 'Deploy', 'Vanya': 10, 'hyi': 10})

print(*[i[1] for i in [*a]])
print(tuple(a.model_dump().items()))

r = 'cont:qwehd:kljdsf:1209'

print(r.startswith('cont'))




