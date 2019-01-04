import re

with open('raw/game_raw.txt', 'r', encoding='utf-8') as f:
    data = []
    for line in f.readlines():
        if line[0].isdigit():
            head, tail = line.split(' ')
            head = re.sub('[^0-9]', '', head) + '.'
            tail = re.sub(';', '', tail)
            tail = re.findall('([AaBb]{1}[0-9]{1}[<>]{1}[*+#]?\*?)', tail)
            data.append([head] + tail)
        else:
            data.append([line])

header = ['[Event ""]',
          '[Site ""]',
          '[Date ""]',
          '[Round ""]',
          '[South ""]',
          '[North ""]',
          '[Result ""]']

data = header + [''] + data

with open('data/game2.pgn', 'w', encoding='utf-8') as f:
    for i in data:
        if isinstance(i, str):
           f.write(i)
        else:
            f.write(' '.join(i))
        f.write('\n')

