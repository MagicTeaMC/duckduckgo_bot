import os
import hikari
import arc
from ddginternal import search as ddg_search

bot = hikari.GatewayBot(os.environ["TOKEN"])
client = arc.GatewayClient(bot)

@client.include
@arc.slash_command("search", "Search something on DuckDuckGo")
async def search_command(ctx: arc.GatewayContext,
    question: arc.Option[str, arc.StrParams("The question to search.")],) -> None: # type: ignore
    
    results = ddg_search(str(question)).web[:3]
    
    embed = hikari.Embed(
        title=f"Search results for: {question}",
        description="Here are the top 3 results:",
        color=hikari.Color(0x1D4ED8)
    )
    
    for result in results:
        embed.add_field(
            name=f"{result.title} - {result.url}",
            value=f"{result.description.strip()}",
            inline=False
        )
    
    await ctx.respond(embed=embed)