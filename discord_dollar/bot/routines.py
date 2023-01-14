from datetime import datetime

from pytz import timezone

from discord_dollar.log import logger
from discord_dollar.crawler import get_usd_to_brl_exchange_rate
from discord_dollar.repository.adapter import add_usd_to_brl_item
from discord_dollar.repository.config import SessionLocal


@logger.catch()
def usd_to_brl_routine():
    logger.debug("Started usd_to_brl_routine.")
    dollar, variation = get_usd_to_brl_exchange_rate()

    if dollar is None or variation is None:
        logger.warning(
            f"Could not get conversion. [dollar={dollar};variation={variation}]"
        )
        return

    logger.info("Got conversion result.")

    time = datetime.now(tz=timezone("America/Sao_Paulo"))
    hours = time.strftime("%H:%M:%S")
    date = time.strftime("%d/%m")

    data = {
        "value": dollar,
        "hours": hours,
        "date": date,
        "variation": variation,
    }

    try:
        db = SessionLocal()
        add_usd_to_brl_item(db, data)
    except Exception as e:
        logger.warning(f"Could not add item to database. [exception={repr(e)}]")
    else:
        logger.info("Added to table.")

    logger.debug("Ended usd_to_brl routine.")
