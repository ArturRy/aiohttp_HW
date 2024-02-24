import asyncio

import aiohttp


async def main():
    client = aiohttp.ClientSession()

    # response = await client.post(
    #     "http://127.0.0.1:8080/adverts",
    #     json={'title': 'some_advert2',
    #           'description': 'description',
    #           'owner': 'owner'},
    # )
    #
    # print(response.status)
    # print(await response.json())

    # response = await client.get(
    #     "http://127.0.0.1:8080/adverts/3",
    # )
    # print(response.status)
    # print(await response.json())

    # response = await client.patch(
    #     "http://127.0.0.1:8080/adverts/1",
    #     json={"title": "new_advert"},
    # )
    # print(response.status)
    # print(await response.json())

    # response = await client.get(
    #     "http://127.0.0.1:8080/adverts/1"
    # )
    # print(response.status)
    # print(await response.json())

    # response = await client.delete(
    #     "http://127.0.0.1:8080/adverts/1",
    # )
    # print(response.status)
    # print(await response.json())
    #
    # response = await client.get(
    #     "http://127.0.0.1:8080/adverts/1",
    # )
    # print(response.status)
    # print(await response.json())
    await client.close()


asyncio.run(main())
