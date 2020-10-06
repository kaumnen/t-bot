import requests


class Cats:
    def __init__(self):
        self.r = requests.request('GET', 'https://cataas.com/c')
        self.r_gif = requests.request('GET', 'https://cataas.com/c/gif')

    def cat_url(self):
        if self.r.status_code == 200:
            return self.r.url
        else:
            return 'Meow! I\'m having hard time communicating with cat server. Please try later!'


    def cat_gif_url(self):
        if self.r_gif.status_code == 200:
            return self.r_gif.url
        else:
            return 'Meow! I\'m having hard time communicating with cat server. Please try later!'
