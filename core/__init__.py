import gc

import dotenv

dotenv.load_dotenv()
del dotenv
gc.collect()

from core import ai, core
from core.ai import (
    groq,
)
from core.core import (
    aisearch_command,
    arc_client,
    asearch,
    bot,
    client,
    search_command,
)

__all__ = [
    "ai",
    "aisearch_command",
    "arc_client",
    "asearch",
    "bot",
    "client",
    "core",
    "groq",
    "search_command",
]
