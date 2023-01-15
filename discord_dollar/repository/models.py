from sqlalchemy import Column, Integer, String, Float, Numeric

from .config import Base


class DollarSubscription(Base):
    __tablename__ = "dollar_subscription"

    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(String, unique=True)
    guild_id = Column(String)
    user_id = Column(String)


class USDToBRL(Base):
    __tablename__ = "usd_to_brl"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float)
    variation = Column(Float)
    hours = Column(String)
    date = Column(String)
