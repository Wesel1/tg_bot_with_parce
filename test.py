a = 'https://ranobelib.me/ru/262500--megami-isekai-tensei-nani-ni-naritai-desu-ka-ore-yusha-no-rokkotsu-de/read/v1/c0'
c = 'https://ranobelib.me/ru/262500--megami-isekai-tensei-nani-ni-naritai-desu-ka-ore-yusha-no-rokkotsu-de/read/v1/c100'
b = a.split('/read/')
volume = 1
chapter = 100
s = f"v{volume}/c{chapter}"

print(''.join([b[0],'/read/', s]))