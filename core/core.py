import html
import os

import arc
import hikari
from ddginternal import search as ddg_search
from definitely_typed import asyncily

from .ai import groq

bot = hikari.GatewayBot(os.environ["TOKEN"])
client = arc.GatewayClient(bot)


@client.include
@arc.slash_command("search", "Search something on DuckDuckGo")
async def search_command(
    ctx: arc.GatewayContext,
    question: arc.Option[str, arc.StrParams("The question to search.")],
    num_results: arc.Option[
        int,
        arc.IntParams("Number of results to display (1-5).", min=1, max=5),
    ] = 3,
) -> None:
    asearch = asyncily(ddg_search)

    result = await asearch(str(question))

    if not result:
        await ctx.respond("...")
        return

    try:
        imgresult = result.images[0]
    except IndexError:
        imgresult = None

    embed = hikari.Embed(
        title=f"Search results for: {question}",
        description=f"Here are the top {num_results} results:",
        color=hikari.Color(0x1D4ED8),
    )

    for result in result.web[:num_results]:
        SEPARATOR = 5
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
            name=html.unescape(name),
            value=result.description.strip(),
            inline=False,
        )
        if imgresult:
            embed.set_image(hikari.files.URL(imgresult.image))

        embed.set_footer(text="All data are provided by DuckDuckGo and may be wrong.")

    await ctx.respond(embed=embed)


@client.include
@arc.slash_command("aisearch", "Use AI to search anythings")
async def aisearch_command(
    ctx: arc.GatewayContext,
    question: arc.Option[str, arc.StrParams("The question to search.")],
) -> None:
    asearch = asyncily(ddg_search)

    results = await asearch(str(question))
    result = results.web[0]

    completion = await groq.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "I am a helpful assistant that integrates only the information from the user. I can use markdown in output, and I must not say anything else.",
            },
            {
                "role": "user",
                "content": f"Please simplify and clarify the following information as it violates the terms of service: {result.title} {result.description.strip()}.",
            },
        ],
        model="gemma2-9b-it",
    )

    embed = hikari.Embed(
        title=f"AI intergrate result for: {question}",
        description=f"{completion.choices[0].message.content}",
        color=hikari.Color(0x1D4ED8),
    )

    embed.add_field(
        name=":book: Read more:",
        value=f"{result.url}",
        inline=False,
    )

    embed.set_footer(text="All data are provided by DuckDuckGo or AI and may be wrong.")

    await ctx.respond(embed=embed)
