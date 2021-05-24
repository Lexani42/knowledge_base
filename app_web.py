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
        return web.HTTPNotFound(text='user not found')
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
        return web.HTTPNotFound(text='note not found')
    return web.json_response({'id': note.id, 'text': note.text})


@router.post('/users/')
async def create_user(request):
    data = await request.json()
    try:
        uname = data['username']
    except KeyError:
        return web.HTTPBadRequest()
    try:
        User.create(name=uname)
        return web.HTTPOk(text='user created')
    except IntegrityError:
        return web.HTTPBadRequest(text='user is already exists')


@router.delete('/users/{user_id}')
async def delete_user(request):
    user_id = request.match_info['user_id']
    User.delete().where(User.id == user_id).execute()
    return web.HTTPOk(text='user deleted')


app = web.Application()
app.add_routes(routes=router)
web.run_app(app, host='localhost')
