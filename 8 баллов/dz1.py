import requests
import re

HREF = re.compile('<a href=[\'\"](/.*)[\'\"]')
URL = re.compile('<code>(/.*)</code>')
KEY = re.compile('Секретный ключ: <b><code>(.*)</code></b>')
DATE = re.compile('<code>(.*)</code>')
STEP = re.compile(r"(Шаг .*?) ")


class Request:
    def __init__(self, url, type, parametrs):
        self.type = type
        self.url = url
        self.parametrs = parametrs


def parse(request, url):
    type = parse_type(request.text)
    new_url = url + parse_url(request.text)
    request_parametrs=parse_tables(request)
    return Request(new_url, type, request_parametrs)


def parse_type(s):
    if "GET" in s or "<a href=" in s:
        return "GET"
    elif "POST" in s or "Загрузите файлы" in s:
        return "POST"
    return ""


def parse_url(text):
    if "<a href=" in text:
        return HREF.search(text).group(1)
    return URL.search(text).group(1)


def parse_tables(request):
    request_parametrs = {}
    request_parametrs['cookies'] = {}
    text = request.text
    start = text.find('<br />')
    if start == -1:
        start = text.find('<table border=\"1\">')
    while True:
        if '</table>' in text[start:]:
            end = text[start:].index('</table>')
        else:
            break
        current = text[start:end + start + 8]
        if "параметры" in current:
            request_parametrs['params'] = parse_table(current)
        elif "cookie" in current:
            request_parametrs['cookies'] = parse_table(current)
        elif "заголовки" in current:
            request_parametrs['headers'] = parse_table(current)
        elif "данные формы" in current:
            request_parametrs['data'] = parse_table(current)
        elif "файл" in current:
            request_parametrs['files'] = parse_table(current)
        start = end + start + 8
    request_parametrs['cookies']['user'] = '67508b925f71c6ad39915b77db7946fa'
    return request_parametrs

def parse_table(text):
    result = {}
    data = DATE.findall(text)
    for i in range(len(data) // 2):
        result[data[2 * i]] = data[2 * i + 1]
    return result


def main():
    url = 'http://178.62.232.110'
    cookies = {"user": '67508b925f71c6ad39915b77db7946fa'}
    request = requests.get(url, cookies=cookies)
    while 'Секретный ключ:' not in request.text:
        request_data = parse(request, url)
        if request_data.type == "GET":
            request = requests.get(request_data.url, **request_data.parametrs)
        if request_data.type == "POST":
            request = requests.post(request_data.url, **request_data.parametrs)
    print(KEY.findall(request.text)[0])


if __name__ == '__main__':
    main()
