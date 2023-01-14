import discord

from discord_dollar.configure.log import get_logger
from discord_dollar.repository.adapter import get_table

logger = get_logger()


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
