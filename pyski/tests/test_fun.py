

# Testing functional implementation
# TODO :
# 1) sample tests
# 2) pathological tests
# 3) property based testing - hypothesis
# 4) transfer sample tests to doctests

# 1

#
import functools

import time


from ..fun import zap

# SLOW Routine
@zap()
@functools.lru_cache()
def add16(val):
    time.sleep(20)
    return 16 + val

# FAST Routine


# SLOW Corountine


# FAST Coroutine




# 2


# no caching
@zap()
def add16(val):
    time.sleep(20)
    return 16 + val



# no caching coro
@zap()
async def add16(val):
    time.sleep(20)
    return 16 + val





















if __name__ == '__main__':
    import pytest
    pytest.main(['-s'])
