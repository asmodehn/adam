#!/usr/bin/python3

import asyncio
import functools
import operator
import time

# decorators, used for imposing maximum call rate on (co)routines
# Point is to get a "control theory feeling" on top of corountines...


def rate(max_rate_hz=30):
    """
    TODO : description + doctest
    :param max_rate_hz:
    :return:
    """
    def decorator(coro):
        last_call = time.time()
        last_handle = None

        @functools.wraps(coro)
        async def maxrate_coro(*args):
            nonlocal last_call, last_handle

            loop = asyncio.get_event_loop()
            now = loop.time()

            if last_handle is not None:
                last_handle.cancel()

            async def wrapped_coro(*args):
                result = await coro(*args)
                last_handle = None
                return result

            future = asyncio.ensure_future(wrapped_coro(*args))
            loop.call_later(max(last_call + 1 / max_rate_hz, now), future)
            last_call = now

        return maxrate_coro

    return decorator



# operator declaring a coroutine monadic
# that is, ifscheduled once, and not run, and scheduled a second time, the first can be cancelled, and the param of the first call can be merged with the one of the second call
# Ex : If I schedule parse('my awesome string'), it is not run, and then I schedule parse ('bla bla'), aggregating both result is hte same as running parse('my awesome string bla bla')
# TODO : more theoritic study for this...


# IO to external world is through a monad -> we can aggregate our effects to keep control on the rate...
def rate_monadic_arg(max_rate_hz=30, monad_init="", monad_op=operator.concat):
    """TODO : description + doctest"""
    def decorator(coro):
        last_call = time.time()
        last_arg = monad_init
        last_handle = None

        @functools.wraps(coro)
        async def maxrate_monad_coro(arg):
            nonlocal last_arg, last_call, last_handle

            loop = asyncio.get_event_loop()
            now = loop.time()

            if last_handle is not None:
                last_handle.cancel()
                last_arg = monad_op(last_handle, arg)

            async def wrapped_coro(arg):
                await coro(arg)
                last_handle = None
                last_arg = monad_init

            last_handle = loop.call_later(wrapped_coro(arg), max(last_call + 1/max_rate_hz, now))

            last_call = now
        return maxrate_monad_coro

    return decorator


if __name__ == "__main__":
    import doctest
    doctest.testmod()

