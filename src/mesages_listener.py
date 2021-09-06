import asyncio


async def handle_service_message(reader: asyncio.StreamReader,
                                 writer: asyncio.StreamWriter) -> None:
    data = (await reader.read(65_536)).decode('utf-8')
    print(f"Msg received, processing: {data}")

    writer.write(b"Msg processed")
    await writer.drain()

    writer.close()


async def socket_listener():
    server = await asyncio.start_server(
        handle_service_message, '127.0.0.1', 2025)

    async with server:
        await server.serve_forever()
