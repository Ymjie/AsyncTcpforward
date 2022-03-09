import asyncio
from sqlite3 import connect
from WSClient import *
import hashlib
from WsConnectPoll import *


class AC:
    def __init__(self, TCP_reader, TCP_writer, WS) -> None:
        self.TCP_reader = TCP_reader
        self.TCP_writer = TCP_writer
        self.ws = WS


class TCP2WS(AC):
    async def translate(self, data):
        await self.ws.send_data(data)
# 触发器1：TCP请求
# 触发器2：WS的返回


class TCPserver:
    WSstats = False

    def __init__(self, ip, port, WSClient) -> None:
        print('开始创建')
        loop = asyncio.get_event_loop()
        self.ip, self.port = ip, port
        self.ws = WSClient
        print('开启协程任务')
        loop.create_task(WSClient.main())
        loop.create_task(self.ws_data_divert())
        self.wcpoll = WsConnectPoll()
        print('开始创建')
        crt = asyncio.start_server(self.handle, ip, port, loop=loop)
        try:
            server = loop.run_until_complete(crt)
            print(server)
            # loop.run_until_complete(server.wait_closed())
            loop.run_forever()
        except (asyncio.CancelledError, KeyboardInterrupt):
            print('Tasks has been canceled')
        finally:
            server.close()
            loop.close()

    async def handle(self, reader, writer):
        client = writer.get_extra_info('peername')  # 获取客户的信息
        flag = ':'.join(map(str, (client)))
        md5 = hashlib.md5()
        md5.update(flag.encode())
        flag = md5.hexdigest().encode()
        self.wcpoll.add(flag, [reader, writer])
        tcp2ws = TCP2WS(reader, writer, self.ws)
        while True:
            if writer.is_closing():
                if self.wcpoll.is_set(flag):
                    del self.wcpoll._poll[flag]
                return
            data = await reader.read(1024)
            if not data: 
                if not writer.is_closing():
                    writer.close()
                    print('TCP_handle-关闭连接')
                    await writer.wait_closed()
                    if self.wcpoll.is_set(flag):
                        del self.wcpoll._poll[flag]
                return
            data = flag + data
            await tcp2ws.translate(data)

    async def ws_data_divert(self):
        while True:
            if self.ws.stats == False:
                await asyncio.sleep(1)
                continue
            try:
                data = await self.ws.recv_data()
            except websockets.exceptions.ConnectionClosedError:
                print('ws连接断开')
                # await self.ws.close()
                # await self.ws.wait_closed()
            flag = data[:32]
            data = data[32:]
            # print(self.wcpoll._poll)
            if self.wcpoll.is_set(flag):
                reader, writer = *self.wcpoll.get(flag),
            else:
                print('ws服务器发来了一个鬼鬼数据')
                continue
            if isinstance(data, str):
                data = data.encode()
            if isinstance(flag, str):
                flag = flag.encode()
            writer.write(data)
            if writer.is_closing():
                if self.wcpoll.is_set(flag):
                    del self.wcpoll._poll[flag]
                continue
            await writer.drain()

    async def auth_system(self, websocket):
        await websocket.send(f'{self.t_ip}:{self.t_port}:admin')
        response_str = await websocket.recv()
        if "格式正确" in response_str:
            return True
        print(response_str)
        return False


if __name__ == '__main__':
    WSClient = WSClient('127.0.0.1', 45001)
    print('a')
    A = TCPserver('127.0.0.1', 8888, WSClient)
