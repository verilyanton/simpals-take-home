import json
import os

from tornado import httpclient


class SimpalsAccountApi:

    def __init__(self):
        self.auth_username = os.environ['AUTH_USERNAME']

    async def fetch_all_ads(self):
        http_client = httpclient.AsyncHTTPClient()
        try:
            response = await http_client.fetch(
                httpclient.HTTPRequest(
                    'https://partners-api.999.md/adverts',
                    auth_username=self.auth_username
                )
            )
        except httpclient.HTTPError as e:
            return {'error': str(e)}
        except Exception as e:
            return {'error': str(e)}
        else:
            return {'ads': json.loads(response.body)['adverts']}
