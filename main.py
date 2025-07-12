import asyncio
import json
import websockets
from websockets import ServerConnection

from session import push_request


def is_valid(code: str) -> bool:
    return code.isdigit()


async def main(conn: ServerConnection):
    while True:
        data = await conn.recv()
        res: any
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

        await conn.send(json.dumps(push_request(code)))


async def start_server():
    # Start the WebSocket server
    server = await websockets.serve(main, 'localhost', 8765)
    await server.wait_closed()


if __name__ == '__main__':
    asyncio.run(start_server())

# jmcomic.download_album('422866')
