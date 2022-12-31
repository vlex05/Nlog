import ccxt
from src import config

class Trade:
    def __init__(self):
        self.bitget_auth_object = {
            "apiKey": config.API_KEY,
            "secret": config.SECRET_KEY,
            "password": config.PASSWORD,
            'options': {
                'defaultType': 'swap',
            }
        }
        if self.bitget_auth_object['secret'] is None:
            self.session = ccxt.bitget()
        else:
            self.session = ccxt.bitget(self.bitget_auth_object)
        self.market = self.session.load_markets()
        self.risk_position = 0.03
        self.futur_path = '_UMCBL'
    
    def set_margin_mode(self, symbol):
        try:
            self.session.set_margin_mode('Fixed', symbol=symbol)
        except Exception as e:
            print("Erreur lors du changement de paramètre pour le margin mode: ", e)
            return
    
    def execute_trade(self, trade_type, symbol, leverage):
        try:
            side = 'sell' if trade_type == 'Short' else 'buy'
            holdside = trade_type.lower()
            pair_1 = symbol.split()[0][:-4] + 'USDT'
            pair_2 = self.session.markets_by_id[pair_1 + self.futur_path][0]['symbol']
            self.set_margin_mode(pair_2)

            balance = self.session.fetch_balance()
            usdt_balance = float(balance['info'][0]['available'])
            usdt_position = usdt_balance * self.risk_position * leverage
            tickers = self.session.fetch_tickers()
            symbol_position = usdt_position / tickers[pair_2]['last']
            amount = self.session.amount_to_precision(pair_2, symbol_position)

            self.session.set_leverage(leverage=leverage, symbol=pair_2, params={"holdSide": holdside})
            self.session.create_market_order(symbol=pair_2, side=side, amount=amount, params={"reduceOnly": False})
            return amount
        
        except Exception as e:
            print(e)
            print("Il y a eu une erreur lors de l'exécution de l'ordre d'ouverture' du trade")
            return

    def close_trade(self, trade_type, symbol, amount):
        try:
            side = 'buy' if trade_type == 'Short' else 'sell'
            pair_1 = symbol.split()[0][:-4] + 'USDT'
            pair_2 = self.session.markets_by_id[pair_1 + self.futur_path][0]['symbol']

            self.session.create_market_order(symbol=pair_2, side=side, amount=amount, params={"reduceOnly": True})
        except Exception as e:
            print(e)
            print("Il y a eu une erreur lors de l'exécution de l'ordre de fermeture du trade")
            return