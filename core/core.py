import os
import hikari
import arc
from ddginternal import search as ddg_search

bot = hikari.GatewayBot(os.environ["TOKEN"])
client = arc.GatewayClient(bot)

@client.include
@arc.slash_command("search", "Search something on DuckDuckGo")
async def search_command(ctx: arc.GatewayContext,
    question: arc.Option[str, arc.StrParams("The question to search.")],) -> None:
    result = await ddg_search(str(question))
    await ctx.respond(result)