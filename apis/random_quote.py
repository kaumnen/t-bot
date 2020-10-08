import requests

class Quote:
    def __init__(self):
        self.r = requests.request('GET', 'https://api.quotable.io/random')

    def quote_msg(self):
        if self.r.status_code == 200:
            data = self.r.json()
            nl = '\n'
            return f'"{data["content"]}"{nl}- {data["author"]}'

        else:
            return 'I\'m having hard time communicating with quotes all over internet. Please try later!'
