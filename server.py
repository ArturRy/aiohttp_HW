import json

from aiohttp import web


from models import Session, Advert, engine, init_orm

app = web.Application()


@web.middleware
async def session_middleware(request, handler):
    async with Session() as session:
        request.session = session
        response = await handler(request)
        return response


async def orm_context(app):
    print("START")
    await init_orm()
    yield
    await engine.dispose()
    print("FINISH")


app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)


def get_error(error_class, message):
    return error_class(
        text=json.dumps({"error": message}), content_type="application/json"
    )


async def get_advert_by_id(session, advert_id):
    advert = await session.get(Advert, advert_id)
    if advert is None:
        raise get_error(web.HTTPNotFound, f"Advert with id {advert_id} not found")
    return advert


async def add_advert(session, advert):

    session.add(advert)
    await session.commit()
    return advert.id


class AdvertView(web.View):

    @property
    def advert_id(self):
        return int(self.request.match_info["advert_id"])

    @property
    def session(self) -> Session:
        return self.request.session

    async def get_advert(self):
        user = await get_advert_by_id(self.session, self.advert_id)
        return user

    async def get(self):
        advert = await self.get_advert()
        return web.json_response(advert.dict)

    async def post(self):
        advert_data = await self.request.json()

        advert = Advert(**advert_data)
        await add_advert(self.session, advert)

        return web.json_response({"id": advert.id})

    async def patch(self):
        advert_data = await self.request.json()
        advert = await self.get_advert()
        for key, value in advert_data.items():
            setattr(advert, key, value)
        await add_advert(self.session, advert)
        return web.json_response({"id": advert.id})

    async def delete(self):
        advert = await self.get_advert()
        await self.session.delete(advert)
        await self.session.commit()
        return web.json_response({"status": "deleted"})


app.add_routes(
    [
        web.get("/adverts/{advert_id:\d+}", AdvertView),
        web.patch("/adverts/{advert_id:\d+}", AdvertView),
        web.delete("/adverts/{advert_id:\d+}", AdvertView),
        web.post("/adverts", AdvertView),
    ]
)

web.run_app(app)
