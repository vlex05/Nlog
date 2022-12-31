#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import ast
from src.trade import Trade
import telegram
import datetime


class CheckingTrades:
    def __init__(self):
        self.path = "src/data/trader_info.csv"
        df = pd.read_csv(self.path)
        df = df.iloc[:, 1:]
        self.df = df
        data = pd.concat([self.df.iloc[:, 0:1], self.df.iloc[:, 9:16]], axis=1)
        self.data = data
        dt = pd.DataFrame(columns=['id_message', 'name', 'open_info','amount'])
        self.dt = dt
        
    def get_live_time(self):
        now = datetime.datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        return date_time

    def parse_string_values(self, data):
        for key, value in data.items():
            try:
                data[key] = ast.literal_eval(value)
            except Exception as e:
                pass
        return data
    
    def create_compare_list(self, second_or_last_row):
        result = []
        for i in range(0,second_or_last_row['number_of_trade']):
            result.append(second_or_last_row['traded_symbols'][i] + ' ' + second_or_last_row['traded_leverages'][i] + ' ' + second_or_last_row['traded_types'][i])
        return result
        
    def check_if_same(self):
        df = pd.read_csv(self.path)
        df = df.iloc[:, 1:]
        self.df = df
        data = pd.concat([self.df.iloc[:, 0:1], self.df.iloc[:, 9:16]], axis=1)
        self.data = data
        self.dt.to_csv('src/data/trader.csv')
        
        unique_traders = self.data['trader_name'].drop_duplicates()

        for trader in unique_traders:
            num_rows = self.data[self.data['trader_name'] == trader].shape[0]
            if num_rows <= 1:
                print("\nIl n'y a qu'une seule ligne pour le trader {}.".format(trader))
            else:
                last_row = self.data[self.data['trader_name'] == trader].iloc[-1]
                last_row = self.parse_string_values(last_row)
                second_last_row = self.data[self.data['trader_name'] == trader].iloc[-2]
                second_last_row = self.parse_string_values(second_last_row)
                
                are_same = last_row.equals(second_last_row)
                if not are_same:
                    print("\nLes données ne sont pas les mêmes entre la dernière ligne et l'avant-dernière ligne pour le trader {}.".format(trader))
                    self.check_trade(last_row,second_last_row)
                else:
                    print("\nLes données sont les mêmes entre la dernière ligne et l'avant-dernière ligne pour le trader {}.".format(trader))
    
    def check_trade(self, last_row, second_last_row):
        previous_traded = self.create_compare_list(second_last_row)
        current_traded = self.create_compare_list(last_row)

        if type(previous_traded) == str:
            previous_traded = [previous_traded]
        if type(current_traded) == str:
            current_traded = [current_traded]

        newly_opened_trades = [item for item in current_traded if item not in previous_traded]
        
        if len(newly_opened_trades) > 0:
            self.message_open_trade(newly_opened_trades, last_row)

        closed_trades = [item for item in previous_traded if item not in current_traded]
        
        if len(closed_trades) > 0:
            self.message_close_trade(closed_trades, second_last_row)

        if len(closed_trades) == 0 and len(newly_opened_trades) == 0:
            print("\nIl n'y a aucune ouverture 🚨 ni fermeture 🔒 de trade, il y a donc un changement de volume 📊 dans une position pour le trader \033[1m{}\033[0m.".format(last_row['trader_name']))

    def message_open_trade(self, new_open_trades, position_details):

        for open_trade in new_open_trades:
            open_trade_index = position_details['traded_symbols'].index(open_trade.split(' ')[0] + ' ' + open_trade.split(' ')[1])

            position_name = position_details.get('trader_name')
            symbol = position_details.get('traded_symbols')[open_trade_index]
            trade_type = position_details.get('traded_types')[open_trade_index]
            leverage = position_details.get('traded_leverages')[open_trade_index]
            open_date = position_details.get('traded_open_dates')[open_trade_index]
            open_prices = position_details.get('traded_open_price')[open_trade_index]

            try:

                bot = telegram.Bot(token="5905641178:AAEPlfF-xbI8V3WxWiddCe2H9QMCY8nmZWY")
                id_ = "-1001552070973"

                message = "🚨 *Nouvelle position ouverte* 🚨\n\nTrader: *{}* \nPaire: *{}*\nType: *{}*🟢\nLevier: *{}*\nDate d'ouverture: *{}*\nPrix d'ouverture: *{}*".format(position_name, symbol, trade_type, leverage, open_date, open_prices) if trade_type == 'Long' else "🚨 *Nouvelle position ouverte* 🚨\n\nTrader: *{}* \nPaire: *{}*\nType: *{}*🔴\nLevier: *{}*\nDate d'ouverture: *{}*\nPrix d'ouverture: *{}*".format(position_name, symbol, trade_type, leverage, open_date, open_prices)    
                print()
                print(message)
                
                trade_instance = Trade()
                leverage_trade = int(leverage[:-1])
                
                amount = trade_instance.execute_trade(trade_type = trade_type, symbol=symbol, leverage=leverage_trade)
                
                message_id_ = bot.send_message(chat_id=id_, text=message, parse_mode=telegram.ParseMode.MARKDOWN)
                id_message = message_id_.message_id
                
                self.dt = self.dt.append({'id_message': id_message, 'name': position_name, 'open_info': open_trade, 'amount': amount}, ignore_index=True)
            except Exception as e:
                print(e)
    
    def message_close_trade(self, new_close_trades, position_details):

        for close_trade in new_close_trades:
            close_trade_index = position_details['traded_symbols'].index(close_trade.split(' ')[0] + ' ' + close_trade.split(' ')[1])

            position_name = position_details.get('trader_name')
            symbol = position_details.get('traded_symbols')[close_trade_index]
            trade_type = position_details.get('traded_types')[close_trade_index]
            leverage = position_details.get('traded_leverages')[close_trade_index]
            open_date = position_details.get('traded_open_dates')[close_trade_index]
            open_prices = position_details.get('traded_open_price')[close_trade_index]
            pnl_close = self.df['trade_roi'][self.df['trader_name']==position_name].iloc[-2]
            pnl_close = ast.literal_eval(pnl_close)[close_trade_index].replace("(", "").replace(")", "")

            try:
                
                bot = telegram.Bot(token="5905641178:AAEPlfF-xbI8V3WxWiddCe2H9QMCY8nmZWY")
                id_ = "-1001552070973"
                close_date = self.get_live_time()
                message = "🔒 *Nouvelle position fermée* 🔒\n\nTrader: *{}*\nPaire: *{}*\nType: *{}*🟢\nLevier: *{}*\nDate de fermeture: *{}*\nPNL: *{}*".format(position_name, symbol, trade_type, leverage, close_date, pnl_close) if trade_type == 'Long' else "🔒 *Nouvelle position fermée* 🔒\n\nTrader: *{}*\nPaire: *{}*\nType: *{}*🔴\nLevier: *{}*\nDate de fermeture: *{}*\nPNL: *{}*".format(position_name, symbol, trade_type, leverage, close_date, pnl_close)
                print()
                print(message)
                trader_dt = self.dt[self.dt['name']==position_name]
                trade_instance = Trade()
                amount_close = trader_dt['amount'][trader_dt['open_info'] ==close_trade].tail(1).values[0]
                finish_trade = trade_instance.close_trade(trade_type = trade_type, symbol= symbol, amount=amount_close)
                bot.send_message(chat_id='-1001552070973', text=message, reply_to_message_id=trader_dt['id_message'][trader_dt['open_info'] ==close_trade].tail(1).values[0], parse_mode=telegram.ParseMode.MARKDOWN)
            except Exception as e:
                print("\nLa position a surement aucun ID de message telegram ! Pas de problème..")
                print(e)
                pass


# In[ ]:




