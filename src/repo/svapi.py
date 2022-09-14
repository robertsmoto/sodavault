from typing import Generator
import json
import os
import requests


class SVApiRequest:
    def __init__(self, qstr: str):
        self.qstr = qstr
        self.url = os.getenv('SVAPI_URL', '')
        self.header = {
                'Aid': os.getenv('SVAPI_AID', ''),
                'Auth': os.getenv('SVAPI_AUTH', ''),
                'Prefix': os.getenv('SVAPI_PREF', ''),
                'Content-Type': 'application/json'
                }
        self.data = {}

    def delete(self):
        print("not implemented")

    def query(self):
        url = os.path.join(self.url, 'query')
        r = requests.post(
            url=url,
            headers=self.header,
            json={"query": self.qstr})
        self.data = r.json()
        return self

    def upset(self):
        print("not implemented")

    def decode_base(self, key: str) -> Generator:
        base = self.data.get('data', {}).get(key, {}).get('edges', [])
        length = len(base) - 1
        counter = 0
        while counter <= length:
            node = base[counter].get('node', {})
            node['document'] = json.loads(node['document'])
            counter += 1
            yield node

    def decode_connection(self, key: str) -> Generator:
        print("## not implemented", key)
        yield key
