import asyncio

async def handle(reader, writer): 
    try:
        target_r, target_w = await asyncio.open_connection('127.0.0.1', 5201)
    except ConnectionRefusedError:
        print('远程计算机连接失败！')
    print('new connect！')
    task = [
        tcp_reader_Tg(reader,writer,target_r,target_w),
        tcp_writer_Tg(reader,writer,target_r,target_w)
    ]
    await asyncio.gather(*task)
async def tcp_reader_Tg(reader,writer,target_r,target_w):
    while True:
        try:
            data = await reader.read(1024)
            if not data: 
                if not writer.is_closing():
                    writer.close()
                    print('关闭连接')
                    await writer.wait_closed()
                break
        except:
            break
        
        # client = writer.get_extra_info('peername') 
        target_w.write(data) 
        try:
            if target_w.is_closing():
                print('已经关闭')
                break
            await target_w.drain()
        except:
            print('ConnectionResetError')
            break
    print('tcp发送机 done')
async def tcp_writer_Tg(reader,writer,target_r,target_w):
    while True:
        try:
            data = await target_r.read(1024)
            if not data: 
                if not writer.is_closing():
                    target_w.close()
                    print('关闭连接')
                    await target_w.wait_closed()
                break
        except:
            break
        # client = target_w.get_extra_info('peername') 
        writer.write(data)
        try:
            if writer.is_closing():
                print('已经关闭')
                break
            await writer.drain()
        except:
            print('err')
            break      
    print('tcp接收机 done')
loop = asyncio.get_event_loop()
ip = '127.0.0.1'
port = 9999
crt = asyncio.start_server(handle, ip, port, loop=loop) 
try:
    server = loop.run_until_complete(crt)
    print(server)
    # loop.run_until_complete(server.wait_closed())
    loop.run_forever()
except (asyncio.CancelledError,KeyboardInterrupt):
    print('Tasks has been canceled')
finally:
    server.close()
    loop.close()
