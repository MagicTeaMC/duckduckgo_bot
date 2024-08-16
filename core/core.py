import os
import hikari
import arc
from ddginternal import search as ddg_search
from definitely_typed import asyncily

bot = hikari.GatewayBot(os.environ["TOKEN"])
client = arc.GatewayClient(bot)

@client.include
@arc.slash_command("search", "Search something on DuckDuckGo")
async def search_command(ctx: arc.GatewayContext,
    question: arc.Option[str, arc.StrParams("The question to search.")],) -> None: # type: ignore
    
    asearch = asyncily(ddg_search)
    
    embed = hikari.Embed(
        title=f"Search results for: {question}",
        description="Here are the top 3 results:",
        color=hikari.Color(0x1D4ED8)
    )
    
    for result in (await asearch(str(question))).web[:3]:
        # Ensure the name is 256 characters or fewer
        name = f"{result.title} - {result.url}"
        if len(name) > 255:
            name = f"{result.title[:255 - len(result.url) - 4]}... - {result.url}"
        
        embed.add_field(
            name=name,
            value=f"{result.description.strip()}",
            inline=False
        )
    
    await ctx.respond(embed=embed)