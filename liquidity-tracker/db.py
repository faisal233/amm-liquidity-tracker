from datetime import datetime
from json import loads
from os import path, remove
from threading import Timer

import requests

import config
import models

url = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2"


def get_eth_price():
    data = """
    query{
        bundle(id: 1) { 
            id ethPrice
        }
    }
    """
    response = requests.post(url, json={"query": data})

    return float(loads(response.content)["data"]["bundle"]["ethPrice"])


def get_token_data():
    data = """
    query{
        tokens(first: 500, skip: $skip, orderBy: tradeVolumeUSD, orderDirection: desc) {
            id
            name
            symbol
            totalLiquidity
            derivedETH
        }
    }
    """

    response = requests.post(url, json={"query": data})
    return response


def build_db():
    _eth_price = get_eth_price()
    response = get_token_data()

    # Delete database file if it exists currently
    if path.exists("liquidity-tracker/token.db"):
        remove("liquidity-tracker/token.db")

    # Create the database
    config.db.create_all()

    for token in loads(response.content)["data"]["tokens"]:
        _id = token.get("id")
        _symbol = token.get("symbol")
        _name = token.get("name")
        _liq = float(token.get("totalLiquidity"))
        _eth_val = float(token.get("derivedETH"))
        _total_eth_val = _liq * _eth_val
        _total_usd_val = _total_eth_val * _eth_price

        t = models.Token(
            token_id=_id,
            symbol=_symbol,
            name=_name,
            total_liquidity=_liq,
            eth_value=_eth_val,
            total_eth_value=_total_eth_val,
            total_usd_value=_total_usd_val,
        )
        config.db.session.add(t)

    config.db.session.commit()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Database created at", current_time)


def update_db(update_interval):
    t = Timer(update_interval, update_db, args=[update_interval])
    t.daemon = True
    t.start()

    _eth_price = get_eth_price()
    response = get_token_data()

    for token in loads(response.content)["data"]["tokens"]:
        _id = token.get("id")
        _symbol = token.get("symbol")
        _name = token.get("name")
        _liq = float(token.get("totalLiquidity"))
        _eth_val = float(token.get("derivedETH"))
        _total_eth_val = _liq * _eth_val
        _total_usd_val = _total_eth_val * _eth_price

        existing_token = models.Token.query.get(_id)
        if existing_token:
            existing_token.total_liquidity = _liq
            existing_token.eth_value = _eth_val
            existing_token.total_eth_value = _total_eth_val
            existing_token.total_usd_value = _total_usd_val
        else:
            t = models.Token(
                token_id=_id,
                symbol=_symbol,
                name=_name,
                total_liquidity=_liq,
                eth_value=_eth_val,
                total_eth_value=_total_eth_val,
                total_usd_value=_total_usd_val,
            )
            config.db.session.add(t)

    config.db.session.commit()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Database updated at", current_time)

# build_db()
