# T-bot

T-bot is Telegram bot utilizing a few API's. Operating 24/7, find it [here.](https://t.me/awsmm_bot) 

Built using [python-telegram-bot.](https://github.com/python-telegram-bot/python-telegram-bot)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required modules.

```bash
pip3 install -r requirements.txt
```

## DEV Usage

Every file that needs secret key uses configparser. 

If you want to test it with your own ones, make .ini file in folder where main.py file is, should look like this:

```
[TELEGRAM_API]
api_key=[your_api_key_here]

[NASA_API]
api_key=[your_api_key_here]

[CATS_API]
api_key=[your_api_key_here]

```

**Make sure to write keys without quotes!**

## API's used
[URL Shortener](https://goolnk.com/)

[NASA API](https://api.nasa.gov/)

[Quotes API](http://quotable.io/)

[Cats API](https://thecatapi.com/)

[Dogs API](https://random.dog/)


## License
[MIT](https://choosealicense.com/licenses/mit/)
