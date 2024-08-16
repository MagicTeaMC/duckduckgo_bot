import os
import hikari
import arc
from ddginternal import search

bot = hikari.GatewayBot(os.environ["TOKEN"])
client = arc.GatewayClient(bot)

@client.include
@arc.slash_command("search", "Search something on DuckDuckGo")
async def search(ctx: arc.GatewayContext,
    question: arc.Option[str, arc.StrParams("The question to search.")],) -> None:
    await ctx.respond(await search(question).web[0])