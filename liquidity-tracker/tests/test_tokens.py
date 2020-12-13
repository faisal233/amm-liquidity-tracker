import pytest
import tokens
import models
import load_db_data
import json
from werkzeug.exceptions import Conflict, NotFound


def test_read_all():
    load_db_data.init_db()
    expected = [
        {
            "eth_value": 1.0,
            "name": "Wrapped Ether",
            "symbol": "WETH",
            "timestamp": "2020-12-13T00:08:36.471087+00:00",
            "token_id": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
            "total_eth_value": 1084745.6062393214,
            "total_liquidity": 1084745.6062393214,
            "total_usd_value": 617944642.406465,
        },
        {
            "eth_value": 0.0017545156183593797,
            "name": "Tether USD",
            "symbol": "USDT",
            "timestamp": "2020-12-13T00:08:36.477148+00:00",
            "token_id": "0xdac17f958d2ee523a2206206994597c13d831ec7",
            "total_eth_value": 288268.1453647538,
            "total_liquidity": 164300700.631157,
            "total_usd_value": 164217080.00474447,
        },
        {
            "eth_value": 0.0017530458947402543,
            "name": "USDC",
            "symbol": "USD//C",
            "timestamp": "2020-12-13T00:08:36.484720+00:00",
            "token_id": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
            "total_eth_value": 267484.28711764846,
            "total_liquidity": 152582592.344099,
            "total_usd_value": 152377185.21424127,
        },
    ]

    actual = tokens.read_all()

    for a, e in zip(actual, expected):
        assert a.get("eth_value") == e.get("eth_value")
        assert a.get("name") == e.get("name")
        assert a.get("symbol") == e.get("symbol")
        assert a.get("token_id") == e.get("token_id")
        assert a.get("total_eth_value") == e.get("total_eth_value")
        assert a.get("total_liquidity") == e.get("total_liquidity")
        assert a.get("total_usd_value") == e.get("total_usd_value")


def test_read():
    e = {
        "eth_value": 0.0017545156183593797,
        "name": "Tether USD",
        "symbol": "USDT",
        "timestamp": "2020-12-13T00:08:36.477148+00:00",
        "token_id": "0xdac17f958d2ee523a2206206994597c13d831ec7",
        "total_eth_value": 288268.1453647538,
        "total_liquidity": 164300700.631157,
        "total_usd_value": 164217080.00474447,
    }

    a = tokens.read_one("0xdac17f958d2ee523a2206206994597c13d831ec7")

    assert a.get("eth_value") == e.get("eth_value")
    assert a.get("name") == e.get("name")
    assert a.get("symbol") == e.get("symbol")
    assert a.get("token_id") == e.get("token_id")
    assert a.get("total_eth_value") == e.get("total_eth_value")
    assert a.get("total_liquidity") == e.get("total_liquidity")
    assert a.get("total_usd_value") == e.get("total_usd_value")


def test_create():
    dup_token = {
        "eth_value": 1.0,
        "name": "Wrapped Ether",
        "symbol": "WETH",
        "token_id": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
        "total_eth_value": 1084745.6062393214,
        "total_liquidity": 1084745.6062393214,
        "total_usd_value": 617944642.406465,
    }

    new_token = {
        "eth_value": 33.108458139581096,
        "name": "Wrapped BTC",
        "symbol": "WBTC",
        "token_id": "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599",
        "total_eth_value": 143582.61059057893,
        "total_liquidity": 4336.7350417,
        "total_usd_value": 81223136.04616883,
    }

    with pytest.raises(Conflict) as err:
        _, _ = tokens.create(dup_token)

    assert err.type is Conflict

    _, res_code = tokens.create(new_token)
    assert res_code == 201


def test_update():
    update_token = {
        "eth_value": 1.0,
        "name": "Wrapped Ether",
        "symbol": "WETH",
        "token_id": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
        "total_eth_value": 1,
        "total_liquidity": 1,
        "total_usd_value": 1,
    }

    with pytest.raises(NotFound) as err:
        tokens.update("bad_ID", update_token)

    assert err.type is NotFound

    tokens.update("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2", update_token)
    update_resonse = tokens.read_one("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2")

    assert update_resonse.get("total_eth_value") == 1
    assert update_resonse.get("total_liquidity") == 1
    assert update_resonse.get("total_usd_value") == 1
