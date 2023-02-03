from monoflow.utils import Account

# obtain from https://api.monobank.ua/
MONOBANK_API_TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
MONOBANK_API_FETCH_TIMEOUT = 60
EXPORT_FILE_NAME = "monobank.csv"

# this is used for scraping the extract from Monobank
# to obtain account IDs, see this Monobank endpoint:
# https://api.monobank.ua/docs/#tag/Kliyentski-personalni-dani/paths/~1personal~1client-info/get
accounts = [
    Account(
        id="xxxxxxxxxxxxxxxxxxxxxx",  # monobank account ID
        name="UAH Card",  # the name in the Money Flow app
        currency="UAH",  # currency name
    ),
    Account(
        id="xxxxxxxxxxxxxxxxxxxxxx",  # monobank account ID
        name="USD PE Card",  # the name in the Money Flow app
        currency="USD",  # currency name
    ),
]
