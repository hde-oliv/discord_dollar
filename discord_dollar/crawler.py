from selenium import webdriver
from selenium.webdriver.common.by import By

from discord_dollar.log import logger

from typing import Tuple


def get_usd_to_brl_exchange_rate() -> Tuple[str, str]:
    logger.debug("Started get_usd_to_brl_exchange_rate")
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    options.add_argument("--ignore-ssl-errors=yes")
    options.add_argument("--ignore-certificate-errors")

    driver = webdriver.Firefox(options=options)
    driver.get("https://economia.uol.com.br/cotacoes/cambio/")
    logger.info("Got page.")

    try:
        dollar = driver.find_element(
            by=By.CSS_SELECTOR,
            value=".chart-info-pay > .info-content > .chart-info-val",
        )
        variation = driver.find_element(
            by=By.CSS_SELECTOR,
            value=".chart-info-var > .info-content > .chart-info-val > .ng-binding",
        )
    except Exception as e:
        logger.warning(f"Failed to grab information on page. [exception={repr(e)}]")
    else:
        if dollar is None or variation is None:
            logger.warning(
                f"Failed to grab information on page. [dollar={dollar};variation={variation}]"
            )

        dollar = dollar.get_attribute("innerHTML")
        variation = variation.get_attribute("innerHTML")

        dollar = dollar.replace(",", ".")
        variation = variation.replace(",", ".")

        logger.debug("Ended get_usd_to_brl_exchange_rate")
        return dollar, variation
