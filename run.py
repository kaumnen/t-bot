from main import *
updater.start_polling()

# working until stop signal received (SIGINT)
updater.idle()
