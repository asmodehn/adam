import asyncio
import threading


class BackgroundLoop(object):
    """
    Wrapping an asyncio.eventloop in order to execute it in the background.
    This makes running async code easy to manage, and make computation actually more visible, inside a context manager

    TODO :  doctest usage sample
    """

    def __init__(self, impl=None, debug=True):
        asyncio.set_event_loop(impl or asyncio.get_event_loop())
        self._loop = asyncio.get_event_loop()
        self._thd = None
        if debug:
            import logging
            import warnings
            # for debug
            self._loop.set_debug(True)
            logging.basicConfig(level=logging.DEBUG)
            warnings.filterwarnings("default", message='', category=Warning, module='', lineno=0, append=False)

    def _bgthread(self):
        try:
            return self._loop.run_forever()
        except Exception:
            raise
        finally:
            self._loop.close()

    def __enter__(self):
        # TODO : support using a superseeding eventloop if there is one... (probably monadic style instead of tree-style ?)
        self._thd = threading.Thread(target=self._bgthread, args=())
        self._thd.start()
        # returning our own wrapped eventloop instance
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._thd.join()
        # exception will be raised as long as we dont return true
        pass

    # delegate methods (careful : we are jumping between threads)
    def call_soon(self, callback, *args):
        self._loop.call_soon_threadsafe(callback, args)



# TODO : compose eventloop : a loop inside a loop ??
