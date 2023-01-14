import discord

import pandas as pd

from discord_dollar.log import logger
from discord_dollar.repository.adapter import get_table


@logger.catch()
def create_dollar_embed(latest: pd.DataFrame):
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
