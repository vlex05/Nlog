from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd

class TraderScraper:
    
    def __init__(self, driver, xpath_trader_name, xpath_roi_pnl, xpath_trades_table, xpath_no_positions_message):
        self.driver = driver
        self.xpath_trader_name = xpath_trader_name
        self.xpath_roi_pnl = xpath_roi_pnl
        self.xpath_trades_table = xpath_trades_table
        self.xpath_no_positions_message = xpath_no_positions_message
        self.number_of_trades = self.get_number_of_trades()
        
    def get_trader_name(self):
        try:
            trader_name = self.driver.find_element(By.XPATH, self.xpath_trader_name).text
            return trader_name
        except Exception as e:
            print(e)
            print('trader_name not found')
            return ""
        
    def get_data_overview(self, data_type, period):
        if not isinstance(period, int) or period < 1 or period > 4:
            raise ValueError('Invalid period value')
        if data_type not in ['pnl', 'roi']:
            raise ValueError('Invalid data type')
        data_index = 2 if data_type == 'pnl' else 1
        xpath = self.xpath_roi_pnl.format(period, data_index)
        try:
            element = self.driver.find_element(By.XPATH, xpath)
            data = element.text
            return data
        except Exception as e:
            print(e)
            print('Element not found -- data overview')
            return None
        
    def get_number_of_trades(self):
        try:
            trades_table = self.driver.find_element(By.XPATH, self.xpath_trades_table)
            trade_count = len([row for row in trades_table.find_elements(By.XPATH, 'tr') if 'Trade' in row.text])

            if trade_count == 0 and self.driver.find_element(By.XPATH, self.xpath_no_positions_message).text != "No positions to display":
                for i in range(10):
                    trades_table = self.driver.find_element(By.XPATH, self.xpath_trades_table)
                    trade_count = len([row for row in trades_table.find_elements(By.XPATH, 'tr') if 'Trade' in row.text])
                    if trade_count != 0:
                        break

            return trade_count
        except Exception as e:
            print(e, 'number of trades')
            return 0
    
    def get_traded_open_dates(self):
        try:
            date_list = []

            for i in range(1, self.number_of_trades + 1):
                xpath = f"{self.xpath_trades_table}/tr[{i}]/td[6]"
                date_element = self.driver.find_element(By.XPATH, xpath)
                date_list.append(date_element.text)

            return date_list
        except Exception as e:
            print(e, 'traded open dates')
            return []
        
    def get_traded_symbols(self):
        try:
            symbol_list = []

            for i in range(1, self.number_of_trades + 1):
                xpath = f"{self.xpath_trades_table}/tr[{i}]/td[1]/div/div[1]"
                symbol_element = self.driver.find_element(By.XPATH, xpath)
                symbol_list.append(symbol_element.text)

            return symbol_list
        except Exception as e:
            print(e, 'traded symbols')
            return []
        
    def get_traded_leverages(self):
        try:
            leverage_list = []

            for i in range(1, self.number_of_trades + 1):
                xpath = f"{self.xpath_trades_table}/tr[{i}]/td[1]/div/div[2]/div[2]/div"
                leverage_element = self.driver.find_element(By.XPATH, xpath)
                leverage_list.append(leverage_element.text)
            return leverage_list
        except Exception as e:
            print(e, 'traded leverages')
            return []
    
    def get_traded_types(self):
        try:
            types_list = []
            for i in range(1, self.number_of_trades + 1):
                xpath = f"{self.xpath_trades_table}/tr[{i}]/td[1]/div/div[2]/div[1]"
                type_element = self.driver.find_element(By.XPATH, xpath)
                types_list.append(type_element.text)
            return types_list
        except Exception as e:
            print(e, 'traded types')
            return []
        
    def get_traded_size(self):
        try:
            size_list = []

            for i in range(1, self.number_of_trades + 1):
                xpath = f"{self.xpath_trades_table}/tr[{i}]/td[2]"
                size_element = self.driver.find_element(By.XPATH, xpath)
                size_list.append(size_element.text)      
            return size_list
        except Exception as e:
            print(e, 'traded size')
            return []
    
    def get_traded_open_price(self):
        try:
            open_price_list = []
            for i in range(1, self.number_of_trades + 1):
                xpath = f"{self.xpath_trades_table}/tr[{i}]/td[3]"
                open_price_element = self.driver.find_element(By.XPATH, xpath)
                open_price_list.append(open_price_element.text)
            return open_price_list
        except Exception as e:
            print(e, 'open price')
            return []
        
    def get_traded_market_price(self):
        try:
            market_price_list = []
            for i in range(1, self.number_of_trades + 1):
                xpath = f"{self.xpath_trades_table}/tr[{i}]/td[4]"
                market_price_element = self.driver.find_element(By.XPATH, xpath)
                market_price_list.append(market_price_element.text)
            return market_price_list
        except Exception as e:
            print(e, 'market price')
            return []
        
    def get_trade_pnl(self):
        try:
            pnl_list = []
            for i in range(1, self.number_of_trades + 1):
                xpath = f"{self.xpath_trades_table}/tr[{i}]/td[5]/div/span[1]" 
                pnl_element = self.driver.find_element(By.XPATH, xpath)
                pnl_list.append(pnl_element.text)
            return pnl_list
        except Exception as e:
            print(e, 'trade pnl')
            return []
    
    def get_trade_roi(self):
        try:
            roi_list = []
            for i in range(1, self.number_of_trades + 1):
                xpath = f"{self.xpath_trades_table}/tr[{i}]/td[5]/div/span[2]" 
                roi_element = self.driver.find_element(By.XPATH, xpath)
                roi_list.append(roi_element.text)
            return roi_list
        except Exception as e:
            print(e, 'trade roi')
            return []




