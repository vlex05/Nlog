from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from src import config
from src.google_sheet import GoogleSheet
from src.trader_scraper import TraderScraper

class DataFrame:
    def __init__(self):
        self.XPATH_TRADER_NAME = config.XPATH_TRADER_NAME
        self.XPATH_ROI_PNL = config.XPATH_ROI_PNL
        self.XPATH_TRADES_TABLE = config.XPATH_TRADES_TABLE
        self.XPATH_NO_POSITIONS_MESSAGE = config.XPATH_NO_POSITIONS_MESSAGE
        self.driver = self.open_browser()
        self.trader_url_list = self.get_trader_list_url()
        self.PERIOD_DAILY = 1
        self.PERIOD_WEEKLY = 2
        self.PERIOD_MONTHLY = 3
        self.PERIOD_ALL = 4
        columns = ['trader_name', 'daily_roi', 'weekly_roi', 'monthly_roi', 'all_roi', 'daily_pnl', 'weekly_pnl', 'monthly_pnl', 'all_pnl', 'number_of_trade', 'traded_open_dates', 'traded_symbols', 'traded_leverages', 'traded_types', 'traded_size', 'traded_open_price', 'traded_market_price', 'trade_pnl', 'trade_roi']
        self.df = pd.DataFrame(columns=columns)
        
    def open_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)  
        return driver
    
    def get_trader_list_url(self):  
        google_sheet = GoogleSheet().dataframe
        return list(google_sheet['Url'])
    
    def check_empty_datas(self, trade_info_list):
        is_not_empty = True
        for liste in trade_info_list:
            if not all(liste):
                is_not_empty = False
                break
            else:
                pass
        return is_not_empty
        
    def update_dataframe(self):
        self.trader_url_list = self.get_trader_list_url()
        for url in self.trader_url_list:
            self.driver.get(url)
            try:
                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, self.XPATH_TRADES_TABLE))
                )
            except:
                #print("la page met du temps a chargé, verifiez la conexion internet.")
                pass
            time.sleep(3)
            trader_scraper = TraderScraper(self.driver, self.XPATH_TRADER_NAME, self.XPATH_ROI_PNL, self.XPATH_TRADES_TABLE, self.XPATH_NO_POSITIONS_MESSAGE)
            trader_name = trader_scraper.get_trader_name()
            daily_roi = trader_scraper.get_data_overview('roi', self.PERIOD_DAILY)
            weekly_roi = trader_scraper.get_data_overview('roi', self.PERIOD_WEEKLY)
            monthly_roi = trader_scraper.get_data_overview('roi', self.PERIOD_MONTHLY)
            all_roi = trader_scraper.get_data_overview('roi', self.PERIOD_ALL)
            daily_pnl = trader_scraper.get_data_overview('pnl', self.PERIOD_DAILY)
            weekly_pnl = trader_scraper.get_data_overview('pnl', self.PERIOD_WEEKLY)
            monthly_pnl = trader_scraper.get_data_overview('pnl', self.PERIOD_MONTHLY)
            all_pnl = trader_scraper.get_data_overview('pnl', self.PERIOD_ALL)
            number_of_trade = trader_scraper.number_of_trades
            traded_open_dates = trader_scraper.get_traded_open_dates()
            traded_symbols = trader_scraper.get_traded_symbols()
            traded_leverages = trader_scraper.get_traded_leverages()
            traded_types = trader_scraper.get_traded_types()
            traded_size = trader_scraper.get_traded_size()
            traded_open_price = trader_scraper.get_traded_open_price()
            traded_market_price = trader_scraper.get_traded_market_price()
            trade_pnl = trader_scraper.get_trade_pnl()
            trade_roi = trader_scraper.get_trade_roi()
            lists_equal_length = (number_of_trade == len(traded_open_dates) == len(traded_symbols) == len(traded_leverages) == len(traded_types) == len(traded_size) == len(traded_open_price))
            trade_info_list = [traded_open_dates, traded_symbols, traded_leverages, traded_types, traded_size, traded_open_price]
            is_not_empty = self.check_empty_datas(trade_info_list)
            
            if lists_equal_length and trader_name != '--' and is_not_empty:
                self.df = self.df.append({'trader_name': trader_name, 'daily_roi': daily_roi, 'weekly_roi': weekly_roi, 'monthly_roi': monthly_roi, 'all_roi': all_roi, 'daily_pnl': daily_pnl, 'weekly_pnl': weekly_pnl, 'monthly_pnl': monthly_pnl, 'all_pnl': all_pnl, 'number_of_trade': number_of_trade, 'traded_open_dates': traded_open_dates, 'traded_symbols': traded_symbols, 'traded_leverages': traded_leverages, 'traded_types': traded_types, 'traded_size': traded_size, 'traded_open_price': traded_open_price, 'traded_market_price': traded_market_price, 'trade_pnl': trade_pnl, 'trade_roi': trade_roi}, ignore_index=True)
        self.df.to_csv("src/data/trader_info.csv")
        return self.df