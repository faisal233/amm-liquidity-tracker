"""Initialization script to load test data into the DB."""
from models import Token
from config import ma, db
from os import path, remove


def init_db():
    """Init the DB with some fake data."""

    # Delete database file if it exists currently
    if path.exists("liquidity-tracker/token.db"):
        db.drop_all()

    db.create_all()
    db_items = [
        Token(
            token_id="0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
            symbol="WETH",
            name="Wrapped Ether",
            total_liquidity=1084745.6062393214,
            eth_value=1.0,
            total_eth_value=1084745.6062393214,
            total_usd_value=617944642.406465,
        ),
        Token(
            token_id="0xdac17f958d2ee523a2206206994597c13d831ec7",
            symbol="USDT",
            name="Tether USD",
            total_liquidity=164300700.631157,
            eth_value=0.0017545156183593797,
            total_eth_value=288268.1453647538,
            total_usd_value=164217080.00474447,
        ),
        Token(
            token_id="0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
            symbol="USD//C",
            name="USDC",
            total_liquidity=152582592.344099,
            eth_value=0.0017530458947402543,
            total_eth_value=267484.28711764846,
            total_usd_value=152377185.21424127,
        ),

    ]
    for item in db_items:
        # pylint: disable=no-member
        db.session.merge(item)
        db.session.commit()
