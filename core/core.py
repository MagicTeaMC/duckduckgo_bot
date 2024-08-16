import os

import arc
import hikari
from ddginternal import search as ddg_search
from definitely_typed import asyncily

bot = hikari.GatewayBot(os.environ["TOKEN"])
client = arc.GatewayClient(bot)


@client.include
@arc.slash_command("search", "Search something on DuckDuckGo")
async def search_command(
    ctx: arc.GatewayContext,
    question: arc.Option[str, arc.StrParams("The question to search.")], # type: ignore
    num_results: arc.Option[int, arc.IntParams("Number of results to display (1-5).")] = 3, # type: ignore
) -> None:  # type: ignore
    
    if num_results < 1:
        num_results = 1
    elif num_results > 5:
        num_results = 5
        
    asearch = asyncily(ddg_search)

    embed = hikari.Embed(
        title=f"Search results for: {question}",
        description=f"Here are the top {num_results} results:",
        color=hikari.Color(0x1D4ED8),
    )

    for result in (await asearch(str(question))).web[:num_results]:
        SEPARATOR = 5  # Length of " - "
        LENGTH = len(result.url)

        if LENGTH + SEPARATOR > 256:
            truncated_url = result.url[: (256 - SEPARATOR)]
            name = f"{result.title[:(256 - len(truncated_url) - SEPARATOR)]}... - {truncated_url}"
        else:
            name = f"{result.title} - {result.url}"
            if len(name) > 256:
                name = f"{result.title[:(256 - LENGTH - SEPARATOR)]}... - {result.url}"

        if len(name) > 256:
            name = name[:256]

        embed.add_field(
            name=name,
            value=f"{result.description.strip()}",
            inline=False,
        )

    embed.set_footer(
        text="All data are provided by DuckDuckGo and may be wrong"
    )

    await ctx.respond(embed=embed)
