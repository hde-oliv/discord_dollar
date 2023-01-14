import pandas as pd
from .config import engine
from sqlalchemy.orm import Session
from . import models


def get_usd_to_brl_table() -> pd.DataFrame:
    df = pd.read_sql_table("usd_to_brl", con=engine)
    return df


def get_dollar_subscriptions_table() -> pd.DataFrame:
    df = pd.read_sql_table("dollar_subscription", con=engine)
    return df


def add_usd_to_brl_item(db: Session, item: dict):
    db_item = models.USDToBRL(**item)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return True


def add_dollar_subscription_item(db: Session, item: dict):
    db_item = models.DollarSubscription(**item)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return True
