from aiohttp import web
from models import *
from json.decoder import JSONDecodeError
import settings

router = web.RouteTableDef()


# USERS #

@router.get('/users')
async def get_users(request):
    users = {}
    for user in User.select():
        users[user.id] = user.name
    return web.json_response(users)


@router.get('/users/search/{name}')
async def search_users(request):
    users = {}
    name = request.match_info['name']
    for user in User.select().where(User.name.contains(name)):
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


@router.get('/users/{user_id}/search/{word}')
async def search_notes(request):
    user_id = request.match_info['user_id']
    word = request.match_info['word']
    try:
        user = User.get(id=user_id)
    except User.DoesNotExist:
        return web.HTTPNotFound(text='user not found')
    notes = {}
    for note in Note.select().where((Note.user == user) & (Note.text.contains(word))):
        notes[note.id] = note.text
    return web.json_response(notes)


@router.post('/users/')
async def create_user(request):
    try:
        data = await request.json()
    except JSONDecodeError:
        return web.HTTPBadRequest(text='bad data sent')
    try:
        uname = data['username']
    except KeyError:
        return web.HTTPBadRequest(text='no username in body')
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

# NOTES #


@router.get('/notes/{note_id}')
async def get_note(request):
    note_id = request.match_info['note_id']
    try:
        note = Note.get(id=note_id)
    except Note.DoesNotExist:
        return web.HTTPNotFound(text='note not found')
    return web.json_response({'id': note.id, 'text': note.text})


@router.post('/notes/')
async def create_note(request):
    try:
        data = await request.json()
    except JSONDecodeError:
        return web.HTTPBadRequest(text='bad data sent')
    try:
        uid = data['user_id']
    except KeyError:
        return web.HTTPBadRequest(text='no user id in data')
    try:
        text = data['text']
    except KeyError:
        return web.HTTPBadRequest(text='no note text in data')
    try:
        user = User.get(id=uid)
    except User.DoesNotExist:
        return web.HTTPBadRequest(text='this user does not exist')
    Note.create(user=user, text=text)
    return web.HTTPOk(text='note created')


@router.put('/notes/{note_id}')
async def update_note(request):
    try:
        data = await request.json()
    except JSONDecodeError:
        return web.HTTPBadRequest(text='bad data sent')
    try:
        text = data['text']
    except KeyError:
        return web.HTTPBadRequest(text='no note text in data')
    try:
        note_id = request.match_info['note_id']
        note = Note.get(id=note_id)
    except Note.DoesNotExist:
        return web.HTTPNotFound(text='not not found')
    note.text = text
    note.save()
    return web.HTTPOk(text='note updated')


@router.delete('/notes/{note_id}')
async def delete_note(request):
    note_id = request.match_info['note_id']
    Note.delete().where(Note.id == note_id).execute()
    return web.HTTPOk(text='note deleted')


try:
    host, port = settings.host, settings.port
except AttributeError:
    host, port = 'localhost', 8080

app = web.Application()
app.add_routes(routes=router)
web.run_app(app, host=host, port=port)
