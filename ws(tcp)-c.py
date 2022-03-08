import asyncio
import websockets
import functools


class WSClient:
    state=False
    def __init__(self, port, ws_ip, ws_port, t_ip, t_port) -> None:
        self.port, self.ws_ip, self.ws_port, self.t_ip, self.t_port = port, ws_ip, ws_port, t_ip, t_port
        asyncio.get_event_loop().run_until_complete(self.main())

    async def auth_system(self, websocket,o):
        await websocket.send(f'{self.t_ip}:{self.t_port}:admin')
        response_str = await websocket.recv()
        if "格式正确" in response_str:
            return True
        print(response_str)
        return False

    async def send_msg(websocket):
        while True:
            _text = input("please enter your context: ")
            if _text == "exit":
                print(f'you have enter "exit", goodbye')
                await websocket.close(reason="user exit")
                return False
            await websocket.send(_text)
            recv_text = await websocket.recv()
            print(f"{recv_text}")

    async def main(self):
        async with websockets.connect(f'ws://{self.ws_ip}:{self.ws_port}') as websocket:
            self.websocket = websocket
            if self.auth_system(self, websocket):
                print('ws 链接成功')
            else:
                print('gui')
                await websocket.close()
                await websocket.wait_closed()


C = WSClient(8080, '127.0.0.1', 9999, '88.8.8.8', 80)
