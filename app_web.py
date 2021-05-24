from aiohttp import web
from models import *

router = web.RouteTableDef()


@router.get('/users/')
async def get_users(request):
    ...


app = web.Application()
app.add_routes(routes=router)
web.run_app(app)
