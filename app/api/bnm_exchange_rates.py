from datetime import datetime
from xml.dom import minidom

import pytz
from tornado import httpclient


CURRENCIES_MAP = {
    'EUR': '47'
}


def parse_rate(rates_xml: bytes, currency_code: str):
    currency_id = CURRENCIES_MAP[currency_code]

    dom = minidom.parseString(rates_xml)
    currencies = dom.getElementsByTagName('Valute')
    for c in currencies:
        if c.hasAttribute('ID') and c.getAttribute('ID') == currency_id:
            node = c.getElementsByTagName('Value')[0]
            return float(node.firstChild.nodeValue)


class BnmExchangeRatesApi:

    @classmethod
    async def fetch_rate(cls):
        tz = pytz.timezone('Europe/Chisinau')
        current_date = datetime.now(tz).strftime('%d.%m.%Y')
        url = f'https://www.bnm.md/en/official_exchange_rates?get_xml=1&date={current_date}'

        http_client = httpclient.AsyncHTTPClient()
        try:
            response = await http_client.fetch(url)
        except httpclient.HTTPError as e:
            return {'error': str(e)}
        except Exception as e:
            return {'error': str(e)}
        else:
            return {'rate': parse_rate(response.body, 'EUR')}
