import os

from dotenv import dotenv_values

__config = {
    **dotenv_values(".env"),
    **os.environ,
}

api_id = __config['API_ID']
api_hash = __config['API_HASH']
is_mock = __config.get('MOCK', 'False').lower() == 'true'

assert map(lambda x: x is not None and len(x) > 0, [api_id, api_hash])
