# knowledge_base

this is a knowledge base with integrated telegram interface and web API. create for personal needs, so there isn't account management

## getting started
1. install all the requirements
```
pip install -r req.txt
```
2. init database
```
python init.py
```
3. create settings.py file with the following structure:
```
token='your token from @BotFather'
```
4. start telegram bot
```
python app_tg.py
```
5. start web api
```
python app_web.py
```
by default web api starts on localhost:8080. if you want to change this parameters, in your settings file create variables:
```
host=your host
port=your port
```

## web api docs
### GET `/users`

response:
```
{
  id1: name1,
  id2: name2,
  id3: name3
}
```

### GET `/users/{user_id}`

get user notes

response:
```
{
  note_id1: text1,
  note_id2: text2,
  note_id3: text3
}
```

`404 user not found` - user does not exist

### GET `/users/{user_id}/search/{word}`

search in user notes by word

response:
```
{
  note_id1: text1,
  note_id2: text2,
  note_id3: text3
}
```

`404 user not found` - user does not exist

### POST `/users/`

creates new user

body:
```
{
  "username": username
}
```

response:

`200 OK` - user created

`400 bad data sent` - server can't decode your data

`400 no username in body` - no username in request body

`400 user is already exists` - user is already exists

### DELETE `/users/{user_id}`

deletes user

response:

`200 OK` - user deleted

### GET `/notes/{note_id}`

response:

```
{
  "id": note id,
  "text": note text
}
```

`404 not not found` - note does not exist

### POST `/notes/`

creates new note

body:
```
{
  "user_id": user id,
  "text": text
}
```

response:

`200 OK` - note created

`400 bad data sent` - server can't decode your data

`400 no user id in body` - no user id in request body

`400 no note text in body` - no note text in request body

`400 this user does not exist` - this user does not exist

### PUT `/notes/{note_id}`

changes note text

body:
```
{
  "text": new text
}
```

response:

`200 OK` - note updated

`400 bad data sent` - server can't decode your data

`400 no note text in body` - no note text in request body

`404 note not found` - note with selected id does not exist

### DELETE `/notes/{note_id}`

deletes selected note

response:

`200 OK` - note deleted

## telegram docs

`/start` - info message

`/check {name}` - get information about count of user rows/is user exist

`/add {name}` - add new user

`/del {name}` - del user and all his rows`

`/addrow {name} {text}` - add new row for user with text given

`/delrow {id}` - delete row with id given

`/updrow {id} {text}` - update selected row with given text
