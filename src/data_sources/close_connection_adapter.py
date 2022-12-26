import asyncio


class CloseConnectionAdapter:

    def __init__(self, connection):
        self._connection = connection

    async def _close(self):
        await self._connection.close()

    def execute(self):
        asyncio.run(self._close())
