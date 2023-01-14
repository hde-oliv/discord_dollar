import os
import sys

sys.path.append(".")

from discord_dollar.bot import client
from discord_dollar.bot.tasks import dollar_subscribers
from discord_dollar.log import logger
from discord_dollar.repository.config import engine
import discord_dollar.repository.models as models
from discord_dollar.bot.commands import register_commands

models.Base.metadata.create_all(bind=engine)


@logger.catch()
def main():
    logger.debug("Started main")
    dollar_subscribers.start()
    register_commands(client)
    client.run(os.getenv("DISCORD_TOKEN"))
    logger.debug("Ended main")


if __name__ == "__main__":
    main()
