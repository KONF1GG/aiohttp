from aiohttp import web

app = web.Application()

async def orm_context(app: web.Application):
    print('START')
    yield
    print('END')

app.cleanup_ctx.append(orm_context)
async def hello_world(request: web.Request):
    some_id = request.match_info["some_id"]
    json_data = await request.json()
    headers = request.headers
    qs = request.query
    print(f'{some_id=}')
    print(f'{json_data=}')
    print(f'{headers=}')
    print(f'{qs=}')
    http_response = web.json_response({"hello": "world"})
    return http_response

app.add_routes([
    web.post("/hello/world/{some_id:\d+}", hello_world)
])

web.run_app(app)