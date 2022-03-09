import asyncio
import websockets
class WSClient:

    def __init__(self, ip, port,*params) -> None:
        self.params=params
        self.ip, self.port = ip, port
        # asyncio.get_event_loop().run_until_complete(self.main())
        # asyncio.get_event_loop().run_forever()

    async def main(self):
        self.stats=False
        async for websocket in websockets.connect(f'ws://{self.ip}:{self.port}'):
            try:
                print('连接')
                self.ws = websocket
                self.stats=True
                await self.ws.wait_closed()
                self.stats=False
            except websockets.ConnectionClosed:
                self.stats=False
                print('重连')
                continue
        self.stats=False
    async def recv_data(self):
            recv_text = await self.ws.recv()
            return recv_text

    async def send_data(self,data):
        await self.ws.send(data)
if __name__ == '__main__':
    C = WSClient('127.0.0.1',9999, 'S:')
