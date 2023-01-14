import os
import sys

sys.path.append(".")

from discord_dollar.bot import client
from discord_dollar.bot.tasks import dollar_subscribers
from discord_dollar.log import logger


@logger.catch()
def main():
    logger.debug("Started main")
    dollar_subscribers.start()
    client.run(os.getenv("DISCORD_TOKEN"))
    logger.debug("Ended main")


if __name__ == "__main__":
    main()
