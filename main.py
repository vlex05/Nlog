#!/usr/bin/env python
# coding: utf-8

# In[4]:


from src import config
from src.data_frame import DataFrame
from src.checking_trades import CheckingTrades
from src.google_sheet import GoogleSheet
import warnings
import time
warnings.filterwarnings("ignore")


# In[5]:


scrap = DataFrame()


# In[6]:


trade_action = CheckingTrades()


# In[7]:


while True:
    df = scrap.update_dataframe()
    trade_action.check_if_same()
    time.sleep(10)


# In[ ]:




