from main import *

# start bot
updater.start_polling()

# working until stop signal received (SIGINT)
updater.idle()
