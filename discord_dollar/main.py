import discord
from datetime import datetime
from discord.ext import commands, tasks
from log import get_logger
from crawler import get_real_dollar_conversion
from repository import get_table, add_table
from dotenv import dotenv_values
from pytz import timezone

config = dotenv_values(".env")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="%", intents=intents)
logger = get_logger()


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


@logger.catch()
def get_dollar_embed():
    df = get_table("usd_to_brl")
    logger.info("Got table.")

    latest = df.iloc[-1]

    def check_variation():
        variation = float(latest["variation"])

        if variation > 0:
            return ("Subiu! :outbox_tray:", variation)
        elif variation < 0:
            return ("Desceu! :inbox_tray:", variation)

    variation = check_variation()
    embed = discord.Embed(
        title="Valor do Dólar",
        description=f"{variation[0]} ({variation[1]:.2f}%)",
        color=0xFF5733,
    )

    embed.add_field(name="Valor", value=latest["result"], inline=False)
    embed.add_field(name="Horário", value=latest["hours"], inline=True)
    embed.add_field(name="Data", value=latest["date"], inline=True)
    logger.info("Embed created.")
    return embed


@bot.command()
@logger.catch()
async def dollar(ctx):
    logger.debug(
        "Started dollar command. "
        f"[name={ctx.message.author.name};id={ctx.message.author.id};"
        f"channel_name={ctx.channel.name};channel_id={ctx.channel.id};"
        f"guild_name={ctx.guild.name};guild_id={ctx.guild.id}]"
    )

    embed = get_dollar_embed()

    logger.debug("Ended dollar command.")
    await ctx.send(embed=embed)


@bot.command()
@logger.catch()
async def dollar_now(ctx):
    logger.debug(
        "Started dollar_now command. "
        f"[name={ctx.message.author.name};id={ctx.message.author.id};"
        f"channel_name={ctx.channel.name};channel_id={ctx.channel.id};"
        f"guild_name={ctx.guild.name};guild_id={ctx.guild.id}]"
    )

    fetch_exchange_routine()
    embed = get_dollar_embed()

    logger.debug("Ended dollar_now command.")
    await ctx.send(embed=embed)


@bot.command()
@logger.catch()
async def configure(ctx):
    logger.debug(
        "Started configure command. "
        f"[name={ctx.message.author.name};id={ctx.message.author.id};"
        f"channel_name={ctx.channel.name};channel_id={ctx.channel.id};"
        f"guild_name={ctx.guild.name};guild_id={ctx.guild.id}]"
    )
    data = {"channel": [ctx.channel.id]}

    add_table("channels", data)
    logger.info("Added table.")
    logger.debug("Ended configure command.")
    await ctx.send("Channel added.")


@tasks.loop(minutes=0.5)
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


if __name__ == "__main__":
    logger.debug("Started main")
    sub_list.start()
    bot.run(config["DISCORD_TOKEN"])
    logger.debug("Ended main")
