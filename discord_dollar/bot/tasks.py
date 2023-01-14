from discord.ext import tasks

from discord_dollar.bot.routines import usd_to_brl_routine
from discord_dollar.bot.utils import create_dollar_embed
from discord_dollar.log import logger
from discord_dollar.repository.adapter import get_table

from .config import client


@tasks.loop(hours=2)
@logger.catch()
async def dollar_subscribers():
    logger.debug("Started sub_list task")

    usd_to_brl_routine()
    logger.info("Fetched new values.")

    try:
        channels = get_table("channels")
        channels = channels.drop_duplicates()
    except:
        logger.warning("No channels to send.")
        return

    embed = create_dollar_embed()
    logger.info("Embed created.")

    for i, r in channels.iterrows():
        channel = client.get_channel(r["channel"])
        await channel.send(embed=embed)
    logger.info("Embed sent to all channels.")

    logger.debug("Ended sub_list task")


@dollar_subscribers.before_loop
async def before_looping():
    await client.wait_until_ready()
