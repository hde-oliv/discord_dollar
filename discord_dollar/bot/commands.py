from discord_dollar.bot.routines import get_usd_to_brl_exchange_rate
from discord_dollar.bot.utils import create_dollar_embed
from discord_dollar.log import logger
from discord_dollar.repository.adapter import (
    get_usd_to_brl_table,
    add_dollar_subscription_item,
    get_dollar_subscriptions_table,
)
from discord_dollar.repository.config import SessionLocal
from discord.ext import commands


@commands.command()
@logger.catch()
async def dollar(ctx):
    logger.debug(
        "Started dollar command. "
        f"[name={ctx.message.author.name};id={ctx.message.author.id};"
        f"channel_name={ctx.channel.name};channel_id={ctx.channel.id};"
        f"guild_name={ctx.guild.name};guild_id={ctx.guild.id}]"
    )

    df = get_usd_to_brl_table()
    logger.info("Got table.")
    latest = df.iloc[-1]

    embed = create_dollar_embed(latest)
    logger.info("Got embed.")

    logger.debug("Ended dollar command.")
    await ctx.send(embed=embed)


@commands.command()
@logger.catch()
async def dollar_now(ctx):
    logger.debug(
        "Started dollar_now command. "
        f"[name={ctx.message.author.name};id={ctx.message.author.id};"
        f"channel_name={ctx.channel.name};channel_id={ctx.channel.id};"
        f"guild_name={ctx.guild.name};guild_id={ctx.guild.id}]"
    )

    get_usd_to_brl_exchange_rate()

    df = get_usd_to_brl_table()
    logger.info("Got table.")
    latest = df.iloc[-1]

    embed = create_dollar_embed(latest)

    logger.debug("Ended dollar_now command.")
    await ctx.send(embed=embed)


@commands.command()
@logger.catch()
async def dollar_subscribe(ctx):
    logger.debug(
        "Started dollar subscribe command. "
        f"[name={ctx.message.author.name};id={ctx.message.author.id};"
        f"channel_name={ctx.channel.name};channel_id={ctx.channel.id};"
        f"guild_name={ctx.guild.name};guild_id={ctx.guild.id}]"
    )
    df = get_dollar_subscriptions_table()
    logger.info("Got table.")

    channels = df.ix[:, 0]
    channel = ctx.channel.id

    if channel in channels:
        logger.info("Channel already added.")
        logger.debug("Ended subscribe command.")
        await ctx.send("Channel already added.")
    else:
        data = {
            "channel_id": ctx.channel.id,
            "guild_id": ctx.guild.id,
            "user_id": ctx.message.author.id,
        }

        try:
            db = SessionLocal()
            add_dollar_subscription_item(db, data)
        except Exception as e:
            logger.warning(f"Could not add item to database. [exception={repr(e)}]")
        else:
            logger.info("Added to table.")
            logger.info("Channel added.")
            logger.debug("Ended dollar_subscribe command.")
            await ctx.send("Channel added.")

@logger.catch()
def register_commands(client):
    client.add_command(dollar_now)
    client.add_command(dollar)
    client.add_command(dollar_subscribe)
