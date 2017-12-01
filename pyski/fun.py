# representing a function in python code

import functools
import asyncio

# implementing basic functions (category theory style)

# TODO : depend on combinator logic... maybe after one or two reifications...







# TODO : different caching/memoizing algorithms, with added capabilities to detect deviation (actual and cached result are different)

# https://en.wikipedia.org/wiki/Cache_replacement_policies

# Since functions can be composed, cache access should also compose, somehow ??
# We eventually need to fit somewhere in there : https://en.wikipedia.org/wiki/Consistency_model

@functools.lru_cache()

# TODO : lru_cache_error_check : detect error by result deviation from cache... (ZAP)

def zap():
    def decorator(zap_wrapped):
        # zap stats storage following lru_cache design

        inconsistencies = 0
        cache_time = 0
        actual_time = 0

        async def zap_wrapper(*args, **kwargs):

            start_time = asyncio.get_event_loop().time()

            # TODO : determine faster call (or assume it is the cache by definition ?)
            # or maybe dynamically progressively reduce cache complexity cost if actual call is cheap and consistent ?
            fastest = zap_wrapped(*args, **kwargs)

            # We wait, as we assume the loop is already running, we have to be in async await code...
            fast_result = await fastest

            cache_time = asyncio.get_event_loop().time() - start_time

            if hasattr(zap_wrapped, '__wrapped__'):  # memoized (functools.lru_cache likely)
                actual_future = asyncio.ensure_future(zap_wrapped.__wrapped__(*args, **kwargs))

                def zap(future):
                    nonlocal inconsistencies
                    # future should be already done when callback is called
                    r = future.result()
                    actual_time = asyncio.get_event_loop().time() - start_time
                    if r != fast_result:
                        # ERROR detected !!!
                        inconsistencies += 1

                # TODO : we need to keep processing extra result when we have free time...
                #  We cannot do it "in background" without adding extra complexity.
                #  Note : nested event loops are not supported
                # This seems to be the better option
                actual_future.add_done_callback(zap)




            running.add_done_callback()

            return fast_result

        def zap_info():
            """Report zap statistics"""
            with lock:
                return _CacheInfo(hits, misses, maxsize, len(cache))

        def zap_clear():
            """Clear the cache and cache statistics"""
            nonlocal hits, misses, full
            with lock:
                cache.clear()
                root[:] = [root, root, None, None]
                hits = misses = 0
                full = False

        zap_wrapper.zap_info = zap_info
        zap_wrapper.zap_clear = zap_clear
        return zap_wrapper

    return decorator



# goal :

@zap_lru()
def add2(x):
    return x + 2

# actually does https://stackoverflow.com/questions/31900244/select-first-result-from-two-coroutines-in-asyncio

def add2_zap(x, loop):
    task = asyncio.gather([
        add2(x),
        cached(add2, x)

    ])


# Note : it seems at low level, the loop is the same as a continuation : run once, get one result, stop.
