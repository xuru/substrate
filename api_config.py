from main import on_production_server

VALID_API_KEYS = ['testapikey1', 'testapikey2']
if on_production_server:
    VALID_API_KEYS = ['prodapikey1', 'prodapikey1']

DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100
