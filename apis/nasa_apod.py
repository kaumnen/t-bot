# Import required libraries:
import nasapy
from datetime import datetime
from configparser import ConfigParser

# read .ini file
config_object = ConfigParser()
config_object.read(".ini")

# get the data
nasa_api = config_object["NASA_API"]
api_key = nasa_api["api_key"]


class Nasa_apod:
    def __init__(self):
        # Initialize Nasa class by creating an object:

        k = api_key
        nasa = nasapy.Nasa(key=k)

        # Get today's date in YYYY-MM-DD format:

        d = datetime.today().strftime('%Y-%m-%d')

        # Get the image data:

        self.apod = nasa.picture_of_the_day(date=d, hd=True)

    def retrieve_picture_url(self):
        return self.apod["hdurl"]

    def retrieve_picture_info(self):
        pic_info = ''
        if "copyright" in self.apod.keys():
            pic_info += f'This image is owned by: \n{self.apod["copyright"]}.\n'
        if "title" in self.apod.keys():
            pic_info += f'\nTitle of the image: \n{self.apod["title"]}.\n'
        if "date" in self.apod.keys():
            pic_info += f'\nDate image released: \n{self.apod["date"]}'
        return pic_info

    def retrieve_text_with_picture(self):
        return f'Description of the image:\n\n{self.apod["explanation"]}' if self.apod["explanation"] else ''
