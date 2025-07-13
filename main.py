import asyncio
import json
import websockets
from websockets import ServerConnection, ConnectionClosedOK

from session import push_request

host = "localhost"
port = 24357


def is_valid(code: str) -> bool:
    return code.isdigit()


async def main(conn: ServerConnection):
    print("客户端已连接")
    while True:
        try:
            data = await conn.recv()
        except ConnectionClosedOK:
            break
        try:
            res = json.loads(data)
        except json.decoder.JSONDecodeError:
            continue

        if not isinstance(res, dict):
            continue

        if not ("id" in res):
            continue

        code = res["id"]

        if not isinstance(code, str):
            continue

        response = push_request(code)

        response["SIGNAL"] = "RESPONSE"

        await conn.send(json.dumps(response))


async def start_server():
    # Start the WebSocket server
    server = await websockets.serve(main, host, port)
    print("服务已启动")
    await server.wait_closed()


if __name__ == '__main__':
    asyncio.run(start_server())

# jmcomic.download_album('422866')
