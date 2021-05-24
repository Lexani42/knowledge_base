from aiohttp import web
from models import *

router = web.RouteTableDef()


@router.get('/users/')
async def get_users(request):
    users = {}
    for user in User.select():
        users[user.id] = user.name
    return web.json_response(users)


app = web.Application()
app.add_routes(routes=router)
web.run_app(app, host='localhost')
