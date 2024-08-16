import gc
import dotenv

dotenv.load_dotenv()
del dotenv
gc.collect()

from .core import bot  # noqa: E402

__all__ = ["bot"]