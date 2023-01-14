import os
import sys

sys.path.append(".")

from discord_dollar.bot import client
from discord_dollar.bot.tasks import sub_list
from discord_dollar.configure.log import get_logger

logger = get_logger()


@logger.catch()
def main():
    logger.debug("Started main")
    sub_list.start()
    client.run(os.getenv("DISCORD_TOKEN"))
    logger.debug("Ended main")


if __name__ == "__main__":
    main()
