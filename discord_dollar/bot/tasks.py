from discord.ext import tasks

from discord_dollar.bot.routines import usd_to_brl_routine
from discord_dollar.bot.utils import create_dollar_embed
from discord_dollar.log import logger
from discord_dollar.repository.adapter import get_dollar_subscriptions_table

from .config import client


@tasks.loop(hours=2)
@logger.catch()
async def dollar_subscribers():
    logger.debug("Started dollar_subscription task")

    usd_to_brl_routine()
    logger.info("Fetched new values.")

    channels = get_dollar_subscriptions_table()
    logger.info("Got table.")
    
    if len(channels.index) == 0:
        logger.info("No channels to send.")
        logger.debug("Ended dollar_subscription task")
        return

    embed = create_dollar_embed()
    logger.info("Embed created.")

    for i, r in channels.iterrows():
        channel = client.get_channel(r["channel_id"])
        await channel.send(embed=embed)
        logger.debug(f"Embed sent to {r['channel_id']}")
    logger.info("Embed sent to all channels.")

    logger.debug("Ended dollar_subscription task")


@dollar_subscribers.before_loop
async def before_looping():
    await client.wait_until_ready()
