def json_to_list(js):
    botones = []
    for i in range(len(js)):
        botones.append(js[i])

    return botones


def parse_float(f):
    return float(str(f).replace(',', '.'))
