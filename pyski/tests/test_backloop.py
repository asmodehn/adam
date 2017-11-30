import asyncio

from ..backloop import BackgroundLoop



def test_bgloop():

    def task1():
        print("task1")

    def task2(arg):
        print("task2")

    def task3(arg):
        print("task3")
        return 42

    async def coro1():
        print("coro1")

    async def coro2(arg):
        print("coro2")

    async def corores():
        return 42

    async def coro3(arg):
        print("coro3")
        res = await corores()
        print("returning...")
        return res

    with BackgroundLoop() as bgl:
        bgl.call_soon(task1)
        bgl.call_soon(task2, 42)
        res3 = bgl.call_soon(task3, 42)
        assert res3 == 42

        bgl.call_soon(coro1)
        bgl.call_soon(coro2, 42)
        cores3 = bgl.call_soon(coro3, 42)
        assert cores3 == 42

if __name__ == '__main__':
    import pytest
    pytest.main(['-s'])
