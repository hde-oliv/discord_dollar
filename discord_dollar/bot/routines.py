from datetime import datetime

from pytz import timezone

from discord_dollar.log import logger
from discord_dollar.crawler import get_real_dollar_conversion
from discord_dollar.repository.adapter import add_table


@logger.catch()
def fetch_exchange_routine():
    logger.debug("Started fetch_exchange_routine.")
    dollar, variation = get_real_dollar_conversion()

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
        "result": [dollar],
        "hours": [hours],
        "date": [date],
        "variation": [variation],
    }

    add_table("usd_to_brl", data)
    logger.info("Added to table.")
    logger.debug("Ended fetch_exchange_routine.")
