from datetime import datetime

from config import ma, db


class Token(db.Model):
    __tablename__ = "token"
    token_id = db.Column(db.String(32), primary_key=True)
    symbol = db.Column(db.String(32))
    name = db.Column(db.String(32))
    total_liquidity = db.Column(db.Float())
    eth_value = db.Column(db.Float())
    total_eth_value = db.Column(db.Float())
    total_usd_value = db.Column(db.Float())
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __str__(self):
        return "Token symbol: " + self.symbol


class TokenSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    class Meta:
        model = Token
        sqla_session = db.session
