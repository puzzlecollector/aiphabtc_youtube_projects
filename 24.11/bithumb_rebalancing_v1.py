import pandas as pd 
from pybithumb import Bithumb 
import os
import time 

conkey = "<MASKED>"
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

def rebalance_portfolio():
    # Step 1: sell all holdings to convert to cash 
    for asset in assets: 
        current_units = bithumb.get_balance(asset)[0] 
        if current_units > 0:
            bithumb.sell_market_order(asset, current_units) # sell all units of each asset 
    # Step 2: calculate total portfolio cash value 
    total_cash_value = get_cash_balance() 
    target_allocation = total_cash_value / num_assets 

    # Step 3: rebalance by buying each asset to reach target allocation 
    for asset in assets: 
        asset_price = Bithumb.get_current_price(asset) 
        if asset_price:
            units_to_buy = target_allocation / asset_price 
            bithumb.buy_market_order(asset, units_to_buy) 
    print(f"Rebalanced portfolio. Cash allocations: {target_allocation} KRW, Total cash aft
er rebalancing: {get_cash_balance()} KRW") 

first_run = False

while True:
    if first_run:
        initial_investment() 
        first_run = False
    else:
        rebalance_portfolio()
    print("waiting...") 
    time.sleep(5 * 24 * 60 * 60) # wait for 5 days 
