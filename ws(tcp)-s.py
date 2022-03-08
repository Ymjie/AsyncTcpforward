import asyncio
import websockets
import functools


class WSServer:
    def __init__(self, ip, port) -> None:
        self.ip, self.port = ip, port
        self.start_server = websockets.serve(functools.partial(
            self.main_logic,other_param='66'),self.ip, self.port)

        asyncio.get_event_loop().run_until_complete(self.start_server)
        asyncio.get_event_loop().run_forever()
        print('结束')

    async def main_logic(self, websocket,other_param):
        await self.get_connect_target(self,websocket)
        task = [
            self.recv_msg(websocket, other_param),
            self.send_msg(websocket, other_param)
        ]
        await asyncio.gather(*task)
        # await self.get_connect_target(websocket)

    async def get_connect_target(self,o,websocket):
        print(self,websocket)
        while True:
            recv_str = await websocket.recv()
            try:
                self.t_ip, self.t_port, self.ws_passwd = * \
                    recv_str.split(":"),  # t_ip,t_port,ws_passwd
                if self.ws_passwd == "admin" and (self.t_port and self.t_ip) is not None:
                    await websocket.send('格式正确')
                    return True
                else:
                    response_str = "sorry,wrong data, please submit again"
                    await websocket.send(response_str)
            except ValueError:
                await websocket.send('sorry,wrong data, please submit again')



    @staticmethod
    async def recv_msg(websocket, other_param):
        while True:
            recv_text = await websocket.recv()
            print(recv_text)

    @staticmethod
    async def send_msg(websocket, other_param):
        while True:
            await asyncio.sleep(1)
            await websocket.send(other_param)


A = WSServer('127.0.0.1', 9999)
