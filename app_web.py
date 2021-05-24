from aiohttp import web
from models import *

router = web.RouteTableDef()


@router.get('/users')
async def get_users(request):
    users = {}
    for user in User.select():
        users[user.id] = user.name
    return web.json_response(users)


@router.get('/users/{user_id}')
async def get_notes(request):
    user_id = request.match_info['user_id']
    try:
        user = User.get(id=user_id)
    except User.DoesNotExist:
        return web.HTTPNotFound()
    notes = {}
    for note in user.notes:
        notes[note.id] = note.text
    return web.json_response(notes)


@router.get('/notes/{note_id}')
async def get_note(request):
    note_id = request.match_info['note_id']
    try:
        note = Note.get(id=note_id)
    except Note.DoesNotExist:
        return web.HTTPNotFound()
    return web.json_response({'id': note.id, 'text': note.text})


app = web.Application()
app.add_routes(routes=router)
web.run_app(app, host='localhost')
