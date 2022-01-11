import json
import os

from tornado import httpclient

from app.api.bnm_exchange_rates import BnmExchangeRatesApi


class SimpalsAccountApi:

    def __init__(self):
        self.auth_username = os.environ['AUTH_USERNAME']

    async def fetch_all_ads(self):
        fetch_rate_result = await BnmExchangeRatesApi.fetch_rate('EUR')
        if 'rate' in fetch_rate_result:
            eur_rate = fetch_rate_result['rate']
        else:
            return fetch_rate_result

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
            ads = json.loads(response.body)['adverts']

            for ad in ads:
                result = await self.fetch_ad(ad['id'])
                if 'ad_data' in result:
                    if 'price' in result['ad_data']:
                        price = result['ad_data']['price']
                        if price['unit'] == 'eur':
                            ad['price'] = {
                                'unit': 'mdl',
                                'value': round(float(price['value']) * eur_rate)
                            }
                        else:
                            ad['price'] = price

                else:
                    return result

            return {'ads': ads}

    async def fetch_ad(self, ad_id):
        http_client = httpclient.AsyncHTTPClient()
        try:
            response = await http_client.fetch(
                httpclient.HTTPRequest(
                    f'https://partners-api.999.md/adverts/{ad_id}',
                    auth_username=self.auth_username
                )
            )
        except httpclient.HTTPError as e:
            return {'error': str(e)}
        except Exception as e:
            return {'error': str(e)}
        else:
            return {'ad_data': json.loads(response.body)}
