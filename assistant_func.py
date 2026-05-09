def proc_link(url: str) -> str:
    return url.split('/read/')[0]

if __name__ == '__main__':
    print(proc_link('https://ranobelib.me/ru/262500--megami-isekai-tensei-nani-ni-naritai-desu-ka-ore-yusha-no-rokkotsu-de/read/v1/c0'))