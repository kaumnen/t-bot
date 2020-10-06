import requests
import urllib.parse


def short_url(url):
    r = requests.post('https://goolnk.com/api/v1/shorten', {'url': 'https://' + urllib.parse.quote(url)})
    if r.status_code == 200:
        return r.json()['result_url']
    else:
        return ''
