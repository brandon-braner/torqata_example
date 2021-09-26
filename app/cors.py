from typing import List


def get_cors_domains(env: str) -> List:
    '''Return a list of domains we accept for cors'''
    if env == 'local':
        return [
            'http://localhost:3000',
            'http://localhost:8000',
            'http://app.released.local',
            'http://api.released.local'
        ]
