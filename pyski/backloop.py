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
            self._loop.run_forever()
        except Exception:
            # finishing scheduled tasks
            pending = asyncio.Task.all_tasks()
            self._loop.run_until_complete(asyncio.gather(*pending))
            raise
        finally:
            if hasattr(self._loop, 'shutdown_asyncgens'):  # py3.6
                self._loop.run_until_complete(self._loop.shutdown_asyncgens())
            self._loop.close()
        # cannot return directly...

    def __enter__(self):
        # TODO : support using a superseeding eventloop if there is one... (probably monadic style - we have limited cpus anyway - instead of tree-style - with max checked ?)
        self._thd = threading.Thread(target=self._bgthread, args=())
        self._thd.start()
        # returning our own wrapped eventloop instance
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:  # exception caught
            # making exception visible before tripping on async loops
            print("Exception caught in BackgroundLoop : {exc_type} : {exc_val}\nTraceback: {exc_tb}".format(**locals()))

        self._loop.stop()
        # self._loop.close()
        self._thd.join()
        # exception will be raised as long as we dont return true
        return

    # delegate methods (careful : we are jumping between threads)
    # note at this point we already have all arguments,
    # to have runtime equivalence - bisimulation - of corountine and routine calls
    def call_soon(self, callback, *args):
        if asyncio.iscoroutinefunction(callback):
            future = asyncio.run_coroutine_threadsafe(callback(*args), self._loop)
            return future
        else:
            # TODO : a better way : result is lost here, and no point to put up with a whole big thread machinery when we have coroutines...
            handle = self._loop.call_soon_threadsafe(callback, *args)
            return handle



# TODO : compose eventloop : a loop inside a loop ??
