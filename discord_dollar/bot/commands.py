from .config import client

from discord_dollar.bot.routines import fetch_exchange_routine
from discord_dollar.bot.utils import create_dollar_embed
from discord_dollar.log import logger
from discord_dollar.repository.adapter import add_table, get_table


@client.command()
@logger.catch()
async def dollar(ctx):
    logger.debug(
        "Started dollar command. "
        f"[name={ctx.message.author.name};id={ctx.message.author.id};"
        f"channel_name={ctx.channel.name};channel_id={ctx.channel.id};"
        f"guild_name={ctx.guild.name};guild_id={ctx.guild.id}]"
    )

    df = get_table("usd_to_brl")
    logger.info("Got table.")
    latest = df.iloc[-1]

    embed = create_dollar_embed(latest)
    logger.info("Got embed.")

    logger.debug("Ended dollar command.")
    await ctx.send(embed=embed)


@client.command()
@logger.catch()
async def dollar_now(ctx):
    logger.debug(
        "Started dollar_now command. "
        f"[name={ctx.message.author.name};id={ctx.message.author.id};"
        f"channel_name={ctx.channel.name};channel_id={ctx.channel.id};"
        f"guild_name={ctx.guild.name};guild_id={ctx.guild.id}]"
    )

    fetch_exchange_routine()

    df = get_table("usd_to_brl")
    logger.info("Got table.")
    latest = df.iloc[-1]

    embed = create_dollar_embed(latest)

    logger.debug("Ended dollar_now command.")
    await ctx.send(embed=embed)


@client.command()
@logger.catch()
async def subscribe(ctx):
    logger.debug(
        "Started subscribe command. "
        f"[name={ctx.message.author.name};id={ctx.message.author.id};"
        f"channel_name={ctx.channel.name};channel_id={ctx.channel.id};"
        f"guild_name={ctx.guild.name};guild_id={ctx.guild.id}]"
    )
    df = get_table("channels")
    logger.info("Got table.")

    channels = df.ix[:, 0]
    channel = ctx.channel.id

    if channel in channels:
        logger.info("Channel already added.")
        logger.debug("Ended subscribe command.")
        await ctx.send("Channel already added.")
    else:
        data = {"channel": [ctx.channel.id]}
        add_table("channels", data)

        logger.info("Added table.")
        logger.info("Channel added.")
        logger.debug("Ended subscribe command.")

        await ctx.send("Channel added.")
