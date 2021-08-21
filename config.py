from dotenv import dotenv_values

__config = dotenv_values(".env")

api_id = __config['API_ID']
api_hash = __config['API_HASH']

assert map(lambda x: x is not None and len(x) > 0, [api_id, api_hash])
