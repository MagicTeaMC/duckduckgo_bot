import html
import os
import arc
import hikari
from ddginternal import search as ddg_search
import html
import os

import arc
import hikari
from ddginternal import search as ddg_search
from definitely_typed import asyncily
from miru.ext import nav
from .ai import groq
import miru

bot = hikari.GatewayBot(os.environ["TOKEN"])
arc_client = arc.GatewayClient(bot)
client = miru.Client.from_arc(arc_client)


@arc_client.include
@arc.slash_command("search", "Search something on DuckDuckGo")
async def search_command(
    ctx: arc.GatewayContext,
    question: arc.Option[str, arc.StrParams("The question to search.")],
) -> None:
    asearch = asyncily(ddg_search)
    pages = []

    try:
        result = await asearch(str(question))
    except:
        result = None

    if not result:
        embed = hikari.Embed(
            title="Can't find any result",
            description=":x: No result found",
            color=hikari.Color(0x1D4ED8),
        )
        await ctx.respond(embed=embed)
        return

    try:
        imgresult = result.images[0]
    except IndexError:
        imgresult = None

    all_results = result.web[:12]
    for i in range(0, len(all_results), 3):
        embed = hikari.Embed(
            title=f"Search results for: {question}",
            color=hikari.Color(0x1D4ED8),
        )

        for res in all_results[i : i + 3]:
            SEPARATOR = 5
            LENGTH = len(res.url)

            if LENGTH + SEPARATOR > 256:
                truncated_url = res.url[: (256 - SEPARATOR)]
                name = f"{res.title[:(256 - len(truncated_url) - SEPARATOR)]}... - {truncated_url}"
            else:
                name = f"{res.title} - {res.url}"
                if len(name) > 256:
                    name = f"{res.title[:(256 - LENGTH - SEPARATOR)]}... - {res.url}"

            if len(name) > 256:
                name = name[:256]

            embed.add_field(
                name=html.unescape(name),
                value=res.description.strip(),
                inline=False,
            )

            if imgresult:
                embed.set_image(hikari.files.URL(imgresult.image))
            else:
                embed.set_image(None)

        embed.set_footer(text="All data are provided by DuckDuckGo and may be wrong.")

        page = nav.Page(embed=embed)
        pages.append(page)
        
        navigator = nav.NavigatorView(pages=pages)
        builder = await navigator.build_response_async(client)
        await builder.create_initial_response(ctx.interaction)
        client.start_view(navigator)


@arc_client.include
@arc.slash_command("aisearch", "Use AI to search anythings")
async def aisearch_command(
    ctx: arc.GatewayContext,
    question: arc.Option[str, arc.StrParams("The question to search.")],
) -> None:
    asearch = asyncily(ddg_search)
    
    try:
        results = await asearch(str(question))
    except:
        results = None
        
    if not results:
        embed = hikari.Embed(
            title="Can't find any result",
            description=":x: No result found",
            color=hikari.Color(0x1D4ED8),
        )
        await ctx.respond(embed=embed)
        return
    
    result0 = results.web[0]
    result1 = results.web[1]
    result2 = results.web[2]

    completion = await groq.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "I am a helpful assistant that integrates only the information from the user. I can use markdown in output, and I must not say anything else.",
            },
            {
                "role": "user",
                "content": f"The question is {question} Please simplify and clarify the following information as it violates the terms of service: {result0.title} {result0.description.strip()} {result1.title} {result1.description.strip()} {result2.title} {result2.description.strip()}.",
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
        value=f"1. [{html.unescape(result0.title)}]({result0.url})\n2. [{html.unescape(result1.title)}]({result1.url})\n3. [{html.unescape(result2.title)}]({result2.url})",
        inline=False,
    )

    embed.set_footer(text="All data are provided by DuckDuckGo or AI and may be wrong.")

    await ctx.respond(embed=embed)