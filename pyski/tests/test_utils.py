import asyncio

from ..utils import rate

# Testing corountines utils
# TODO :
# 1) sample tests
# 2) pathological tests
# 3) property based testing - hypothesis
# 4) transfer sample tests to doctests



# 1




def test_coro_rate():

    import logging
    import warnings

    event_loop = asyncio.get_event_loop()

    # for debug
    event_loop.set_debug(True)
    logging.basicConfig(level=logging.DEBUG)
    warnings.filterwarnings("default", message='', category=Warning, module='', lineno=0, append=False)

    #
    start_time = event_loop.time()

    # define a global var to store the call frequency

    # keeping data to help compute frequency
    calls = 0
    last_time = 0

    # define a corountine

    @rate(60)
    async def mycoro(any=42, thing="fortytwo"):
        nonlocal calls, last_time

        l = asyncio.get_event_loop()
        t = l.time() - start_time
        calls += 1
        last_time = t

    # schedule a bunch of calls in sequence
    task = [mycoro(a, t) for a, t in zip(
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26],
            ["a", "b", "c", "d", "e", "f", "g", "h", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        )]

    # like gather but in sequence...
    async def seq(*tasks):
        freq = 0
        for res in asyncio.as_completed(tasks):
            await res
            freq = calls / last_time
            print(freq)
        return freq


    try:
        return_value = event_loop.run_until_complete(seq(*task))

    finally:
        event_loop.close()


# 2 TODO

def test_ro_rate():
    pass