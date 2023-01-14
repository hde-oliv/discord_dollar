from .conf import bot
from discord.ext import tasks
from discord_dollar.configure.log import get_logger
from discord_dollar.repository.adapter import get_table
from discord_dollar.bot.routines import fetch_exchange_routine
from discord_dollar.bot.utils import get_dollar_embed

logger = get_logger()


@tasks.loop(hours=2)
@logger.catch()
async def sub_list():
    logger.debug("Started sub_list task")

    fetch_exchange_routine()
    logger.info("Fetched new values.")

    try:
        channels = get_table("channels")
        channels = channels.drop_duplicates()
    except:
        logger.warning("No channels to send.")
        return

    embed = get_dollar_embed()
    logger.info("Embed created.")

    for i, r in channels.iterrows():
        channel = bot.get_channel(r["channel"])
        await channel.send(embed=embed)
    logger.info("Embed sent to all channels.")

    logger.debug("Ended sub_list task")


@sub_list.before_loop
async def before_looping():
    await bot.wait_until_ready()