import requests


class DataRequest:
    """
    Request for data.
    List of all coins, raw historical daily chart data.
    """

    limit = 1
    to_currency = 'USD'
    key = '1de25ecebeecbd8918f258fb09d4333c50f6d855c3107a5e98650d65868c99dd'
    url_coins = "https://min-api.cryptocompare.com/data/all/coinlist"
    url_dailyhistorical = "https://min-api.cryptocompare.com/data/histoday"
    # sample list_of_coins_request()
    coins = ['42', '300', '365', '404', '433', '611', '808', '888', '1337', '2015', 'BTC', 'ETH', 'LTC', 'DASH', 'XRP', 'XLM', 'MIOTA']
    # coins = ['BTC', 'ETH', 'XRP', 'BCH', 'EOS', 'LTC', 'BNB', 'USDT', 'XLM', 'ADA', 'TRX', 'XMR', 'BSV', 'DASH', 'XTZ', 'MIOTA', 'NEO', 'ETC', 'ONT', 'MKR', 'XEM', 'BAT', 'CRO', 'ZEC', 'VET', 'DOGE', 'USDC', 'BTG', 'REP', 'DCR', 'OMG', 'WAVES', 'NANO', 'QTUM', 'TUSD', 'LSK', 'RVN', 'BCD','HOT', 'ICX', 'ZRX', 'LINK', 'BCN', 'ZIL', 'BTS', 'BTT', 'IOST', 'PAX', 'DGB', 'NPXS', 'XVG', 'ENJ', 'AE', 'HT', 'AOA', 'KMD', 'STEEM', 'SC', 'KCS', 'BTM', 'MXM', 'WTC', 'STRAT', 'THETA', 'DAI', 'SNT', 'FCT', 'INB', 'XIN', 'ABBC', 'CNX', 'MCO', 'GNT', 'QBIT', 'ARDR', 'WAX', 'ORBS', 'THR', 'PPT', 'GXC', 'VEST', 'MONA', 'DGD', 'PAI', 'MAID', 'ODE', 'ARK']
    # coins = ['888', '1337', 'BTC', 'XRP', 'XLM']
    # coins = [ 'BTC']
    # coins = ['BTC', 'ETH', 'LTC', 'DASH', 'XRP', 'XLM']
    # coins = ['BTC', 'XRP', '888', '1337']

    def list_of_coins_request(self):
        payload_coins = {
            'api_key': self.key
        }
        all_coins = list((requests.get(self.url_coins, params=payload_coins).json())['Data'].keys())

        return all_coins

    def chart_data_request(self):
        chart_data = []
        for ticker in self.coins:
            payload_charts = {
                'api_key': self.key,
                'fsym': ticker,
                'tsym': self.to_currency,
                'limit': self.limit
            }
            chart_data.append((requests.get(self.url_dailyhistorical, params=payload_charts).json()))

        return chart_data