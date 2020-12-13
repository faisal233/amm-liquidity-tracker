import db
import tokens


def test_get_eth_price():
    eth_price = db.get_eth_price()
    assert eth_price is not None


def test_get_token_data():
    token_data = db.get_token_data()
    assert token_data is not None


def test_build_db():
    db.build_db()
    token = tokens.read_one("0xdac17f958d2ee523a2206206994597c13d831ec7")
    token_symbol = token.get("symbol")

    assert token_symbol == "USDT"


# def test_update_db():
#     eth = tokens.read_one("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2")
#     old_timestamp = eth.get("timestamp")
#     db.update_db()
#     eth = tokens.read_one("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2")
#     new_timestamp = eth.get("timestamp")
#     assert new_timestamp != old_timestamp