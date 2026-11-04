import asyncio
import atexit
import signal
import sys
import threading


class AsyncThread:
    __async_loop = None
    __async_thread = None

    def __init__(self):
        self.async_loop = asyncio.new_event_loop()

        self.async_thread = threading.Thread(
            target=self._run_async_loop,
            daemon=True
        )
        atexit.register(self._stop_async_loop)
        signal.signal(signal.SIGTERM, self._stop_async_loop)
        signal.signal(signal.SIGINT, self._stop_async_loop)

        self.async_thread.start()

    def _run_async_loop(self):
        asyncio.set_event_loop(self.async_loop)
        self.async_loop.run_forever()


    def _stop_async_loop(self, *args):
        self.async_loop.call_soon_threadsafe(
            self.async_loop.stop
        )
        self.async_thread.join(timeout=2)
        sys.exit(0)
