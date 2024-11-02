## useful under two conditions 
## 1. Bull market 
## 2. Cyclical pumping of cryptos 
## I am already holding large amounts of BTC, ETH, SOL, so I decided to create a portfolio of cryptos that I have not invested yet. Each of these cover different sectors that I suspect would be bullish this cycle e.g. RWA, AI, Meme, L2 

import numpy as np 
import pandas as pd 
from pybithumb import Bithumb 
import os
import time 

conkey = "<MASKED>" # your Bithumb keys 
seckey = "<MASKED>" 
bithumb = Bithumb(conkey, seckey)

assets = ["BONK", "MEW", "WLD", "ONDO", "STX"] 
num_assets = len(assets) + 1 
THRESHOLD_PERCENTAGE = 0.05 # 5% threshold to minimize trades 

# function to get the current KRW balance for an asset 
def get_asset_krw_value(asset):
    asset_balance = bithumb.get_balance(asset)[0] # Balance in asset units 
    asset_price = Bithumb.get_current_price(asset) # Price in KRW per unit 
    return asset_balance * asset_price if asset_price else 0 

def get_cash_balance():
    return bithumb.get_balance("BTC")[2]  

def initial_investment():
    cash_balance = get_cash_balance() 
    allocation_for_assets = cash_balance / num_assets  
    for asset in assets:
        asset_price = Bithumb.get_current_price(asset)
        if asset_price:
            units_to_buy = allocation_for_assets / asset_price 
            bithumb.buy_market_order(asset, units_to_buy) 
    print("Initial investment complete") 

# simulates uniform distribution but modified to reduce trading costs. 
def rebalance_portfolio():
    # calculat the current total portfolio value (cash + asset values) 
    total_value = get_cash_balance() + sum(get_asset_krw_value(asset) for asset in assets)
    print(f"current total value = {total_value}")
    target_allocation = total_value / num_assets # new target per asset 

    # calculate and execute trades to rebalance 
    for asset in assets: 
        asset_price = Bithumb.get_current_price(asset) 
        if asset_price:
            target_units = target_allocation / asset_price 
            current_units = bithumb.get_balance(asset)[0] 
            diff_units = target_units - current_units 
            # only make a trade if the difference exceeds the 5% threshold 
            if abs(diff_units * asset_price) >= target_allocation * THRESHOLD_PERCENTAGE:
                if diff_units > 0: 
                    bithumb.buy_market_order(asset, diff_units) 
                elif diff_units < 0: 
                    bithumb.buy_market_order(asset, -diff_units) 
    print(f"Rebalanced portfolio. Current cash holding: {get_cash_balance()} KRW")

first_run = True

while True:
    if first_run:
        initial_investment() 
        first_run = False
    else:
        rebalance_portfolio()
    print("waiting...") 
    time.sleep(5 * 24 * 60 * 60) # rebalance after 5 days  
