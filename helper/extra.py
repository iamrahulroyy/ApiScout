import functools
import traceback
import logging
from typing import Callable, Coroutine, Any

logger = logging.getLogger(__name__)


def catch_async(func: Callable[..., Coroutine[Any, Any, Any]]):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            tb = traceback.format_exc()
            logger.error(f"[{func.__name__}] Exception occurred:\n{tb}")
            return None
    return wrapper
