import requests


class Dogs:
    def __init__(self):
        self.r = requests.get('https://random.dog/woof.json')

    def dog_url(self):
        if self.r.status_code == 200:
            return self.r.json()['url']
        else:
            return 'Woof! I\'m having hard time communicating with dogo server. Please try later!'
